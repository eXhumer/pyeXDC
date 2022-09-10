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
from mimetypes import guess_type
from pathlib import Path
from random import randint
from typing import BinaryIO, List, TypedDict

from requests import Session
from requests_toolbelt import MultipartEncoder

from .type import AllowedMention, ComponentActionRow, Embed, EmbedImage, EmbedThumbnail, \
    EmbedVideo, MessageFlag, MessageReference, Snowflake


class AttachmentFile(TypedDict):
    id: int
    stream: BinaryIO
    filename: str
    content_type: str


class DiscordBotAuthorization:
    def __init__(self, bot_token: str) -> None:
        self.__token = bot_token

    def __str__(self) -> str:
        return f"Bot {self.__token}"


class DiscordClient:
    """Discord client
    """
    __rest_api_url = "https://discord.com/api"
    __rest_api_version = 9

    def __init__(self, authorization: DiscordBotAuthorization, session: Session | None = None):
        if session is None:
            session = Session()

        self.__authorization = authorization
        self.__session = session

    @staticmethod
    def __random_attachment_id():
        return randint(0, 0x7fffffffffffffff)

    def post_message(self, channel_id: str, content: str | None = None, tts: bool | None = None,
                     embeds: List[Embed] | None = None,
                     allowed_mentions: AllowedMention | None = None,
                     message_reference: MessageReference | None = None,
                     components: List[ComponentActionRow] | None = None,
                     sticker_ids: List[Snowflake | str | int] | None = None,
                     flags: MessageFlag | None = None, files: List[Path] | None = None):
        assert content or embeds or sticker_ids or files

        files_data: List[AttachmentFile] = []
        payload_json_data = {}

        if tts is not None:
            payload_json_data.update(tts=tts)

        if files:
            for file in files:
                attachment_id = DiscordClient.__random_attachment_id()
                filename = str(attachment_id) + file.suffix

                files_data.append({
                    "id": attachment_id,
                    "stream": file.open(mode="rb"),
                    "filename": filename,
                    "content_type": guess_type(filename)[0],
                })

        if content:
            payload_json_data.update(content=content)

        if embeds:
            for i, embed in enumerate(embeds):
                if "footer" in embed:
                    if not isinstance(embed["footer"]["icon_url"], str):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["footer"]["icon_url"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["footer"]["icon_url"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["footer"]["icon_url"] = f"attachment://{filename}"

                if "image" in embed:
                    if not isinstance(embed["image"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["image"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["image"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["image"]: EmbedImage = {"url": f"attachment://{filename}"}

                if "thumbnail" in embed:
                    if not isinstance(embed["thumbnail"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["thumbnail"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["thumbnail"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["thumbnail"]: EmbedThumbnail = {
                            "url": f"attachment://{filename}",
                        }

                if "video" in embed:
                    if not isinstance(embed["video"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["video"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["video"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["video"]: EmbedVideo = {"url": f"attachment://{filename}"}

                if "author" in embed:
                    if not isinstance(embed["author"]["icon_url"], str):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["author"]["icon_url"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["author"]["icon_url"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["author"]["icon_url"] = f"attachment://{filename}"

            payload_json_data.update(embeds=embeds)

        if sticker_ids:
            payload_json_data.update(sticker_ids=[str(id) for id in sticker_ids])

        if allowed_mentions:
            allowed_mentions["parse"] = [str(data) for data in allowed_mentions["parse"]]
            allowed_mentions["roles"] = [str(data) for data in allowed_mentions["roles"]]
            payload_json_data.update(allowed_mentions=allowed_mentions)

        if message_reference:
            if "message_id" in message_reference:
                message_reference["message_id"] = str(message_reference["message_id"])

            if "channel_id" in message_reference:
                message_reference["channel_id"] = str(message_reference["channel_id"])

            if "guild_id" in message_reference:
                message_reference["guild_id"] = str(message_reference["guild_id"])

            payload_json_data.update(message_reference=message_reference)

        if components:
            payload_json_data.update(components=components)

        if flags is not None:
            payload_json_data.update(flags=flags)

        if len(files_data) > 0:
            files_dict = {}
            payload_json_data.update(attachments=[])

            for file_data in files_data:
                files_dict.update({
                    f"files[{file_data['id']}]": (
                        file_data["filename"],
                        file_data["stream"],
                        file_data["content_type"],
                    )
                })
                payload_json_data["attachments"].append({
                    "id": file_data["id"],
                    "filename": file_data["filename"],
                })

            mp_encoder = MultipartEncoder(
                fields={
                    "payload_json": (
                        None,
                        json.dumps(payload_json_data, separators=(',', ':')),
                        "application/json",
                    ),
                    **files_dict,
                }
            )

            res = self.__post(
                f"channels/{channel_id}/messages",
                data=mp_encoder,
                headers={"Content-Type": mp_encoder.content_type},
            )

        else:
            res = self.__post(
                f"channels/{channel_id}/messages",
                json=payload_json_data,
            )

        res.raise_for_status()
        return res

    @staticmethod
    def post_webhook_message(webhook_id: str, webhook_token: str, content: str | None = None,
                             username: str | None = None, avatar_url: str | None = None,
                             tts: bool | None = None, embeds: List[Embed] | None = None,
                             allowed_mentions: AllowedMention | None = None,
                             components: List[ComponentActionRow] | None = None,
                             flags: int | None = None, files: List[Path] | None = None):
        assert content or embeds or files
        session = Session()

        files_data: List[AttachmentFile] = []
        payload_json_data = {}

        if tts is not None:
            payload_json_data.update(tts=tts)

        if files:
            for file in files:
                attachment_id = DiscordClient.__random_attachment_id()
                filename = str(attachment_id) + file.suffix

                files_data.append({
                    "id": attachment_id,
                    "stream": file.open(mode="rb"),
                    "filename": filename,
                    "content_type": guess_type(filename)[0],
                })

        if content:
            payload_json_data.update(content=content)

        if username:
            payload_json_data.update(username=username)

        if avatar_url:
            payload_json_data.update(avatar_url=avatar_url)

        if embeds:
            for i, embed in enumerate(embeds):
                if "footer" in embed:
                    if not isinstance(embed["footer"]["icon_url"], str):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["footer"]["icon_url"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["footer"]["icon_url"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["footer"]["icon_url"] = f"attachment://{filename}"

                if "image" in embed:
                    if not isinstance(embed["image"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["image"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["image"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["image"]: EmbedImage = {"url": f"attachment://{filename}"}

                if "thumbnail" in embed:
                    if not isinstance(embed["thumbnail"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["thumbnail"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["thumbnail"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["thumbnail"]: EmbedThumbnail = {
                            "url": f"attachment://{filename}",
                        }

                if "video" in embed:
                    if not isinstance(embed["video"], dict):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["video"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["video"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["video"]: EmbedVideo = {"url": f"attachment://{filename}"}

                if "author" in embed:
                    if not isinstance(embed["author"]["icon_url"], str):
                        attachment_id = DiscordClient.__random_attachment_id()
                        filename = str(attachment_id) + Path(embed["author"]["icon_url"][0]).suffix

                        files_data.append({
                            "id": attachment_id,
                            "stream": embed["author"]["icon_url"][1],
                            "filename": filename,
                            "content_type": guess_type(filename)[0],
                        })

                        embeds[i]["author"]["icon_url"] = f"attachment://{filename}"

            payload_json_data.update(embeds=embeds)

        if allowed_mentions:
            allowed_mentions["parse"] = [str(data) for data in allowed_mentions["parse"]]
            allowed_mentions["roles"] = [str(data) for data in allowed_mentions["roles"]]
            payload_json_data.update(allowed_mentions=allowed_mentions)

        if components:
            payload_json_data.update(components=components)

        if flags is not None:
            payload_json_data.update(flags=flags)

        if len(files_data) > 0:
            files_dict = {}
            payload_json_data.update(attachments=[])

            for file_data in files_data:
                files_dict.update({
                    f"files[{file_data['id']}]": (
                        file_data["filename"],
                        file_data["stream"],
                        file_data["content_type"],
                    )
                })
                payload_json_data["attachments"].append({
                    "id": file_data["id"],
                    "filename": file_data["filename"],
                })

            mp_encoder = MultipartEncoder(
                fields={
                    "payload_json": (
                        None,
                        json.dumps(payload_json_data, separators=(',', ':')),
                        "application/json",
                    ),
                    **files_dict,
                }
            )

            res = session.post(
                "/".join((
                    DiscordClient.__rest_api_url,
                    f"v{DiscordClient.__rest_api_version}",
                    "webhooks",
                    webhook_id,
                    webhook_token,
                )),
                data=mp_encoder,
                headers={"Content-Type": mp_encoder.content_type},
            )

        else:
            res = session.post(
                "/".join((
                    DiscordClient.__rest_api_url,
                    f"v{DiscordClient.__rest_api_version}",
                    "webhooks",
                    webhook_id,
                    webhook_token,
                )),
                json=payload_json_data,
            )

        res.raise_for_status()
        return res

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
