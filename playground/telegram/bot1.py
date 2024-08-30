from telegram.ext import Updater, CommandHandler, MessageHandler, filters

# Replace 'YOUR_API_TOKEN' with the token you got from BotFather
TOKEN = '6620355924:AAHufzTyzCbgzjECFiEtNha53f4ACw_v1pM'

def start(update, context):
    update.message.reply_text('Hello! I am your alert bot.')

def handle_message(update, context):
    text = update.message.text
    # Here you can define your criteria and what the bot should do
    if 'urgent' in text.lower():
        # Add custom logic here, such as sending an SMS, or triggering a special alert
        update.message.reply_text('This is an urgent message!')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
