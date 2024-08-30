import os
import logging
import sqlite3
from telethon import TelegramClient
from datetime import datetime

# Replace these with your own values
api_id = '27715324'
api_hash = '72f0a5168ab258f7b6cb169c78ff31d6'
phone_number = '+14698380038'

# The session name (can be anything)
session_name = 'my_telegram_client'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the client and connect
client = TelegramClient(session_name, api_id, api_hash)

# Ensure the media directory exists
media_dir = 'media'
os.makedirs(media_dir, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect('telegram_messages.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT UNIQUE,
                    name TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    channel_id INTEGER,
                    sender_id INTEGER,
                    text TEXT,
                    timestamp DATETIME,
                    FOREIGN KEY(channel_id) REFERENCES channels(id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER,
                    file_path TEXT,
                    FOREIGN KEY(message_id) REFERENCES messages(id))''')

async def main():
    try:
        # Authenticate
        await client.start(phone=phone_number)
        logger.info("Successfully logged in!")

        # Define the channels to monitor
        channels_to_monitor = ['crypto_musk1', 'another_channel']

        for channel_name in channels_to_monitor:
            # Fetch the chat entity (use the chat's username or ID)
            chat = await client.get_entity(channel_name)
            channel_id = chat.id

            # Insert or update the channel in the database
            cursor.execute('''INSERT OR IGNORE INTO channels (channel_id, name)
                              VALUES (?, ?)''', (channel_id, chat.title))
            conn.commit()

            # Fetch the last 50 messages
            async for message in client.iter_messages(chat, limit=50):
                # Insert the message into the database
                cursor.execute('''INSERT INTO messages (message_id, channel_id, sender_id, text, timestamp)
                                  VALUES (?, (SELECT id FROM channels WHERE channel_id=?), ?, ?, ?)''',
                               (message.id, channel_id, message.sender_id, message.text, message.date))
                message_db_id = cursor.lastrowid
                conn.commit()

                # Download media if present
                if message.media:
                    media_path = await message.download_media(file=os.path.join(media_dir, f"{message.id}"))
                    logger.info(f"Downloaded media for message ID {message.id} to {media_path}")

                    # Insert media into the database
                    cursor.execute('''INSERT INTO media (message_id, file_path)
                                      VALUES (?, ?)''', (message_db_id, media_path))
                    conn.commit()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        conn.close()

# Run the client
with client:
    client.loop.run_until_complete(main())
