import random


class number():
    def __init__(self):
        self.check = True
        dataset_numbers = [i for i in range(10)]
        number_from_bot = [random.choice(dataset_numbers) for _ in range(4)]
        check = True

    def logika(self, number_from_user, number_from_bot):
        output_data = ['*' for _ in range(4)]
        for enum, bot_num in enumerate(number_from_bot):
            if bot_num == number_from_user[enum]:
                output_data[enum] = bot_num
        if output_data == number_from_bot:
            print('Congratilations! You guessed all the numbers!\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return False
        elif output_data == ['*' for _ in range(4)]:
            print('You were unlucky. Not a single number is guessed right\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return True
        elif output_data != ['*' for _ in range(4)]:
            print('Hmm ... something to guess happened\n{}'.format(' '.join(map(lambda x: str(x),output_data))))
            return True

    while check:
        number_from_user = [int(j) for j in input('Input numbers(4x simbols): ')]
        check = number().logika(number_from_user, number_from_bot)
