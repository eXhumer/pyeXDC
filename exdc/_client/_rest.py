from logging import getLogger

from httpx import Client

from .._consts import __user_agent__
from ..exception import RESTException
from ..type.interactions.application_command import ApplicationCommand
from ..type.interactions import Interaction, InteractionResponse
from ..type.rest import GetGatewayResponse

try:
    import h2  # noqa: F401
    h2_available = True

except ImportError:
    h2_available = False


class REST:
    API_URL = "https://discord.com/api"
    VERSION = 10
    __LOGGER = getLogger("exdc.REST")

    def __init__(self, authorization: str | None = None, http_client: Client | None = None,
                 user_agent: str | None = None):
        self.__http_client = REST.__setup_http_client(authorization=authorization,
                                                      http_client=http_client,
                                                      user_agent=user_agent)

    @staticmethod
    def __setup_http_client(authorization: str | None = None, http_client: Client | None = None,
                            user_agent: str | None = None):
        if not http_client:
            http_client = Client(http2=h2_available)

        http_client.base_url = f"{REST.API_URL}/v{REST.VERSION}/"
        http_client.follow_redirects = True
        http_client.headers["User-Agent"] = user_agent or __user_agent__

        if authorization:
            http_client.headers["Authorization"] = authorization

        return http_client

    def add_global_command(self, application_id: str, command: ApplicationCommand):
        res = self.__http_client.post(f"applications/{application_id}/commands", json=command)

        if not res.is_success:
            print(res.status_code)
            print(res.text)
            raise RESTException(res)

        return res

    def add_guild_command(self, application_id: str, guild_id: str, command: ApplicationCommand):
        res = self.__http_client.post(f"applications/{application_id}/guilds/{guild_id}/commands",
                                      json=command)

        if not res.is_success:
            raise RESTException(res)

        return res

    def delete_global_command(self, application_id: str, command_id: str):
        res = self.__http_client.delete(f"applications/{application_id}/commands/{command_id}")

        if not res.is_success:
            raise RESTException(res)

        return res

    def delete_guild_command(self, application_id: str, guild_id: str, command_id: str):
        res = self.__http_client.delete(f"applications/{application_id}/guilds/{guild_id}/" +
                                        f"commands/{command_id}")

        if not res.is_success:
            raise RESTException(res)

        return res

    @staticmethod
    def get_gateway(http_client: Client | None = None, user_agent: str | None = None):
        http_client = REST.__setup_http_client(http_client=http_client, user_agent=user_agent)
        res = http_client.get("gateway")

        if not res.is_success:
            raise RESTException(res)

        data: GetGatewayResponse = res.json()
        return data

    def get_global_command(self, application_id: str, command_id: str):
        res = self.__http_client.get(f"applications/{application_id}/commands/{command_id}")

        if not res.is_success:
            raise RESTException(res)

        return res

    def get_global_commands(self, application_id: str, with_localizations: bool | None = None):
        if with_localizations is not None:
            params = {"with_localizations": with_localizations}

        else:
            params = None

        res = self.__http_client.get(f"applications/{application_id}/commands", params=params)

        if not res.is_success:
            raise RESTException(res)

        return res

    def get_guild_command(self, application_id: str, guild_id: str, command_id: str):
        res = self.__http_client.get(f"applications/{application_id}/guilds/{guild_id}/" +
                                     f"commands/{command_id}")

        if not res.is_success:
            raise RESTException(res)

        return res

    def get_guild_commands(self, application_id: str, guild_id: str,
                           with_localizations: bool | None = None):
        if with_localizations is not None:
            params = {"with_localizations": with_localizations}

        else:
            params = None

        res = self.__http_client.get(f"applications/{application_id}/guilds/{guild_id}/commands",
                                     params=params)

        if not res.is_success:
            raise RESTException(res)

        return res

    def interaction_response(self, interaction: Interaction, callback: InteractionResponse):
        res = self.__http_client.post(
            f"interactions/{interaction['id']}/{interaction['token']}/callback", json=callback)

        if not res.is_success:
            raise RESTException(res)

        return res

    def update_global_command(self, application_id: str, command_id: str,
                              command: ApplicationCommand):
        res = self.__http_client.patch(f"applications/{application_id}/commands/{command_id}",
                                       json=command)

        if not res.is_success:
            raise RESTException(res)

        return res

    def update_guild_command(self, application_id: str, guild_id: str, command_id: str,
                             command: ApplicationCommand):
        res = self.__http_client.patch(f"applications/{application_id}/guilds/{guild_id}/" +
                                       f"commands/{command_id}", json=command)

        if not res.is_success:
            raise RESTException(res)

        return res

    @classmethod
    def with_bot_token(cls, token: str, http_client: Client | None = None,
                       user_agent: str | None = None):
        return cls(f"Bot {token}", http_client=http_client, user_agent=user_agent)
