from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import GameNumbers
import time


REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}
global GAME_NUMBERS
global GAME_WORDS
GAME_NUMBERS = False
GAME_WORDS = False

used_words = []
start_time = 0
chance = 0

with open('russian_nouns.txt', 'r', encoding='UTF-8') as file:
    data = file.read()
    data = data.split('\n')


def start(update, context):
    global GAME_NUMBERS
    global GAME_WORDS

    GAME_NUMBERS = False
    GAME_WORDS = False

    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


def games(update, context):
    global GAME_NUMBERS
    global GAME_WORDS

    GAME_NUMBERS = False
    GAME_WORDS = False

    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("Выбери игру, в которую хочешь поиграть", reply_markup=markup)


def game_numbers(update, context):
    global GAME_NUMBERS
    global NUMBER_FROM_BOT
    GAME_NUMBERS = True

    global chance
    chance = 14

    update.message.reply_text("Хорошо. Я загадал четырёхзначное число. У тебя есть 15 попыток. "
                              "Попробуй угадать)\nЧисло: ****", reply_markup=ReplyKeyboardRemove())

    dataset_numbers = [i for i in range(10)]
    NUMBER_FROM_BOT = [random.choice(dataset_numbers) for _ in range(4)]

    # print(NUMBER_FROM_BOT)


def game_words(update, context):
    global GAME_WORDS
    GAME_WORDS = True

    global used_words
    used_words = []

    global start_time
    start_time = time.time() + 5

    update.message.reply_text("Хорошо. Давай поиграем в слова. На слово у тебя есть 15 секунд. Начинай.",
                              reply_markup=ReplyKeyboardRemove())


def help(update, context):
    if GAME_NUMBERS:
        update.message.reply_text("Напиши боту число, и он скажет, какие цифры правильные")
    elif GAME_WORDS:
        update.message.reply_text("Слово должно начинаться с последней буквы предыдущего слова и помни, "
                                  "что на ход у тебя есть 15 секунд")
    else:
        update.message.reply_text("Это бот мини игр. Выбери, в какую хочешь сыграть('/games'): угадай число или слова")


def answer(update, context):
    global GAME_NUMBERS
    global GAME_WORDS

    if GAME_NUMBERS:
        global chance

        if chance == 0:
            GAME_NUMBERS = False
            update.message.reply_text("Число так и не разгадано. Это моя тайна)")
        else:
            number_from_user = [int(j) for j in update.message.text]
            f = GameNumbers.number()
            answer = f.logika(number_from_user, NUMBER_FROM_BOT, update, chance)
            if answer:
                GAME_NUMBERS = False
            else:
                chance -= 1

    if GAME_WORDS:
        flag_bot = True
        global start_time

        word_player = update.message.text.lower()

        if word_player not in data:
            update.message.reply_text("Это не существительное или такого слова не существует")
            flag_bot = False
        else:
            if len(used_words) != 0:
                if word_player not in used_words:
                    letter = used_words[-1][-1]
                    if letter == 'ъ' or letter == 'ы' or letter == 'ь':
                        letter = used_words[-1][-2]

                    if word_player[0] == letter:
                        used_words.append(word_player)
                    else:
                        update.message.reply_text(
                            "Слово должно начинаться с последней буквы предыдущего слова: '{}'".format(letter))
                        flag_bot = False
                        start_time += 2
                else:
                    update.message.reply_text('Такое слово уже было!')
                    flag_bot = False
                    start_time += 2
            else:
                used_words.append(word_player)

        if flag_bot:
            word = True

            if time.time() - start_time > 15:
                update.message.reply_text('Время вышло!')
                GAME_WORDS = False
                word = False

            start_time = time.time()

            letter = used_words[-1][-1]
            if letter == 'ъ' or letter == 'ы' or letter == 'ь':
                letter = used_words[-1][-2]

            with open('russian_nouns_{}.txt'.format(letter), 'r', encoding='UTF-8') as file:
                data_letter = file.read()
                data_letter = data_letter.split('\n')

            while word:
                word_bot = random.choice(data_letter)

                if set(data_letter).issubset(used_words):
                    update.message.reply_text('Ну ладно, сдаюсь!')
                    GAME_WORDS = False
                    word = False

                if word_bot not in used_words:
                    used_words.append(word_bot)
                    update.message.reply_text(word_bot)
                    word = False


def main():
    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    games_handler = CommandHandler('games', games)
    help_handler = CommandHandler('help', help)
    game_numbers_handler = CommandHandler('number', game_numbers)
    game_words_handler = CommandHandler('words', game_words)
    answer_handler = MessageHandler(Filters.text, answer)

    dp.add_handler(start_handler)
    dp.add_handler(games_handler)
    dp.add_handler(help_handler)
    dp.add_handler(game_numbers_handler)
    dp.add_handler(game_words_handler)
    dp.add_handler(answer_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
