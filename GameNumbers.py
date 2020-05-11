class Number():
    def logika(self, number_from_user, number_from_bot, context, chance, chat_id):
        output_data = ['*' for _ in range(4)]
        for enum, bot_num in enumerate(number_from_bot):
            if bot_num == number_from_user[enum]:
                output_data[enum] = bot_num
        if output_data == number_from_bot:
            context.bot.send_message(chat_id=chat_id, text='Ура! Число отгадано: {}'.format(
                ''.join(map(lambda x: str(x), output_data))))
            return True
        elif output_data == ['*' for _ in range(4)]:
            context.bot.send_message(chat_id=chat_id, text='К сожалению, нет ни одной правильной цифры '
                                                           '(осталось попыток: {})'.format(chance))
            return False
        elif output_data != ['*' for _ in range(4)]:
            context.bot.send_message(chat_id=chat_id, text='Хмм... Некоторые цифры угаданы\nЧисло: {} '
                                                           '(осталось попыток: {})'.format(
                ' '.join(map(lambda x: str(x), output_data)), chance))
            return False
