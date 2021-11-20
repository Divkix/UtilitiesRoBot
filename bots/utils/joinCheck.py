from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bots import JoinChannel, JoinCheck, SupportGroup


def joinCheck():
    def wrapper(func):
        async def decorator(client, message):
            if not JoinCheck:
                return await func(client, message)
            if message.sender_chat:
                return
            try:
                get = await client.get_chat_member(JoinChannel, message.from_user.id)
            except UserNotParticipant:
                return await message.reply_text(
                    f"You need to Join {JoinChannel} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{JoinChannel.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            if get.status in ("restricted", "kicked"):
                return await message.reply_text(
                    f"You were banned from using me. If you think this is a mistake then report this at {SupportGroup}",
                )
            if not get.status in ("creator", "administrator", "member"):
                return await message.reply_text(
                    f"You need to Join {JoinChannel} to use me.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Join Channel",
                                    url=f"https://t.me/{JoinChannel.replace('@', '')}",
                                ),
                            ],
                        ],
                    ),
                )
            return await func(client, message)

        return decorator

    return wrapper