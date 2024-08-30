from telethon import TelegramClient
import logging
import os

# Replace these with your own values
api_id = '27715324'
api_hash = '72f0a5168ab258f7b6cb169c78ff31d6'
phone_number = '+14698380038'

# The session name (can be anything)
session_name = 'my_telegram_client'
last_message_file = 'last_message_id.txt'

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the client and connect
client = TelegramClient(session_name, api_id, api_hash)

async def main():
    try:
        # Authenticate
        await client.start(phone=phone_number)
        logger.info("Successfully logged in!")

        # Fetch the chat entity
        chat = await client.get_entity('crypto_musk1')  # Use the chat's username or ID
        logger.info(f"Found chat: {chat.title}")

        # Get the last processed message ID
        last_message_id = 0
        if os.path.exists(last_message_file):
            with open(last_message_file, 'r') as f:
                last_message_id = int(f.read().strip())
        
        logger.info(f"Starting from message ID: {last_message_id}")

        # Fetch messages from the chat, starting from the last message ID
        async for message in client.iter_messages(chat, min_id=last_message_id, reverse=True):  # Adjust limit as needed
            print(message.sender_id, message.text)

            # Save the message ID
            with open(last_message_file, 'w') as f:
                f.write(str(message.id))

            # Save messages to a file (ensure encoding is UTF-8)
            with open('messages.txt', 'a', encoding='utf-8') as f:
                f.write(f"{message.sender_id}: {message.text}\n")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Run the client
with client:
    client.loop.run_until_complete(main())
