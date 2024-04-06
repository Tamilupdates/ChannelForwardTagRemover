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

BOT_USERNAME = os.environ["BOT_USERNAME"]

START_TXT = """
<b>Hi {}, \nI'm Channel Forward Tag Remover bot.\n\nForward me some messages, I will remove forward tag from them.\nAlso can do it in channels.</b>
"""

START_BTN = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Add Channel', url='https://t.me/{}?startchannel=&admin=post_messages'.format(BOT_USERNAME))]]
)

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

async def delete_message(c, m):
    try:
        await bot.delete_messages(chat_id=c, message_ids=m)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await delete_message(c, m)
    except Exception as e:
        print(f"Error deleting message: {e}")

@bot.on_message(filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            new_caption = f"<b>{m.caption}</b>\n\n" if m.caption else None
            new_message = await m.copy(m.chat.id, caption=new_caption)
            await delete_message(m.chat.id, m.message_id)
        else:
            new_message = await m.copy(m.chat.id)
            await delete_message(m.chat.id, m.message_id)
    except Exception as e:
        print(f"Error processing message: {e}")

@bot.on_message(filters.private | filters.group)
async def fwdrm(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            new_caption = f"<b>{m.caption}</b>\n\n" if m.caption else None
            await m.copy(m.chat.id, caption=new_caption)
        else:
            await m.copy(m.chat.id)
    except Exception as e:
        print(f"Error processing message: {e}")

bot.run()


