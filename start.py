from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
import GameNumbers
import time

REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}

with open('russian_nouns.txt', 'r', encoding='UTF-8') as file:
    data = file.read()
    data = data.split('\n')


def main():
    global GAME_NUMBERS
    global GAME_WORDS
    global used_words
    global start_time
    global chance

    GAME_NUMBERS = False
    GAME_WORDS = False
    used_words = []
    start_time = 0
    chance = 0

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

    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True))

    updater.start_polling()

    updater.idle()


def start(update, context):
    global GAME_NUMBERS
    global GAME_WORDS

    GAME_NUMBERS = False
    GAME_WORDS = False

    reply_keyboard = [['/number', '/words']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я бот мини-игр. Выбери, в какую игру хочешь сыграть: угадай число - '/number'\nслова - '/words'",
        reply_markup=markup)


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

    print(NUMBER_FROM_BOT)


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
            number_from_user_str = update.message.text

            if not number_from_user_str.isdigit():
                update.message.reply_text('Это не число')
            elif len(number_from_user_str) < 4 or len(number_from_user_str) > 4:
                update.message.reply_text('Введи четырёхзначное число')
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

        flag_word_player = False

        while not flag_word_player:
            print(len(used_words))
            word_player = update.message.text.lower()
            if len(used_words) == 1 or word_player != used_words[-2]:
                flag_word_player = True
            if time.time() - start_time > 30:
                update.message.reply_text('Время вышло!')
                GAME_WORDS = False
                flag_word_player = True
                word = False

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

            #if time.time() - start_time > 30:
             #   update.message.reply_text('Время вышло!')
              #  GAME_WORDS = False
               # word = False

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

def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')

def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента (секунды таймера)
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        # Запоминаем созданную задачу в данных чата.
        context.chat_data['job'] = new_job
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(f'Вернусь через {due} секунд')

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')

def unset_timer(update, context):
    # Проверяем, что задача ставилась
    if 'job' not in context.chat_data:
        update.message.reply_text('Нет активного таймера')
        return
    job = context.chat_data['job']
    # планируем удаление задачи (выполнится, когда будет возможность)
    job.schedule_removal()
    # и очищаем пользовательские данные
    del context.chat_data['job']
    update.message.reply_text('Хорошо, вернулся сейчас!')

# update.message.send_text('test message')
if __name__ == '__main__':
    main()
