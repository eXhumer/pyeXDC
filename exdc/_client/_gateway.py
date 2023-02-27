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
from ..exception import GatewayNotConnectedException, GatewayReceiveTimeout
from ..type.gateway import DispatchPayload, HeartbeatPayload, IdentifyData, IdentifyPayload, \
    IdentifyProperties, Operation, PresenceUpdateData, PresenceUpdatePayload, ReadyEventData, \
    ReceiveEvent, ResumeData, ResumePayload


class Gateway:
    """Client to communicate with Discord Gateway"""

    VERSION = 10
    __REST_CLIENT = REST()
    __LOGGER = getLogger("exdc.Gateway")
    __URL = None

    def __enter__(self):
        # Check make sure there is a valid connection when context manager is entered
        if not self.connected:
            # Try to resume connection if we have existing session data, otherwise start a new
            # connection
            self._resume() if self.ready else self._connect()

        return self

    def __exit__(self, *exc_args):
        # Close connection asking gateway to invalidate current session when context manager is
        # exited.
        self._close(status=1000)

    def __init__(self, token: str, intents: int, presence_update: PresenceUpdateData | None = None,
                 timeout: int = 3, user_agent: str | None = None):
        self.__first_hb_at = None
        self.__hb_interval_ms = None
        self.__intents = intents
        self.__jitter = uniform(0, 1)
        self.__last_hb_ack = None
        self.__last_hb_sent = None
        self.__presence_update = presence_update
        self.__ready_event_data = None
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
            # Stop iteration if we are no longer connected, as there is no gateway connection to
            # get data from
            raise StopIteration

        return self._recv()

    def _close(self, status: int = 1000):
        """Close gateway connection, clears session variables if status is 1000/1001."""
        # If we have a valid gateway connection
        if self.connected:
            # Close connection with status provided
            self.__ws.close(status=status)

        if status in [1000, 1001]:
            # If non resumable status, clear all session variables
            self.__ready_event_data = None
            self.__sequence = None
            self.__ws = None

        self.__zlib_ctx = None

        # Clear heartbeat data
        self.__first_hb_at = None
        self.__hb_interval_ms = None
        self.__last_hb_ack = None
        self.__last_hb_sent = None

    def _connect(self):
        """Create new gateay connection"""
        if self.connected:
            Gateway.__LOGGER.warn("Active gateway connection exists for client already! " +
                                  "Closing previous connection!")
            self._close(status=1000)

        # If gateway URL hasn't been cached
        if not Gateway.__URL:
            # GET it from REST client and cache it
            Gateway.__LOGGER.info("Gateway URL not cached! Attempting to get gateway URL!")
            gateway_data = Gateway.__REST_CLIENT.get_gateway()
            Gateway.__URL = gateway_data["url"]
            Gateway.__LOGGER.info(f"Gateway URL: {Gateway.__URL}")

        # Create a new gateway connection with zlib transport stream compression
        params = {"v": self.VERSION, "encoding": "json", "compress": "zlib-stream"}
        self.__ws = create_connection(f"{Gateway.__URL}?{urlencode(params)}",
                                      timeout=self.__timeout,
                                      header={"User-Agent": self.__user_agent or __user_agent__},
                                      skip_utf8_validation=True)
        Gateway.__LOGGER.info("Gateway connection created!")
        self.__zlib_ctx = decompressobj()

    def _heartbeat(self):
        """Method to send heartbeat to gateway"""
        Gateway.__LOGGER.info("Sending heartbeat payload!")
        self._send(dumps(HeartbeatPayload(op=Operation.HEARTBEAT, d=self.__sequence, s=None,
                                          t=None)))
        self.__last_hb_sent = datetime.utcnow()

    def _heartbeat_check(self):
        """Method to check heartbeat and heartbeat ack status"""
        # If first heartbeat datetime set and first heartbeat is due by client
        if self.__first_hb_at and datetime.utcnow() >= self.__first_hb_at:
            # Send heartbeat
            self._heartbeat()
            # And clear first heartbeat datetime
            self.__first_hb_at = None

        # If we received heartbeat interval and we have sent a heartbeat
        elif self.__hb_interval_ms and self.__last_hb_sent:
            # If we are due to send a heartbeat
            if datetime.utcnow() > self.__last_hb_sent + \
                    timedelta(milliseconds=self.__hb_interval_ms):
                # If we haven't received heartbeat ack for last heartbeat
                if not self.__last_hb_ack or self.__last_hb_sent > self.__last_hb_ack:
                    Gateway.__LOGGER.warn("No heartbeat ACK from gateway for last heartbeat!" +
                                          " Aborting connection and attempting to resume!")
                    # Close connection with non 1000/1001 error
                    self._close(status=1011)

                    # Attempt to resume
                    self._resume()

                # If we have received heartbeat ack for last heartbeat
                else:
                    # Send new heartbeat
                    self._heartbeat()

    def _identify(self):
        """Method to identify client to gateway"""
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
        """Receive new data from gateway connection"""
        # Loop incase we are requested to reconnect by gateway, need to go through all checks
        # before we receive any new data
        while True:
            self._heartbeat_check()

            try:
                opcode, data = self.__ws.recv_data()

                if opcode == ABNF.OPCODE_CLOSE:
                    if len(data) == 0:
                        self._close(status=1011)
                        self._resume()
                        continue

                    else:
                        close_code: int = unpack("!H", data[0:2])[0]

                        if close_code != 4000:
                            Gateway.__LOGGER.error("Gateway closed connection with close code " +
                                                   f"{close_code}!")
                            Gateway.__LOGGER.error(f"Data: {data[2:]}")
                            raise GatewayNotConnectedException

                        elif self.ready:
                            self._close(status=1011)
                            self._resume()
                            continue

                        else:
                            self._close()
                            self._connect()
                            continue

                elif opcode == ABNF.OPCODE_BINARY:
                    data = self.__zlib_ctx.decompress(data)

                else:
                    print(data)
                    raise ValueError(f"Received unexpected opcode {opcode}!")

                payload = loads(data)

                if payload["op"] == Operation.DISPATCH:
                    dispatch_payload: DispatchPayload = payload

                    if payload["t"] == ReceiveEvent.READY:
                        ready_event_data: ReadyEventData = payload["d"]
                        self.__ready_event_data = ready_event_data

                    return dispatch_payload["t"], dispatch_payload["d"]

                elif payload["op"] == Operation.HEARTBEAT:
                    # Gateway requested heartbeat from client
                    self._heartbeat()
                    continue

                elif payload["op"] == Operation.RECONNECT:
                    if self.ready:
                        self._close(status=1011)
                        self._resume()
                        continue

                    else:
                        self._close()
                        self._connect()
                        continue

                elif payload["op"] == Operation.INVALID_SESSION:
                    if payload["d"] is True:
                        self._close(status=1011)
                        self._resume()
                        continue

                    else:
                        self._close()
                        self._connect()
                        continue

                elif payload["op"] == Operation.HELLO:
                    Gateway.__LOGGER.info("Gateway sent HELLO payload!")
                    hb_interval_ms: int = payload["d"]["heartbeat_interval"]
                    self.__hb_interval_ms = hb_interval_ms
                    self.__first_hb_at = datetime.utcnow() + timedelta(milliseconds=self.__jitter *
                                                                       self.__hb_interval_ms)

                    # If gateway hasn't sent a READY before, IDENTIFY to gateway
                    if not self.ready:
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
        """Resume existing gateway connection"""
        assert self.__ready_event_data and self.__zlib_ctx

        resume_gateway_url = self.__ready_event_data["resume_gateway_url"]
        params = {"v": self.VERSION, "encoding": "json", "compress": "zlib-stream"}
        self.__ws = create_connection(f"{resume_gateway_url}?{urlencode(params)}",
                                      timeout=self.__timeout, skip_utf8_validation=True,
                                      header={"User-Agent": self.__user_agent or __user_agent__})
        self.__zlib_ctx = decompressobj()
        session_id = self.__ready_event_data["session_id"]
        Gateway.__LOGGER.info("Sending resume payload!")
        self._send(dumps(ResumePayload(op=Operation.RESUME, d=ResumeData(token=self.__token,
                                                                         session_id=session_id,
                                                                         seq=self.__sequence),
                                       s=None, t=None)))

    def _send(self, payload: str):
        """Send utf8 encoded payload to gateway"""
        assert len(payload.encode("utf8")) <= 4096, "Discord only supports payload of 4096 " + \
            "bytes maximum!"

        self.__ws.send(payload)

    @property
    def connected(self):
        """Gatway client connection status"""
        return self.__ws is not None and self.__ws.connected

    @property
    def presence_update(self):
        """Gateway client presence update status"""
        return self.__presence_update

    @presence_update.setter
    def presence_update(self, presence_update: PresenceUpdateData):
        self.__presence_update = presence_update
        self._send(dumps(PresenceUpdatePayload(op=Operation.PRESENCE_UPDATE, d=presence_update,
                                               s=None, t=None)))

    @property
    def ready(self):
        """Check if gateway client received READY event from gateway"""
        return self.__ready_event_data is not None
