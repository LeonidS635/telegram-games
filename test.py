from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import GameNumbers
import time


REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}

global id
id = {}


class User():
    def __init__(self):
        self.GAME_NUMBERS = False
        self.GAME_WORDS = False
        self.used_words = []
        self.start_time = 0
        self.chance = 0
        self.functions = {}

        with open('russian_nouns.txt', 'r', encoding='UTF-8') as file:
            self.data = file.read()
            self.data = self.data.split('\n')

    def games(self, update, context):
        id[update.message.chat_id]['GAME_NUMBERS'] = False
        id[update.message.chat_id]['GAME_WORDS'] = False

        reply_keyboard = [['/number', '/words']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text("Выбери игру, в которую хочешь поиграть", reply_markup=markup)

    def game_numbers(self, update, context):
        update.message.reply_text("Хорошо. Я загадал четырёхзначное число. У тебя есть 15 попыток. "
                                  "Попробуй угадать)\nЧисло: ****", reply_markup=ReplyKeyboardRemove())

        dataset_numbers = [i for i in range(10)]
        number_from_bot = [random.choice(dataset_numbers) for _ in range(4)]

        id[update.message.chat_id]['NUMBER'] = number_from_bot
        id[update.message.chat_id]['GAME_NUMBERS'] = True
        id[update.message.chat_id]['chance'] = 4

        print(id)

    def game_words(self, update, context):
        id[update.message.chat_id]['GAME_WORDS'] = True
        id[update.message.chat_id]['used_words'] = []

        self.start_time = time.time() + 5

        update.message.reply_text("Хорошо. Давай поиграем в слова. На слово у тебя есть 15 секунд. Начинай.",
                                  reply_markup=ReplyKeyboardRemove())

    def help(self, update, context):
        if id[update.message.chat_id]['GAME_NUMBERS']:
            update.message.reply_text("Напиши боту число, и он скажет, какие цифры правильные")
        elif id[update.message.chat_id]['GAME_WORDS']:
            update.message.reply_text("Слово должно начинаться с последней буквы предыдущего слова и помни, "
                                      "что на ход у тебя есть 15 секунд")
        else:
            update.message.reply_text(
                "Это бот мини игр. Выбери, в какую хочешь сыграть('/games'): угадай число или слова")

    def answer(self, update, context):
        chat_id = update.message.chat_id

        if id[chat_id]['GAME_NUMBERS']:
            if id[chat_id]['chance'] == 0:
                id[chat_id]['GAME_NUMBERS'] = False
                context.bot.send_message(chat_id=chat_id, text="Число так и не разгадано. Это моя тайна)")
            else:
                number_from_user_str = update.message.text

                if not number_from_user_str.isdigit():
                    context.bot.send_message(chat_id=chat_id, text='Это не число')
                elif len(number_from_user_str) < 4 or len(number_from_user_str) > 4:
                    context.bot.send_message(chat_id=chat_id, text='Введи четырёхзначное число')
                else:
                    number_from_user = [int(j) for j in update.message.text]
                    f = GameNumbers.number()
                    answer = f.logika(number_from_user, id[chat_id]['NUMBER'], context, id[chat_id]['chance'], chat_id)
                    if answer:
                        id[chat_id]['GAME_NUMBERS'] = False
                    else:
                        id[chat_id]['chance'] -= 1

        if id[chat_id]['GAME_WORDS']:
            flag_bot = True

            word_player = update.message.text.lower()

            if word_player not in self.data:
                context.bot.send_message(chat_id=chat_id, text="Это не существительное или такого слова не существует")
                flag_bot = False
            else:
                if len(id[chat_id]['used_words']) != 0:
                    if word_player not in id[chat_id]['used_words']:
                        letter = id[chat_id]['used_words'][-1][-1]

                        if letter == 'ъ' or letter == 'ы' or letter == 'ь':
                            letter = id[chat_id]['used_words'][-1][-2]

                        if word_player[0] == letter:
                            id[chat_id]['used_words'].append(word_player)
                        else:
                            context.bot.send_message(chat_id=chat_id, text="Слово должно начинаться с последней буквы "
                                                                           "предыдущего слова: '{}'".format(letter))
                            flag_bot = False
                            self.start_time += 2
                    else:
                        context.bot.send_message(chat_id=chat_id, text='Такое слово уже было!')

                        flag_bot = False
                        self.start_time += 2
                else:
                    id[chat_id]['used_words'].append(word_player)

            if flag_bot:
                word = True

                if time.time() - self.start_time > 60:
                    context.bot.send_message(chat_id=chat_id, text='Время вышло!')
                    id[chat_id]['GAME_WORDS'] = False
                    word = False

                self.start_time = time.time()

                letter = id[chat_id]['used_words'][-1][-1]
                if letter == 'ъ' or letter == 'ы' or letter == 'ь':
                    letter = id[chat_id]['used_words'][-1][-2]

                with open('russian_nouns_{}.txt'.format(letter), 'r', encoding='UTF-8') as file:
                    data_letter = file.read()
                    data_letter = data_letter.split('\n')

                while word:
                    word_bot = random.choice(data_letter)

                    if set(data_letter).issubset(id[chat_id]['used_words']):
                        context.bot.send_message(chat_id=chat_id, text='Ну ладно, сдаюсь!')
                        id[chat_id]['GAME_WORDS'] = False
                        word = False

                    if word_bot not in self.used_words:
                        id[chat_id]['used_words'].append(word_bot)
                        context.bot.send_message(chat_id=chat_id, text=word_bot)
                        word = False
        print(id)


def start(update, context):
    id[update.message.chat_id] = {}
    id[update.message.chat_id]['GAME_NUMBERS'] = False
    id[update.message.chat_id]['GAME_WORDS'] = False

    User()
    print(update.message.chat_id)
    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я бот мини-игр. Выбери, в какую игру хочешь сыграть: угадай число - '/number'\nслова - '/words'",
        reply_markup=markup)


def main():
    user = User()

    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    dp.add_handler(start_handler)

    games_handler = CommandHandler('games', user.games)
    help_handler = CommandHandler('help', user.help)
    game_numbers_handler = CommandHandler('number', user.game_numbers)
    game_words_handler = CommandHandler('words', user.game_words)
    answer_handler = MessageHandler(Filters.text, user.answer)

    dp.add_handler(games_handler)
    dp.add_handler(help_handler)
    dp.add_handler(game_numbers_handler)
    dp.add_handler(game_words_handler)
    dp.add_handler(answer_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
