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

# Lambda function to replace words in the caption and make them bold
def replace_words(caption, replacements):
    for old_word, new_word in replacements.items():
        caption = caption.replace(old_word, f"<b>{new_word}</b>")
    return caption

# Load replacement from environment variable
replacements = {}
for key in os.environ:
    if key.startswith("RNAME"):
        old_word, new_word = os.environ[key].split(":")
        replacements[old_word] = new_word

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
            new_caption = replace_words(m.caption, replacements)
            await m.copy(m.chat.id, caption=new_caption)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)

@bot.on_message(filters.private | filters.group)
async def fwdrm(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            new_caption = replace_words(m.caption, replacements)
            await m.copy(m.chat.id, caption=new_caption)
        else:
            await m.copy(m.chat.id)
    except FloodWait as e:
        await asyncio.sleep(e.x)

bot.run()
