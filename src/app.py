from typing import Optional

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageAuthorRequired, MessageIdInvalid, MessageNotModified, RPCError

from config import load_settings
from matcher import blur_text

app: Client | None = None


def _edited_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    blurred = blur_text(text)
    if blurred == text:
        return None
    return blurred


async def _edit_message(message, text: str, *, is_caption: bool) -> None:
    if app is None:
        return
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


async def blur_outgoing_text(_, message) -> None:
    text = _edited_text(message.text)
    if text:
        await _edit_message(message, text, is_caption=False)


async def blur_outgoing_caption(_, message) -> None:
    caption = _edited_text(message.caption)
    if caption:
        await _edit_message(message, caption, is_caption=True)


def _build_client() -> Client:
    settings = load_settings()
    client = Client(settings.session_name, api_id=settings.api_id, api_hash=settings.api_hash)
    client.on_message(filters.me & filters.text)(blur_outgoing_text)
    client.on_message(filters.me & filters.caption)(blur_outgoing_caption)
    return client


def run() -> None:
    global app
    app = _build_client()
    app.run()
