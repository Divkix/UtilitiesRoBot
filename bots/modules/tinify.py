from os import remove

from pyrogram.types import Message

from bots import DownPath, app
from bots.utils.compressImage import compress_image
from bots.utils.joinCheck import joinCheck


@app.command("tinify", pm_only=True)
@joinCheck()
async def tinify(c, m: Message):
    try:
        if m.reply_to_message.photo or (
            m.reply_to_message.document
            and m.reply_to_message.document.mime_type.startswith("image/")
        ):
            rmsg = await m.reply_text("Compressing photo...")
            exact_file = await c.download_media(
                message=m.reply_to_message,
                file_name=f"{DownPath}/{m.from_user.id}/",
            )
            new_filename = await compress_image(exact_file)
            await m.reply_document(
                new_filename,
                caption="Compressed image.",
            )
            await rmsg.delete()
            remove(new_filename)
            remove(exact_file)
        else:
            await m.reply_text("Reply to a photo or a document.")
    except AttributeError:
        pass

    return