import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from html import escape

bot = Client(
    "Remove FwdTag",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)


START_TXT = """
<b>Hi {}, I'm Channel Forward Tag Remover bot.\n\nForward me some messages, I will remove forward tag from them.\nAlso can do it in channels.</b>
"""

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=None
    )


def get_entities(caption):
    entities = caption.entities or caption.caption_entities
    formatted_entities = []
    if entities:
        for entity in entities:
            if entity.type == "bold":
                formatted_entities.append(MessageEntity(type="bold", offset=entity.offset, length=entity.length))
            elif entity.type == "code":
                formatted_entities.append(MessageEntity(type="code", offset=entity.offset, length=entity.length))
            else:
                formatted_entities.append(MessageEntity(type="text_link", offset=entity.offset, length=entity.length))
    return formatted_entities

@bot.on_message(filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        caption = m.caption if m.caption else ""
        entities = get_entities(m)

        if m.media and not (m.video_note or m.sticker):
            await m.copy(m.chat.id, caption=caption, entities=entities)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)


'''@bot.on_message(filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            # Parse HTML tags in the caption if present
            caption = parse_html_tags(m.caption)
            await m.copy(m.chat.id, caption=caption if caption else None)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)'''


@bot.on_message(filters.private | filters.group)
async def fwdrm(c, m):
    '''try:
        if m.media and not (m.video_note or m.sticker):
            # Parse HTML tags in the caption if present
            caption = parse_html_tags(m.caption)
            await m.copy(m.chat.id, caption=caption if caption else None)
        else:
            await m.copy(m.chat.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)'''
    try:
        caption = m.caption if m.caption else ""
        entities = get_entities(m)

        if m.media and not (m.video_note or m.sticker):
            await m.copy(m.chat.id, caption=caption, entities=entities)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.value)


bot.run()
