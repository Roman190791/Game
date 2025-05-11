from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from functions import load_data, save_data, get_balance, set_balance
from config import TOKEN

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    data = load_data()
    user_id = user.id
    balance = get_balance(user_id, data)
    
    update.message.reply_text(
        f"Привіт, {user.first_name}! Твій баланс: {balance} Lumis Coin.\n"
        "Готовий майнити? Натискай кнопку нижче!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Майнити", callback_data='mine')]
        ])
    )

def mine(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    data = load_data()
    balance = get_balance(user_id, data)
    new_balance = balance + 1
    set_balance(user_id, new_balance, data)
    
    query.edit_message_text(
        f"Ти здобув 1 Lumis Coin!\n"
        f"Новий баланс: {new_balance} Lumis Coin.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Майнити", callback_data='mine')]
        ])
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(mine, pattern='^mine$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
