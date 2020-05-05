from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup


REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}


def start(update, context):
    reply_keyboard = [['/number', 'phone']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


def game_numbers(update, context):
    update.message.reply_text("Хорошо. Я загадал пятизначное число; у тебя есть 5 попыток.\nЧисло: *****")


def main():
    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    game_numbers_handler = CommandHandler('number', game_numbers)

    dp.add_handler(start_handler)
    dp.add_handler(game_numbers_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
