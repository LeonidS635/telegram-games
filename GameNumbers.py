class number():
    def logika(self, number_from_user, number_from_bot, update):
        output_data = ['*' for _ in range(4)]
        for enum, bot_num in enumerate(number_from_bot):
            if bot_num == number_from_user[enum]:
                output_data[enum] = bot_num
        if output_data == number_from_bot:
            update.message.reply_text('Congratilations! You guessed all the numbers!\n{}'.format(
                ' '.join(map(lambda x: str(x), output_data))))
            #return False
        elif output_data == ['*' for _ in range(4)]:
            update.message.reply_text('You were unlucky. Not a single number is guessed right\n{}'.format(
                ' '.join(map(lambda x: str(x), output_data))))
            #return True
        elif output_data != ['*' for _ in range(4)]:
            update.message.reply_text(
                'Hmm ... something to guess happened\n{}'.format(' '.join(map(lambda x: str(x), output_data))))
            #return True
