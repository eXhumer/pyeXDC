from __future__ import annotations
from datetime import datetime, timedelta
from json import dumps, loads
from logging import getLogger
from random import uniform
from struct import unpack
from sys import platform
from urllib.parse import urlencode
from zlib import decompressobj

from websocket import ABNF, create_connection, WebSocketTimeoutException

from ._rest import REST
from .._consts import __user_agent__
from ..exception import GatewayHBNoAckException, GatewayNotConnectedException, \
    GatewayReceiveTimeout
from ..type.gateway import DispatchPayload, HeartbeatPayload, IdentifyData, IdentifyPayload, \
    IdentifyProperties, Operation, PresenceUpdateData, PresenceUpdatePayload, ReadyEventData, \
    ReceiveEvent, ResumeData, ResumePayload


class Gateway:
    """Client to communicate with Discord Gateway"""

    VERSION = 10
    __LOGGER = getLogger("exdc.Gateway")
    __URL = None

    def __enter__(self):
        if not self.connected:
            if self.ready:
                self._resume()

            else:
                self._connect()

        return self

    def __exit__(self, *exc_args):
        self._close(status=1000)

    def __init__(self, token: str, intents: int, presence_update: PresenceUpdateData | None = None,
                 reconnect: bool = True, timeout: int = 3, user_agent: str | None = None):
        self.__first_hb_at = None
        self.__hb_interval_ms = None
        self.__intents = intents
        self.__jitter = uniform(0, 1)
        self.__last_hb_ack = None
        self.__last_hb_sent = None
        self.__presence_update = presence_update
        self.__ready_event_data = None
        self.__reconnect = reconnect
        self.__sequence = None
        self.__timeout = timeout
        self.__token = token
        self.__user_agent = user_agent
        self.__ws = None
        self.__zlib_ctx = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self.connected:
            raise StopIteration

        status, data = self._recv()

        if status == ABNF.OPCODE_CLOSE:
            raise GatewayNotConnectedException

        return status, data

    def _close(self, status: int = 1000):
        if self.connected:
            self.__ws.close(status=status)

        if status in [1000, 1001]:
            self.__first_hb_at = None
            self.__hb_interval_ms = None
            self.__last_hb_ack = None
            self.__last_hb_sent = None
            self.__presence_update = None
            self.__ready_event_data = None
            self.__sequence = None
            self.__ws = None
            self.__zlib_ctx = None

    def _connect(self):
        """Method to create new gateay connection."""
        if self.connected:
            Gateway.__LOGGER.warn("Active gateway connection exists for client already! " +
                                  "Closing previous connection!")
            self._close(status=1000)

        if not Gateway.__URL:
            Gateway.__LOGGER.info("Gateway URL not cached! Attempting to get gateway URL!")
            gateway_data = REST.get_gateway()
            Gateway.__URL = gateway_data["url"]
            Gateway.__LOGGER.info(f"Gateway URL: {Gateway.__URL}")

        params = {"v": self.VERSION, "encoding": "json", "compress": "zlib-stream"}
        self.__ws = create_connection(f"{Gateway.__URL}?{urlencode(params)}",
                                      timeout=self.__timeout,
                                      header={"User-Agent": self.__user_agent or __user_agent__},
                                      skip_utf8_validation=True)
        Gateway.__LOGGER.info("Gateway connection created!")
        self.__zlib_ctx = decompressobj()

    def _heartbeat(self):
        assert self.connected

        Gateway.__LOGGER.info("Sending heartbeat payload!")
        self._send(dumps(HeartbeatPayload(op=Operation.HEARTBEAT, d=self.__sequence, s=None,
                                          t=None)))
        self.__last_hb_sent = datetime.utcnow()

    def _identify(self):
        assert self.connected

        Gateway.__LOGGER.info("Sending identify payload!")
        self._send(dumps(IdentifyPayload(op=Operation.IDENTIFY,
                                         d=IdentifyData(token=self.__token,
                                                        properties=IdentifyProperties(
                                                            os=platform, browser=__package__,
                                                            device=__package__),
                                                        intents=self.__intents,
                                                        presence=self.__presence_update), s=None,
                                         t=None)))

    def _recv(self):
        """Method to create new gateay connection."""
        assert self.connected

        while True:
            if self.__first_hb_at and datetime.utcnow() >= self.__first_hb_at:
                self._heartbeat()
                self.__first_hb_at = None

            if self.__hb_interval_ms and self.__last_hb_sent:
                if datetime.utcnow() > self.__last_hb_sent + \
                        timedelta(milliseconds=self.__hb_interval_ms):
                    if not self.__last_hb_ack or self.__last_hb_sent > self.__last_hb_ack:
                        Gateway.__LOGGER.error("No heartbeat ACK from gateway! " +
                                               "Aborting connection!")
                        raise GatewayHBNoAckException(
                            self.__last_hb_sent, timedelta(milliseconds=self.__hb_interval_ms))

                    else:
                        self._heartbeat()

            try:
                opcode, data = self.__ws.recv_data()

                if opcode == ABNF.OPCODE_CLOSE:
                    close_code: int = unpack("!H", data[0:2])[0]

                    if close_code != 4000:
                        Gateway.__LOGGER.error("Gateway closed connection with close code " +
                                               f"{close_code}!")
                        raise GatewayNotConnectedException

                    elif self.ready:
                        self._resume()
                        continue

                    else:
                        self._connect()
                        continue

                elif opcode == ABNF.OPCODE_BINARY:
                    data = self.__zlib_ctx.decompress(data)

                else:
                    raise ValueError(f"Received unexpected opcode {opcode}!")

                payload = loads(data)

                if payload["op"] == Operation.DISPATCH:
                    dispatch_payload: DispatchPayload = payload

                    if payload["t"] == ReceiveEvent.READY:
                        ready_event_data: ReadyEventData = payload["d"]
                        self.__ready_event_data = ready_event_data

                    return dispatch_payload["t"], dispatch_payload["d"]

                elif payload["op"] == Operation.HEARTBEAT:
                    self._heartbeat()
                    continue

                elif payload["op"] == Operation.RECONNECT:
                    if self.__ready_event_data:
                        if self.__reconnect:
                            self._close(status=1011)
                            self._resume()

                        else:
                            pass

                    else:
                        self._connect()

                    continue

                elif payload["op"] == Operation.INVALID_SESSION:
                    self._close()

                    if self.__reconnect:
                        self._connect()
                        continue

                    raise GatewayNotConnectedException

                elif payload["op"] == Operation.HELLO:
                    Gateway.__LOGGER.info("Gateway sent HELLO payload!")
                    hb_interval_ms: int = payload["d"]["heartbeat_interval"]
                    self.__hb_interval_ms = hb_interval_ms
                    self.__first_hb_at = datetime.utcnow() + timedelta(milliseconds=self.__jitter *
                                                                       self.__hb_interval_ms)
                    self._identify()
                    continue

                elif payload["op"] == Operation.HEARTBEAT_ACK:
                    self.__last_hb_ack = datetime.utcnow()
                    assert self.__last_hb_sent
                    delta = self.__last_hb_ack - self.__last_hb_sent
                    Gateway.__LOGGER.info("Gateway ACK heartbeat!")
                    Gateway.__LOGGER.info(f"Ping: {delta.total_seconds() * 1000}ms")
                    continue

                else:
                    raise ValueError(f"Unknown Gateway opcode {payload['op']} received!")

            except WebSocketTimeoutException:
                raise GatewayReceiveTimeout

    def _resume(self):
        assert self.__ready_event_data and self.__zlib_ctx

        resume_gateway_url = self.__ready_event_data["resume_gateway_url"]
        self.__ws = create_connection(resume_gateway_url, timeout=self.__timeout,
                                      header={"User-Agent": self.__user_agent or __user_agent__},
                                      skip_utf8_validation=True)

        session_id = self.__ready_event_data["session_id"]
        Gateway.__LOGGER.info("Sending resume payload!")
        self._send(dumps(ResumePayload(op=Operation.RESUME, d=ResumeData(token=self.__token,
                                                                         session_id=session_id,
                                                                         seq=self.__sequence),
                                       s=None, t=None)))

    def _send(self, payload: str):
        assert self.connected

        assert len(payload.encode("utf8")) <= 4096, "Discord only supports payload of 4096 " + \
            "bytes maximum!"

        self.__ws.send(payload)

    @property
    def connected(self):
        return self.__ws is not None and self.__ws.connected

    @property
    def presence_update(self):
        return self.__presence_update

    @presence_update.setter
    def presence_update(self, presence_update: PresenceUpdateData):
        self.__presence_update = presence_update
        self._send(dumps(PresenceUpdatePayload(op=Operation.PRESENCE_UPDATE, d=presence_update,
                                               s=None, t=None)))

    @property
    def ready(self):
        return self.__ready_event_data is not None
