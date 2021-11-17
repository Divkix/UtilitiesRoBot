from pyrogram.types import Message

from .. import app
from ..utils.getBinInfo import getBinInfo
from ..utils.joinCheck import join


@app.command("bin", pm_only=True)
@join
async def binChecker(_, m: Message):
    msg = await m.reply_text("...")
    if len(m.text.split()) == 1:
        return await msg.edit_text("Please type a bin after the command.")
    CCBin = m.text.split(None, 1)[1]
    await msg.edit_text(await getBinInfo(CCBin))
