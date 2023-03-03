from json import dumps
from logging import getLogger
from mimetypes import guess_type
from pathlib import Path
from random import randint
from typing import IO

from httpx import Client

from .._consts import __user_agent__
from ..exception import RESTException
from ..type.channel import AllowedMentions, Attachment, Channel, Embed, MessageFlag, \
    MessageReference
from ..type.interactions import Interaction, InteractionResponse
from ..type.interactions.application_command import ApplicationCommand
from ..type.interactions.message_component import ActionRowComponent
from ..type.rest import GetGatewayResponse

try:
    import h2  # noqa: F401
    h2_available = True

except ImportError:
    h2_available = False


class REST:
    API_URL = "https://discord.com/api"
    VERSION = 10
    __CLIENT = None
    __LOGGER = getLogger("exdc.REST")

    def __init__(self, authorization: str | None = None, user_agent: str | None = None):
        if REST.__CLIENT is None:
            REST.__CLIENT = Client(http2=h2_available)
            REST.__CLIENT.base_url = f"{REST.API_URL}/v{REST.VERSION}/"
            REST.__CLIENT.follow_redirects = True
            REST.__CLIENT.headers["User-Agent"] = __user_agent__

        self.__authorization = authorization
        self.__user_agent = user_agent

    def _request(self, method: str, url: str, **kwargs):
        if self.__user_agent:
            if "headers" in kwargs:
                kwargs["headers"] |= {"User-Agent": self.__user_agent}

            else:
                kwargs["headers"] = {"User-Agent": self.__user_agent}

        if self.__authorization:
            if "headers" in kwargs:
                kwargs["headers"] |= {"Authorization": self.__authorization}

            else:
                kwargs["headers"] = {"Authorization": self.__authorization}

        res = REST.__CLIENT.request(method, url, **kwargs)

        if res.status_code >= 400:
            raise RESTException(res)

        return res

    def add_global_command(self, application_id: str, command: ApplicationCommand):
        return self._request("POST", f"applications/{application_id}/commands", json=command)

    def add_guild_command(self, application_id: str, guild_id: str, command: ApplicationCommand):
        return self._request("POST", f"applications/{application_id}/guilds/{guild_id}/commands",
                             json=command)

    def create_dm_channel(self, recipient_id: str):
        res = self._request("POST", "users/@me/channels", json={"recipient_id": recipient_id})
        channel: Channel = res.json()
        return channel

    def delete_global_command(self, application_id: str, command_id: str):
        return self._request("DELETE", f"applications/{application_id}/commands/{command_id}")

    def delete_guild_command(self, application_id: str, guild_id: str, command_id: str):
        return self._request("DELETE", f"applications/{application_id}/guilds/{guild_id}/" +
                             f"commands/{command_id}")

    def get_gateway(self):
        res = self._request("GET", "gateway")
        data: GetGatewayResponse = res.json()
        return data

    def get_global_command(self, application_id: str, command_id: str):
        return self._request("GET", f"applications/{application_id}/commands/{command_id}")

    def get_global_commands(self, application_id: str, with_localizations: bool | None = None):
        if with_localizations is not None:
            params = {"with_localizations": with_localizations}

        else:
            params = None

        res = self._request("GET", f"applications/{application_id}/commands", params=params)

        return res

    def get_guild_command(self, application_id: str, guild_id: str, command_id: str):
        res = self._request("GET", f"applications/{application_id}/guilds/{guild_id}/" +
                            f"commands/{command_id}")

        return res

    def get_guild_commands(self, application_id: str, guild_id: str,
                           with_localizations: bool | None = None):
        if with_localizations is not None:
            params = {"with_localizations": with_localizations}

        else:
            params = None

        res = self._request("GET", f"applications/{application_id}/guilds/{guild_id}/commands",
                            params=params)

        return res

    def interaction_response(self, interaction: Interaction, callback: InteractionResponse):
        res = self._request("POST",
                            f"interactions/{interaction['id']}/{interaction['token']}/callback",
                            json=callback)

        return res

    def post_message(self, channel_id: str, content: str | None = None, tts: bool | None = None,
                     embeds: list[Embed] | None = None,
                     allowed_mentions: AllowedMentions | None = None,
                     message_reference: MessageReference | None = None,
                     components: list[ActionRowComponent] | None = None,
                     sticker_ids: list[str] | None = None, flags: MessageFlag | None = None,
                     attachments: list[Attachment] | None = None,
                     uploads: list[tuple[IO[bytes], str, str | None]] | None = None):
        assert content or embeds or sticker_ids or components or uploads

        payload = {}

        if embeds:
            payload |= {"embeds": embeds}

        if tts:
            payload |= {"tts": tts}

        if content:
            payload |= {"content": content}

        if sticker_ids:
            payload |= {"sticker_ids": sticker_ids}

        if allowed_mentions:
            payload |= {"allowed_mentions": allowed_mentions}

        if message_reference:
            payload |= {"message_reference": message_reference}

        if components:
            payload |= {"components": components}

        if flags:
            payload |= {"flags": flags}

        if attachments:
            payload |= {"attachments": attachments}

        if uploads:
            files = {
                "payload_json": (None, dumps(payload, separators=(",", ":")), "application/json"),
            }

            for stream, filename, attachment_id in uploads:
                attachment_id = attachment_id or REST.random_attachment_id()
                mimetype = guess_type(filename, strict=False)[0]
                assert mimetype is not None and mimetype.startswith(("image/", "video/"))

                files |= {
                    f"files[{attachment_id}]": (f"{attachment_id}{Path(filename).suffix}",
                                                stream, mimetype),
                }

            json = None

        else:
            files = None
            json = payload

        res = self._request("POST", f"channels/{channel_id}/messages", files=files, json=json)

        return res

    @staticmethod
    def post_webhook_message(webhook_id: str, webhook_token: str, content: str | None = None,
                             username: str | None = None, avatar_url: str | None = None,
                             tts: bool | None = None, embeds: list[Embed] | None = None,
                             allowed_mentions: AllowedMentions | None = None,
                             components: list[ActionRowComponent] | None = None,
                             flags: MessageFlag | None = None,
                             attachments: list[Attachment] | None = None,
                             uploads: list[tuple[IO[bytes], str, str | None]] | None = None,
                             wait: bool | None = None, thread_id: str | None = None):
        assert content or embeds or components or uploads

        payload = {}

        if embeds:
            payload |= {"embeds": embeds}

        if username:
            payload |= {"username": username}

        if avatar_url:
            payload |= {"avatar_url": avatar_url}

        if tts:
            payload |= {"tts": tts}

        if content:
            payload |= {"content": content}

        if allowed_mentions:
            payload |= {"allowed_mentions": allowed_mentions}

        if components:
            payload |= {"components": components}

        if flags:
            payload |= {"flags": flags}

        if attachments:
            payload |= {"attachments": attachments}

        if uploads:
            files = {
                "payload_json": (None, dumps(payload, separators=(",", ":")),
                                 "application/json"),
            }

            for stream, filename, attachment_id in uploads:
                attachment_id = attachment_id or REST.random_attachment_id()
                mimetype = guess_type(filename, strict=False)[0]
                assert mimetype is not None and mimetype.startswith(("image/", "video/"))

                files |= {
                    f"files[{attachment_id}]": (f"{attachment_id}{Path(filename).suffix}",
                                                stream, mimetype),
                }

            json = None

        else:
            files = None
            json = payload

        if wait is not None or thread_id is not None:
            params = {}

            if wait is not None:
                params |= {"wait": wait}

            if thread_id is not None:
                params |= {"thread_id": thread_id}

        else:
            params = None

        res = REST.__CLIENT.post(f"webhooks/{webhook_id}/{webhook_token}", files=files, json=json,
                                 params=params)

        if res.status_code >= 400:
            raise RESTException(res)

        return res

    @staticmethod
    def random_attachment_id():
        return str(randint(0, 0x7fffffffffffffff))

    def update_global_command(self, application_id: str, command_id: str,
                              command: ApplicationCommand):
        res = self._request("PATCH", f"applications/{application_id}/commands/{command_id}",
                            json=command)

        return res

    def update_guild_command(self, application_id: str, guild_id: str, command_id: str,
                             command: ApplicationCommand):
        res = self._request("PATCH", f"applications/{application_id}/guilds/{guild_id}/" +
                            f"commands/{command_id}", json=command)

        return res

    @classmethod
    def with_bot_token(cls, token: str, user_agent: str | None = None):
        return cls(f"Bot {token}", user_agent=user_agent)
