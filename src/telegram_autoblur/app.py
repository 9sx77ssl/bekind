import os
from typing import Optional

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageAuthorRequired, MessageIdInvalid, MessageNotModified, RPCError

from telegram_autoblur.matcher import blur_text


API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION_NAME = os.environ.get("TG_SESSION_NAME", "mat-autoblur")

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


def _edited_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    blurred = blur_text(text)
    if blurred == text:
        return None
    return blurred


async def _edit_message(message, text: str, *, is_caption: bool) -> None:
    try:
        if is_caption:
            await message.edit_caption(text)
        else:
            await message.edit_text(text)
    except MessageNotModified:
        return
    except (MessageAuthorRequired, MessageIdInvalid):
        return
    except FloodWait as wait:
        await app.sleep(wait.value)
        try:
            if is_caption:
                await message.edit_caption(text)
            else:
                await message.edit_text(text)
        except RPCError:
            return
    except RPCError:
        return


@app.on_message(filters.me & filters.text)
async def blur_outgoing_text(_, message) -> None:
    text = _edited_text(message.text)
    if text:
        await _edit_message(message, text, is_caption=False)


@app.on_message(filters.me & filters.caption)
async def blur_outgoing_caption(_, message) -> None:
    caption = _edited_text(message.caption)
    if caption:
        await _edit_message(message, caption, is_caption=True)


def run() -> None:
    app.run()
