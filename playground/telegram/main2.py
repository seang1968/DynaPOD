import os
import logging
from telethon import TelegramClient

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

# Text file to persist messages
messages_file = 'messages.txt'

async def main():
    try:
        # Authenticate
        await client.start(phone=phone_number)
        logger.info("Successfully logged in!")

        # Fetch the chat entity (use the chat's username or ID)
        chat = await client.get_entity('crypto_musk1')  # Replace with your target chat

        # Fetch the last 50 messages
        async for message in client.iter_messages(chat, limit=50):
            # Print the message
            print(f"Message ID: {message.id}, Sender: {message.sender_id}, Text: {message.text}")

            # Save the message text to a file
            with open(messages_file, 'a', encoding='utf-8') as f:
                f.write(f"Message ID: {message.id}\nSender: {message.sender_id}\nText: {message.text}\n\n")

            # Download media if present
            if message.media:
                media_path = await message.download_media(file=os.path.join(media_dir, f"{message.id}"))
                logger.info(f"Downloaded media for message ID {message.id} to {media_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Run the client
with client:
    client.loop.run_until_complete(main())
