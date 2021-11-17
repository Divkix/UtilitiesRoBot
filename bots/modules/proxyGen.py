from io import BytesIO

from proxygrab import get_proxy
from tgEasy import array_chunk, ikb

from .. import app
from ..utils.joinCheck import joinCheck

proxytypes = {"HTTP", "HTTPS", "Socks4", "Socks5"}


@app.command("proxy", pm_only=True)
@joinCheck
async def getProxy(_, m):
    msg = await m.reply_text("...", quote=True)
    await msg.edit_text(
        "Choose the Proxy Type you Want.",
        reply_markup=ikb(await gen_proxy_kb()),
    )


@app.callback("getProxy")
async def getProxy(client, cb):
    ptype = cb.data.split(".")[1].lower()
    await cb.message.edit_text(f"Fetching {ptype} Proxies...")
    proxies_source = await get_proxy(ptype)
    proxies_fetched = "\n".join(proxies_source)
    caption = f"<b><i>Proxies scrapped by:</i></b> @{(await client.get_me()).username}\n\nIf you'd like to keep this service alive 😊, please /donate"
    with BytesIO(str.encode(proxies_fetched)) as output:
        output.name = f"{ptype}_{(await client.get_me()).username}.txt"
        await cb.message.reply_document(document=output, caption=caption)
    await cb.message.delete()
    await cb.answer("Done ✅", show_alert=True)


async def gen_proxy_kb():
    cmds = [i for i in proxytypes]
    kb = [(cmd, f"getProxy.{cmd}") for cmd in cmds]
    return array_chunk(kb, 2)
