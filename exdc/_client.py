# eXDC - Discord client
# Copyright (C) 2022  eXhumer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, version 3 of the
# License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
from mimetypes import guess_extension
from pkg_resources import require
from random import randint
from typing import IO, List, Tuple

from requests import Session
from requests.utils import default_user_agent
from requests_toolbelt import MultipartEncoder

from .type import AllowedMention, Attachment, ComponentActionRow, Embed, EmbedImage, \
    EmbedThumbnail, EmbedVideo, MessageFlag, MessagePayload, MessageReference, Snowflake

__version__ = require(__package__)[0].version
__user_agent__ = f"{__package__}/{__version__}"


class DiscordBotAuthorization:
    def __init__(self, bot_token: str) -> None:
        self.__token = bot_token

    def __str__(self):
        return f"Bot {self.__token}"


class DiscordClient:
    __rest_api_url = "https://discord.com/api"
    __rest_api_version = 10
    __rest_session = Session()
    __rest_session.headers["User-Agent"] = __user_agent__

    def __init__(self, authorization: DiscordBotAuthorization, session: Session | None = None):
        session = session or DiscordClient.__rest_session

        if "User-Agent" not in session.headers or \
                session.headers["User-Agent"] == default_user_agent():
            session.headers["User-Agent"] = __user_agent__

        self.__authorization = authorization
        self.__session = session

    def __delete(self, uri: str, **kwargs):
        while uri.startswith("/"):
            uri = uri[1:]

        if "headers" in kwargs:
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = str(self.__authorization)

        else:
            kwargs.update({
                "headers": {"Authorization": str(self.__authorization)}
            })

        return self.__session.delete(
            "/".join((
                DiscordClient.__rest_api_url,
                f"v{DiscordClient.__rest_api_version}",
                uri,
            )),
            **kwargs,
        )

    def __get(self, uri: str, **kwargs):
        while uri.startswith("/"):
            uri = uri[1:]

        if "headers" in kwargs:
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = str(self.__authorization)

        else:
            kwargs.update({
                "headers": {"Authorization": str(self.__authorization)}
            })

        return self.__session.get(
            "/".join((
                DiscordClient.__rest_api_url,
                f"v{DiscordClient.__rest_api_version}",
                uri,
            )),
            **kwargs,
        )

    def __patch(self, uri: str, **kwargs):
        while uri.startswith("/"):
            uri = uri[1:]

        if "headers" in kwargs:
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = str(self.__authorization)

        else:
            kwargs.update({
                "headers": {"Authorization": str(self.__authorization)}
            })

        return self.__session.patch(
            "/".join((
                DiscordClient.__rest_api_url,
                f"v{DiscordClient.__rest_api_version}",
                uri,
            )),
            **kwargs,
        )

    def __post(self, uri: str, **kwargs):
        while uri.startswith("/"):
            uri = uri[1:]

        if "headers" in kwargs:
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = str(self.__authorization)

        else:
            kwargs.update({
                "headers": {"Authorization": str(self.__authorization)}
            })

        return self.__session.post(
            "/".join((
                DiscordClient.__rest_api_url,
                f"v{DiscordClient.__rest_api_version}",
                uri,
            )),
            **kwargs,
        )

    def __put(self, uri: str, **kwargs):
        while uri.startswith("/"):
            uri = uri[1:]

        if "headers" in kwargs:
            if "Authorization" not in kwargs["headers"]:
                kwargs["headers"]["Authorization"] = str(self.__authorization)

        else:
            kwargs.update({
                "headers": {"Authorization": str(self.__authorization)}
            })

        return self.__session.put(
            "/".join((
                DiscordClient.__rest_api_url,
                f"v{DiscordClient.__rest_api_version}",
                uri,
            )),
            **kwargs,
        )

    @staticmethod
    def __random_attachment_id():
        return randint(0, 0x7fffffffffffffff)

    def post_message(self, channel_id: str, content: str | None = None, tts: bool | None = None,
                     embeds: List[Embed] | None = None,
                     allowed_mentions: AllowedMention | None = None,
                     message_reference: MessageReference | None = None,
                     components: List[ComponentActionRow] | None = None,
                     sticker_ids: List[Snowflake | str | int] | None = None,
                     flags: MessageFlag | None = None,
                     attachments: List[Attachment] | None = None,
                     files: List[Tuple[IO[bytes], str] |
                                 Tuple[IO[bytes], str, str]] | None = None):
        assert content or embeds or sticker_ids or components or files

        payload_json: MessagePayload = {}

        if tts:
            payload_json["tts"] = tts

        if content:
            payload_json["content"] = content

        if sticker_ids:
            payload_json["sticker_ids"] = [str(id) for id in sticker_ids]

        if allowed_mentions:
            allowed_mentions["parse"] = [str(data) for data in allowed_mentions["parse"]]
            allowed_mentions["roles"] = [str(data) for data in allowed_mentions["roles"]]
            payload_json["allowed_mentions"] = allowed_mentions

        if message_reference:
            if "message_id" in message_reference:
                message_reference["message_id"] = str(message_reference["message_id"])

            if "channel_id" in message_reference:
                message_reference["channel_id"] = str(message_reference["channel_id"])

            if "guild_id" in message_reference:
                message_reference["guild_id"] = str(message_reference["guild_id"])

            payload_json["message_reference"] = message_reference

        if components:
            payload_json["components"] = components

        if flags:
            payload_json["flags"] = flags

        if not attachments:
            attachments = []

        if not files:
            files = []

        if embeds:
            def new_attachment(stream: IO[bytes], mimetype: str):
                attach_id = DiscordClient.__random_attachment_id()
                attachments.append(Attachment(id=attachment_id))
                files.append((stream, mimetype, str(attachment_id)))
                return attach_id, f"{attachment_id}{guess_extension(mimetype, strict=False)}"

            for i, embed in enumerate(embeds):
                if "footer" in embed:
                    if not isinstance(embed["footer"]["icon_url"], str):
                        attachment_id, filename = new_attachment(*embed["footer"]["icon_url"])
                        embeds[i]["footer"]["icon_url"] = f"attachment://{filename}"

                if "image" in embed:
                    if not isinstance(embed["image"], dict):
                        attachment_id, filename = new_attachment(*embed["image"])
                        embeds[i]["image"] = EmbedImage(url=f"attachment://{filename}")

                if "thumbnail" in embed:
                    if not isinstance(embed["thumbnail"], dict):
                        attachment_id, filename = new_attachment(*embed["thumbnail"])
                        embeds[i]["thumbnail"] = EmbedThumbnail(url=f"attachment://{filename}")

                if "video" in embed:
                    if not isinstance(embed["video"], dict):
                        attachment_id, filename = new_attachment(*embed["video"])
                        embeds[i]["video"] = EmbedVideo(url=f"attachment://{filename}")

                if "author" in embed:
                    if not isinstance(embed["author"]["icon_url"], str):
                        attachment_id, filename = new_attachment(*embed["author"]["icon_url"])
                        embeds[i]["author"]["icon_url"] = f"attachment://{filename}"

            payload_json.update(embeds=embeds)

        if len(files) > 0:
            files_with_id: List[Tuple[IO[bytes], str, str]] = []

            for file in files:
                if len(file) == 2:
                    attachment_id = DiscordClient.__random_attachment_id()
                    attachments.append(Attachment(id=attachment_id))
                    files_with_id.append((*file, attachment_id))

                else:
                    files_with_id.append(file)

            mp_fields = {
                "payload_json": (
                    None,
                    json.dumps(payload_json, separators=(",", ":")),
                    "application/json",
                ),
            }

            for stream, content_type, attachment_id in files_with_id:
                mp_fields |= {
                    f"files[{attachment_id}]": (
                        None,
                        stream,
                        content_type,
                    ),
                }

            mp_encoder = MultipartEncoder(fields=mp_fields)

            r = self.__post(f"channels/{channel_id}/messages", data=mp_encoder,
                            headers={"Content-Type": mp_encoder.content_type})

        else:
            r = self.__post(f"channels/{channel_id}/messages", json=payload_json)

        r.raise_for_status()
        return r

    @staticmethod
    def post_webhook_message(webhook_id: str, webhook_token: str, content: str | None = None,
                             username: str | None = None, avatar_url: str | None = None,
                             tts: bool | None = None, embeds: List[Embed] | None = None,
                             allowed_mentions: AllowedMention | None = None,
                             components: List[ComponentActionRow] | None = None,
                             flags: int | None = None, attachments: List[Attachment] | None = None,
                             files: List[Tuple[IO[bytes], str] | Tuple[IO[bytes], str, str]] |
                             None = None, wait: bool | None = None,
                             thread_id: Snowflake | str | int | None = None,
                             session: Session | None = None):
        assert content or embeds or components or files

        session = session or DiscordClient.__rest_session

        payload_json: MessagePayload = {}

        if content:
            payload_json["content"] = content

        if username:
            payload_json["username"] = username

        if avatar_url:
            payload_json["avatar_url"] = avatar_url

        if tts:
            payload_json["tts"] = tts

        if allowed_mentions:
            allowed_mentions["parse"] = [str(data) for data in allowed_mentions["parse"]]
            allowed_mentions["roles"] = [str(data) for data in allowed_mentions["roles"]]
            payload_json["allowed_mentions"] = allowed_mentions

        if components:
            payload_json["components"] = components

        if flags:
            payload_json["flags"] = flags

        if not attachments:
            attachments = []

        if not files:
            files = []

        if embeds:
            def new_attachment(stream: IO[bytes], mimetype: str):
                attachment_id = DiscordClient.__random_attachment_id()
                attachments.append(Attachment(id=attachment_id))
                files.append((stream, mimetype, str(attachment_id)))
                return attachment_id, f"{attachment_id}{guess_extension(mimetype, strict=False)}"

            for i, embed in enumerate(embeds):
                if "footer" in embed:
                    if not isinstance(embed["footer"]["icon_url"], str):
                        attachment_id, filename = new_attachment(*embed["footer"]["icon_url"])
                        embeds[i]["footer"]["icon_url"] = f"attachment://{filename}"

                if "image" in embed:
                    if not isinstance(embed["image"], dict):
                        attachment_id, filename = new_attachment(*embed["image"])
                        embeds[i]["image"] = EmbedImage(url=f"attachment://{filename}")

                if "thumbnail" in embed:
                    if not isinstance(embed["thumbnail"], dict):
                        attachment_id, filename = new_attachment(*embed["thumbnail"])
                        embeds[i]["thumbnail"] = EmbedThumbnail(url=f"attachment://{filename}")

                if "video" in embed:
                    if not isinstance(embed["video"], dict):
                        attachment_id, filename = new_attachment(*embed["video"])
                        embeds[i]["video"] = EmbedVideo(url=f"attachment://{filename}")

                if "author" in embed:
                    if not isinstance(embed["author"]["icon_url"], str):
                        attachment_id, filename = new_attachment(*embed["author"]["icon_url"])
                        embeds[i]["author"]["icon_url"] = f"attachment://{filename}"

            payload_json.update(embeds=embeds)

        if len(files) > 0:
            files_with_id: List[Tuple[IO[bytes], str, str]] = []

            for file in files:
                if len(file) == 2:
                    attachment_id = DiscordClient.__random_attachment_id()
                    attachments.append(Attachment(id=attachment_id))
                    files_with_id.append((*file, attachment_id))

                else:
                    files_with_id.append(file)

            mp_fields = {
                "payload_json": (
                    None,
                    json.dumps(payload_json, separators=(",", ":")),
                    "application/json",
                ),
            }

            for stream, content_type, attachment_id in files_with_id:
                mp_fields |= {
                    f"files[{attachment_id}]": (
                        None,
                        stream,
                        content_type,
                    ),
                }

            mp_encoder = MultipartEncoder(fields=mp_fields)

            if wait or thread_id:
                params = {}

                if wait:
                    params |= {"wait": wait}

                if thread_id:
                    params |= {"thread_id": thread_id}

            r = session.post("/".join((DiscordClient.__rest_api_url,
                                       f"v{DiscordClient.__rest_api_version}", "webhooks",
                                       webhook_id, webhook_token)),
                             data=mp_encoder, headers={"Content-Type": mp_encoder.content_type},
                             params=params)

        else:
            r = session.post("/".join((DiscordClient.__rest_api_url,
                                      f"v{DiscordClient.__rest_api_version}", "webhooks",
                                       webhook_id, webhook_token)),
                             json=payload_json, params=params)

        r.raise_for_status()
        return r

    @classmethod
    def with_bot_token(cls, token: str, session: Session | None = None):
        return cls(DiscordBotAuthorization(token), session=session)
