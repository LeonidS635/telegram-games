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

used_words = []

with open('russian_nouns.txt', 'r', encoding='UTF-8') as file:
    data = file.read()
    data = data.split('\n')


def start(update, context):
    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


def game_numbers(update, context):
    #global GAME_NUMBERS
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
    global GAME_WORDS

    if GAME_NUMBERS:
        print(update.message.text)
        number_from_user = [int(j) for j in update.message.text]
        print(number_from_user)
        f = GameNumbers.number()
        answer = f.logika(number_from_user, NUMBER_FROM_BOT, update)
        if answer:
            GAME_NUMBERS = False

    if GAME_WORDS:
        flag_bot = True
        ch = 0

        word_player = update.message.text

        if word_player not in data:
            update.message.reply_text("Это не существительное или такого слова не существует")
            ch -= 1
            flag_bot = False
        else:
            if len(used_words) != 0:
                if word_player not in used_words:
                    if word_player[0] == used_words[-1][-1]:
                        used_words.append(word_player)
                        ch += 1
                        print('schet: ', ch)
                    else:
                        update.message.reply_text("Слово должно начинаться с последней буквы предыдущего слова")
                        ch -= 1
                        flag_bot = False
                else:
                    update.message.reply_text('Такое слово уже было!')
                    ch -= 1
                    flag_bot = False
            else:
                used_words.append(word_player)

        if flag_bot:
            letter = used_words[-1][-1]
            if letter == 'ъ' or letter == 'ы' or letter == 'ь':
                letter = used_words[-1][-2]
            print(letter)
            with open('russian_nouns_{}.txt'.format(letter), 'r', encoding='UTF-8') as file:
                data_letter = file.read()
                data_letter = data_letter.split('\n')

            word_bot = random.choice(data_letter)
            used_words.append(word_bot)
            update.message.reply_text(word_bot)


def main():
    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    game_numbers_handler = CommandHandler('number', game_numbers)
    game_words_handler = CommandHandler('words', game_words)
    answer_handler = MessageHandler(Filters.text, answer)

    dp.add_handler(start_handler)
    dp.add_handler(game_numbers_handler)
    dp.add_handler(game_words_handler)
    dp.add_handler(answer_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
