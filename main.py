from pyrogram import Client, filters, compose
from pyrogram.enums import MessageEntityType
from ownserver_logger import *
import uuid
import asyncio
import re
import logging
import os
from dotenv import load_dotenv
from ownserver_logger import send_exception_to_discord, send_message_to_discord
from urllib.parse import urlparse

load_dotenv()

GROUP_ID = os.getenv("GROUP_ID")
webhook_url = os.getenv("WEBHOOK_URL")

monitored_usernames = ["DRBTSolana", "osiuf238jofaidjfoisd"]  # Updated monitored usernames

session_string = os.getenv("TG_SESSION")
# User Client
app = Client("my_account", session_string=session_string)

@app.on_message(filters.channel | filters.chat(monitored_usernames))
async def check_message(client, message):
    try:

        message_text = message.text
        message_caption = message.caption
        message_caption_entities = message.caption_entities
        message_caption_entities = str(message_caption_entities)

        message_1 = str(message_text) + str(message_caption) + str(message_caption_entities)

        message_text_lower = message_1.lower().replace("\n", " ").replace(",", " ")  # Replace commas and periods with spaces

        urls = re.findall(r'http[s]?://[^\s)\]]+', message_text_lower)
        print(f"URLs: {urls}")
        logging.info(f"URLs: {urls}")

        # Domains to filter out
        filter_domains = ["twitter.com", "x.com", "discord.gg", "t.me", "instagram.com", "facebook.com", "reddit.com", "youtube.com", "tiktok.com","binance.com", "opensea.io", "rarible.com", "solsea.io", "solible.com", "solible.io", "wikipedia.com", "solscan.io", "birdeye.so", "dexscreener.com", "rugcheck.xyz", "tinyastro.io"]

        # Extracting hostnames and filtering

        filtered_urls = [urlparse(url).hostname for url in urls if urlparse(url).hostname not in filter_domains]
        logging.info(f"Filtered URLs: {filtered_urls}")

        if filtered_urls:
            await message.forward(GROUP_ID)

    except Exception as e:
        send_exception_to_discord(e, webhook_url)

try:
    app.run()
except Exception as e:
    send_exception_to_discord(e, webhook_url)
    print(e)