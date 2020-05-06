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
            print("hv")
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
                        print("kvckc")
                        ch -= 1
                    print(used_words)
                else:
                    print('Tak0e sl0v0 yshe bil0!\n SHTRAF -1')
                    ch -= 1
            else:
                flag = False

def hod_kompa():
    FLAG = False
    word_bot = random.choice(data)
    used_words.append(word_bot)
    print(word_bot)

hod_igroka()
hod_kompa()
hod_igroka()
hod_kompa()
hod_igroka()
hod_kompa()