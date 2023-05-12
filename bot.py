import asyncio
import os
from pyrogram import Client, filters, idle

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION = os.getenv("SESSION")
TIME = int(os.getenv("TIME"))
GROUPS = [int(grp) for grp in os.getenv("GROUPS", "").split()]
ADMINS = [int(usr) for usr in os.getenv("ADMINS", "").split()]

START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"

User = Client(
    session_name=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    workers=300
)

Bot = Client(
    session_name="auto-delete",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300
)

@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(START_MSG.format(message.from_user.mention))

@User.on_message(filters.chat(GROUPS))
async def delete(user, message):
    try:
        if message.from_user.id in ADMINS:
            return
        else:
            await asyncio.sleep(TIME)
            await Bot.delete_messages(message.chat.id, message.message_id)
    except Exception as e:
        print(e)

User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
