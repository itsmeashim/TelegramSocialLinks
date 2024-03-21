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
import tldextract
from urlextract import URLExtract

extractor = URLExtract()

logging.basicConfig(level=logging.INFO)

load_dotenv()

GROUP_ID = os.getenv("GROUP_ID")
try:
    GROUP_ID = int(GROUP_ID)
except Exception as e:
    send_exception_to_discord(e, webhook_url)
    print(e)
webhook_url = os.getenv("WEBHOOK_URL")

monitored_usernames = ["DRBTSolana", "osiuf238jofaidjfoisd"]  # Updated monitored usernames

session_string = os.getenv("TG_SESSION")
# User Client
app = Client("my_account", session_string=session_string)

@app.on_message(filters.chat(monitored_usernames))
async def check_message(client, message):
    try:
        logging.info(f"New Message")

        message_text = message.text
        message_caption = message.caption
        message_caption_entities = message.caption_entities
        entities_url = ""
        if message_caption_entities:
            for entities in message_caption_entities:
                if entities.type == MessageEntityType.TEXT_LINK:
                    if "solscan.io" not  in entities.url:
                        entities_url += entities.url + "  "
                    print(entities_url)

        message_caption_entities = entities_url
        logging.info(f"entities_url: {message_caption_entities}")

        message_1 = str(message_text) + "  " + str(message_caption) + " " + str(message_caption_entities)

        message_text_lower = message_1.lower().replace("\n", " ").replace(",", " ").replace("]", " ").replace("[", " ").replace("(", " ").replace(")", " ").replace('"', ' ').replace("'", " ")

        print(f"Message: {message_text_lower}")

        extractor.find_urls
        urls = extractor.find_urls(message_text_lower, only_unique=True)
        print(f"URLs: {urls}")
        logging.info(f"URLs: {urls}")

        # Domains to filter out
        filter_domains = ["twitter.com", "x.com", "discord.gg", "t.me", "instagram.com", "facebook.com", "reddit.com", "youtube.com", "tiktok.com","binance.com", "opensea.io", "rarible.com", "solsea.io", "solible.com", "solible.io", "wikipedia.com", "solscan.io", "birdeye.so", "dexscreener.com", "rugcheck.xyz", "tinyastro.io", "www.instagram.com", "medium.com", "wikipedia.org"]

        # Extracting hostnames and filtering

        urls = [tldextract.extract(url.strip('[').strip(']')).registered_domain for url in urls]

        try:
            filtered_urls = [url for url in urls if url not in filter_domains]
        except Exception as e:
            print(e)
            logging.warning(f"Error filtering URLs: {e}")
            filtered_urls = []

        logging.info(f"Filtered URLs: {filtered_urls}")
        print(f"Filtered URLs: {filtered_urls}")

        if filtered_urls:
            await message.forward(GROUP_ID)

    except Exception as e:
        send_exception_to_discord(e, webhook_url)

try:
    app.run()
except Exception as e:
    send_exception_to_discord(e, webhook_url)
    print(e)