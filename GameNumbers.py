class number():
    def logika(self, number_from_user, number_from_bot, update, chance):
        output_data = ['*' for _ in range(4)]
        for enum, bot_num in enumerate(number_from_bot):
            if bot_num == number_from_user[enum]:
                output_data[enum] = bot_num
        if output_data == number_from_bot:
            update.message.reply_text('Ура! Число отгадано: {}'.format(
                ''.join(map(lambda x: str(x), output_data))))
            return True
        elif output_data == ['*' for _ in range(4)]:
            update.message.reply_text('К сожалению, нет ни одной правильной цифры(осталось попыток: {})'.format(chance))
            return False
        elif output_data != ['*' for _ in range(4)]:
            update.message.reply_text('Хмм... Некоторые цифры угаданы\nЧисло: {} (осталось попыток: {})'.format(
                ' '.join(map(lambda x: str(x), output_data)), chance))
            return False
