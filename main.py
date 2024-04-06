import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

bot = Client(
    "Remove FwdTag",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

START_TXT = """
<b>Hi {}, \nI'm Channel Forward Tag Remover bot.\n\nForward me some messages, I will remove forward tag from them.\nAlso can do it in channels.</b>
"""

@bot.on_message(filters.command(["start"]))
async def start_command(bot, update):
    bot_name = (await bot.get_me()).username
    text = START_TXT.format(update.from_user.mention)
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Add Channel', url=f'https://t.me/{bot_name}?startchannel=&admin=post_messages+edit_messages+delete_messages')]]
    )
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@bot.on_message(filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            await m.copy(m.chat.id, caption=m.caption if m.caption else None, parse_mode='HTML')
            await m.delete()
        else:
            await m.copy(m.chat.id, parse_mode='HTML')
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)

@bot.on_message(filters.private | filters.group)
async def fwdrm(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            await m.copy(m.chat.id, caption=m.caption if m.caption else None, parse_mode='HTML')
        else:
            await m.copy(m.chat.id, parse_mode='HTML')
    except FloodWait as e:
        await asyncio.sleep(e.x)

bot.run()
