from pyrogram.types import Message

from bots import MODULES, app
from bots.utils.genFakeInfo import genFakeInfo
from bots.utils.joinCheck import joinCheck
from bots.vars import Vars

MODULES.update(
    {
        "fakeInfo": {
            "info": "To generate a fake user Details, If not gender is specified then a random user data.",
            "usage": "/geninfo [optional: gender]",
        },
    },
)


@app.command("geninfo")
@joinCheck()
async def genInfo(_, m: Message):
    gender = None
    msg = await m.reply_text("...")
    if len(m.command) == 2:
        if m.command[1].lower() in ("male", "female"):
            gender = m.command[1]
            chkUrl += f"?gender={gender}"
            text = f"Generating a Fake {m.command[1]} user data."
        else:
            text = "Generating a Fake user data."
    else:
        text = "Generating a Fake user data."
    await msg.edit_text(text)
    chkUrl = "https://randomuser.me/api/1.3/"
    infoText, userPic = await genFakeInfo(chkUrl)
    if infoText == "API Unreachable":
        return await msg.edit_text(
            "API Unreachable at the Moment, Try again Later"
        )
    if not (infoText or userPic):
        return await msg.edit_text(
            f"error generating fake data{': gender ' if gender else ''} \nReport this at {Vars.SUPPORT_GROUP}",
        )

    await m.reply_document(userPic, caption=infoText)
    await msg.delete()
