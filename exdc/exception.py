from datetime import datetime, timedelta

from httpx import Response


class GatewayException(Exception):
    pass


class GatewayNotConnectedException(GatewayException):
    pass


class GatewayReceiveTimeout(Exception):
    pass


class GatewayHBNoAckException(GatewayException):
    def __init__(self, heartbeat_sent: datetime, heartbeat_interval: timedelta):
        super().__init__(f"Expected heartbeat ACK by {heartbeat_sent + heartbeat_interval}!")


class RESTException(Exception):
    def __init__(self, res: Response):
        self.__res = res
        super().__init__(f"REST exception occurred with status code {self.__res.status_code}!")

    @property
    def response(self):
        return self.__res
