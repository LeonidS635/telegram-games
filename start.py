from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import random
import GameNumbers


REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}
global GAME_NUMBERS
global GAME_WORDS
GAME_NUMBERS = False
GAME_WORDS = False


def start(update, context):
    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


def game_numbers(update, context):
    global GAME_NUMBERS
    global NUMBER_FROM_BOT
    GAME_NUMBERS = True

    update.message.reply_text("Хорошо. Я загадал пятизначное число; у тебя есть 5 попыток.\nЧисло: *****")

    dataset_numbers = [i for i in range(10)]
    NUMBER_FROM_BOT = [random.choice(dataset_numbers) for _ in range(4)]

    print(NUMBER_FROM_BOT)


def game_words(update, context):
    global GAME_WORDS
    GAME_WORDS = True

    update.message.reply_text("Хорошо. Давай поиграем в слова. Начинай.")


def answer(update, context):
    global GAME_NUMBERS
    if GAME_NUMBERS:
        print(update.message.text)
        number_from_user = [int(j) for j in update.message.text]
        print(number_from_user)
        f = GameNumbers.number()
        f.logika(number_from_user, NUMBER_FROM_BOT, update)


def main():
    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    game_numbers_handler = CommandHandler('number', game_numbers)
    game_words_handler = CommandHandler('words', game_numbers)
    answer_handler = MessageHandler(Filters.text, answer)

    dp.add_handler(start_handler)
    dp.add_handler(game_numbers_handler)
    dp.add_handler(game_words_handler)
    dp.add_handler(answer_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
