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

# Define global variables
START_TXT = """
<b>Hi {}, \nI'm Channel Forward Tag Remover bot.\n\nForward me some messages, I will remove forward tag from them.\nAlso can do it in channels.</b>
"""

START_BTN = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Add Channel', url='https://t.me/{}?startchannel=&admin=post_messages'.format(bot_username))]]
    )

# Event handler for /start command
@bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

# Event handler for forwarded messages in channels
@bot.on_message(filters.channel & filters.forwarded)
async def fwdrmv(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            new_caption = f"<b>{m.caption}</b>\n\n" if m.caption else None
            await m.copy(m.chat.id, caption=new_caption)
            await m.delete()
        else:
            await m.copy(m.chat.id)
            await m.delete()
    except FloodWait as e:
        await asyncio.sleep(e.x)

# Event handler for messages in private chats or groups
@bot.on_message(filters.private | filters.group)
async def fwdrm(c, m):
    try:
        if m.media and not (m.video_note or m.sticker):
            new_caption = f"<b>{m.caption}</b>\n\n" if m.caption else None
            await m.copy(m.chat.id, caption=new_caption)
        else:
            await m.copy(m.chat.id)
    except FloodWait as e:
        await asyncio.sleep(e.x)

# Get bot's username
async def get_bot_username():
    me = await bot.get_me()
    return me.username

# Ensure bot is started before getting username
async def main():
    await bot.start()
    global bot_username
    bot_username = await get_bot_username()
    print("Bot Username:", bot_username)
    await bot.run()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
