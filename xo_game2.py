# Игрa  «Крестики-нолики».
# https://lms.skillfactory.ru/courses/course-v1:SkillFactory+FPW-2.0+27AUG2020/courseware/5474bc39c2294893840f3e89e37d31db/c9591776961d497bbeb9bad8c5e41685/6?activate_block_id=block-v1%3ASkillFactory%2BFPW-2.0%2B27AUG2020%2Btype%40vertical%2Bblock%40f8e187ceae154987ba2c7ad6d7aef96b

from random import randint
#=========
# Исключения
# класс-родитель всех исключений
class UserException(Exception):
    def __str__(self):
        return "Неверный юзер"

class BoardException(Exception):
    pass

# мимо доски BoardOutException
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы игрового поля!"

# Сюда уже стреляли
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

# исключения, когда пытаемся поставить корабль на доску в недопустимое место
class BoardWrongShipException(BoardException):
    pass



class Dot:
   def __init__(self,x,y):
        self.x = x
        self.y = y

   def __eq__(self,other):
       return self.x == other.x and self.y == other.y

   def __str__(self):
       return f'Dot: {self.x,self.y}'

   def __repr__(self):
       return f"({self.x}, {self.y})"

class Board:
    def __init__(self, size=3):
        self.size = size
        self.count = 0 # сколько ходов сделано
        self.field = [["-"] * size for _ in range(size)]
        # точки поля, О, если клетка пустая, квадратик, если в точке корабль, Т, если в точку стреляли, Х если корабль в точке подбит

        self.busy = [] # список точек использованных
        self.dotX = []
        self.dotO = []

    def add_dot(self, d, user):


        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.field[d.x][d.y] = user
        self.busy.append(d)
        if user == 'X':
            self.dotX.append(d)
        elif user == 'O':
            self.dotY.append(d)
        else:
            raise UserException()
        self.count += 1


     def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))


    def begin(self):
        self.busy = []

    def win_v1(self, f, user):
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



class Player:
    def __init__(self, board):
        self.board = board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.board.add_dot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    user = "O"
    def ask(self):
        d = Dot(randint(0, 2), randint(0, 2))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    user = "X"
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты через пробел! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=3):
        self.size = size




    board = Board(size=self.size)
    board.begin()
    self.ai = AI(board)
    self.us = User(board)
    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("  крестики-нолики  ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Игровое поле:")
            print(self.board)
            print("-" * 20)




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

def check_countinue(answer):
    if answer == 's':
        print("Выход из игры")
        return False
    elif answer == 'n':
        return True
    else:
        print("Ответ не ясен")
        answer1 = input("""Сыграть еще раз? Введите "s" для выхода, "n" для начала игры: """)
        return check_countinue(answer1)


# начало игры: рисуем начальное поле:
def start_game():
    field = [["-"] * 3 for _ in range(3)]
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
    return False



# основной сценарий:

answer = input("""Новая игра! Введите "s" для выхода, "n" для начала игры: """)
while check_countinue(answer):
        print("Игра началась")
        start_game()
        print("Игра окончена")
        answer = input("""Сыграть еще раз? Введите "s" для выхода, "n" для начала игры: """)
        continue
