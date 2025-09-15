# (c) @RoyalKrrishna

# from os import link   # <-- comment out to avoid ImportError
from telethon import Button
from configs import Config
from pyrogram import Client, idle
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from plugins.tgraph import *
from helpers import *
from telethon import TelegramClient, events
import urllib.parse
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
import re

tbot = TelegramClient('mdisktelethonbot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)
client = TelegramClient(StringSession(Config.USER_SESSION_STRING), Config.API_ID, Config.API_HASH)


async def get_user_join(id):
    if Config.FORCE_SUB == "False":
        return True
    ok = True
    try:
        await tbot(GetParticipantRequest(channel=int(Config.UPDATES_CHANNEL), participant=id))
        ok = True
    except UserNotParticipantError:
        ok = False
    return ok


async def process_args(args):
    answer = ""
    async for i in AsyncIter(re.sub(r"__|\*", "", args).split()):
        if len(i) > 2:
            f_text = re.sub(r"__|\*", "", i)
            f_text = await link_to_hyperlink(f_text)
            answer += f'\n\n{f_text}'
    return answer


@tbot.on(events.NewMessage(incoming=True))
async def message_handler(event):
    try:
        if event.message.post:
            return
        if event.text.startswith("/"): 
            return

        print("\nMessage Received: " + event.text)

        # Force Subscription
        if not await get_user_join(event.sender_id):
            haha = await event.reply(
                f'''**Hey! {event.sender.first_name} 😃**

**You Have To Join Our Update Channel To Use Me ✅**

**Click Below Button To Join Now.👇🏻**''',
                buttons=Button.url('🍿Updates Channel🍿', f'https://t.me/{Config.UPDATES_CHANNEL_USERNAME}'))
            await asyncio.sleep(Config.AUTO_DELETE_TIME)
            return await haha.delete()

        args = event.text
        args = await validate_q(args)

        print(f"Search Query: {args}\n")

        if nlinrgs:
            return

        txt = await event.reply(f'**Searching For "{event.text}" 🔍**')

        search = []
        if event.is_group or event.is_channel:
            group_info = await db.get_group(str(event.chat_id).replace("-100", ""))
            if group_info["has_access"] and group_info["db_channel"] and await db.is_group_verified(str(event.chat_id).replace("-100", "")):
                CHANNEL_ID = group_info["db_channel"]
            else:
                CHANNEL_ID = Config.CHANNEL_ID
        else:
            CHANNEL_ID = Config.CHANNEL_ID

        # Process search queries using the fixed async function
        answer_text = await process_args(args)

        username = Config.UPDATES_CHANNEL_USERNAME
        answer = f'**Join** [@{username}](https://telegram.me/{username}) \n\n' + answer_text

        # Handle final search results, buttons, etc. as needed
        # ...

    except Exception as e:
        print(f"Error in message_handler: {e}")
