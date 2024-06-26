from html import escape
from os import remove

from kantex.html import Code
from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.joinCheck import joinCheck

MODULES.update(
    {
        "json": {
            "info": "To get the json data of the message.",
            "usage": "/json [optional: reply]",
        },
    },
)


@app.command("json", pm_only=False)
@joinCheck()
async def json(_, m: Message):
    ms = m.reply_to_message or m
    if len(str(ms)) > 4020:
        filen = f"json_{m.chat.id}_{m.id}.json"
        with open(filen, "w+") as _file:
            _file.write(str(ms).strip())
        await m.reply_document(filen)
        remove(filen)
        return
    await m.reply_text(Code(escape(str(ms))))
