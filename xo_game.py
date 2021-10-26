# Игрa  «Крестики-нолики».
# https://lms.skillfactory.ru/courses/course-v1:SkillFactory+FPW-2.0+27AUG2020/courseware/5474bc39c2294893840f3e89e37d31db/c9591776961d497bbeb9bad8c5e41685/6?activate_block_id=block-v1%3ASkillFactory%2BFPW-2.0%2B27AUG2020%2Btype%40vertical%2Bblock%40f8e187ceae154987ba2c7ad6d7aef96b

# функция рисовки поля
from typing import List


def show_field(field):
    print('  0 1 2')
    for i in range(len(field)):
        print(str(i) + ' ' + ' '.join(field[i]))


# функция опрос пользователя
def user_input(f):
    global x, y
    while True:
        place: List[str] = input("введите две координаты (от 0 до 2) через пробел: ").split()
        if len(place) != 2:
            print("Введено неверное количество значений ")
            continue
        if not(place[0].isdigit() and place[1].isdigit()):
            print("Введены не числа ")
            continue
        x, y = map(int, place)
        if not(0 <= x < 3 and 0 <= y < 3):
            print("Вышли из диапазона: ")
            continue
        print(place)
        if f[x][y] != '-':
            print("Клетка занята, введите другое значение координат: ")
            continue
        break
    return x, y


# функция проверки на победу
def win_v1(f, user):
    def check_line(a1, a2, a3, user1):
        if a1 == user1 and a2 == user1 and a3 == user1:
            return True

    for n in range(3):
        if check_line(f[n][0], f[n][1], f[n][2], user) or \
                check_line(f[0][n], f[1][n], f[2][n], user) or \
                check_line(f[0][0], f[1][1], f[2][2], user) or \
                check_line(f[2][0], f[1][1], f[0][2], user):
            return True
    return False


# начало игры: рисуем начальное поле:
def start_game(answer1):
    field = [["-"] * 3 for _ in range(3)]
    #    print("Новая игра!")
    #    answer = input("""Новая игра! Введите "s" для выхода, "n" для начала игры: """)
    if answer1 == 's':
        print("Выход из игры")
        return False
    elif answer1 == 'n':
        print("Игра началась")
        count = 0
        while True:
            if count == 9:
                print('Ничья')
                break
            if count % 2 == 0:
                user = 'x'
            else:
                user = 'y'
            show_field(field)
            print(f"Ходит user {user}!")
            x1, y1 = user_input(field)
            field[x1][y1] = user
            if win_v1(field, user):
                print(f"Выиграл {user}!")
                show_field(field)
                break
            count += 1
        print("Игра окончена")
        answer1 = input("""Сыграть еще раз? Введите "s" для выхода, "n" для начала игры: """)
        return start_game(answer1)
    else:
        print("Ответ не ясен")
        return True


# основной сценарий:
answer = input("""Новая игра! Введите "s" для выхода, "n" для начала игры: """)

start_game(answer)
