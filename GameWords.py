import random


used_words=[]

with open('russian_nouns.txt', 'r', encoding='UTF-8') as file:
    data = file.read()
    data = data.split('\n')


def hod_igroka():
    global ch
    flag = True
    ch = 0

    while flag:
        word_player = input('Vvedite sl0v0: ')

        if word_player not in data:
            print("Это не существительное или такого слова не существует")
            ch -= 1
        else:
            if len(used_words) != 0:
                if word_player not in used_words:
                    if word_player[0] == used_words[-1][-1]:
                        used_words.append(word_player)
                        ch += 1
                        print('schet: ', ch)
                        flag = False
                    else:
                        print("Слово должно начинаться с последней буквы предыдущего слова")
                        ch -= 1
                    print(used_words)
                else:
                    print('Такое слово уже было!')
                    ch -= 1
            else:
                used_words.append(word_player)
                flag = False

def hod_kompa():
    letter = used_words[-1][-1]
    if letter == 'ъ' or letter == 'ы' or letter == 'ь':
        letter = used_words[-1][-2]
    print(letter)
    with open('russian_nouns_{}.txt'.format(letter), 'r', encoding='UTF-8') as file:
        data_letter = file.read()
        data_letter = data_letter.split('\n')
    word_bot = random.choice(data_letter)
    used_words.append(word_bot)
    print(word_bot)

hod_igroka()
hod_kompa()
hod_igroka()
hod_kompa()
hod_igroka()
hod_kompa()