from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import random


REQUEST_KWARGS = {'proxy_url': 'socks5://80.248.225.58:31431'}
global GAME_NUMBERS
GAME_NUMBERS = False


def start(update, context):
    reply_keyboard = [['/number', 'phone']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!", reply_markup=markup)


def game_numbers(update, context):
    global GAME_NUMBERS
    GAME_NUMBERS = True

    update.message.reply_text("Хорошо. Я загадал пятизначное число; у тебя есть 5 попыток.\nЧисло: *****")

    dataset_numbers = [i for i in range(10)]
    number_from_bot = [random.choice(dataset_numbers) for _ in range(4)]
    check = True
    print(number_from_bot)

    answer(check, number_from_bot)


def logika(update, number_from_user, number_from_bot, context):
        output_data = ['*' for _ in range(4)]
        for enum, bot_num in enumerate(number_from_bot):
            if bot_num == number_from_user[enum]:
                output_data[enum] = bot_num
        if output_data == number_from_bot:
            update.message.reply_text('Congratilations! You guessed all the numbers!\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return False
        elif output_data == ['*' for _ in range(4)]:
            update.message.reply_text('You were unlucky. Not a single number is guessed right\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return True
        elif output_data != ['*' for _ in range(4)]:
            update.message.reply_text('Hmm ... something to guess happened\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return True

def answer(update, check, number_from_bot, context):
        global GAME_NUMBERS
        if GAME_NUMBERS:
            print(1)
            while check:
                print(update.message.text)
                number_from_user = [int(j) for j in update.message.text]
                print(number_from_user)
                check = logika(number_from_user, number_from_bot)

def main():
    updater = Updater('1204493596:AAGfC3E7LFwdgMUmmuL4Vnw6cxgK_l-04Dw', use_context=True, request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    game_numbers_handler = CommandHandler('number', game_numbers)
    answer_handler = MessageHandler(Filters.text, answer)

    dp.add_handler(start_handler)
    dp.add_handler(game_numbers_handler)
    dp.add_handler(answer_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
