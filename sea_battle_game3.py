# C2.5. Итоговое практическое задание
# Решать задачу будем последовательной реализацией нужных классов.  Можно выделить две группы классов:
#
# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней.
# Внешняя логика игры — пользовательский интерфейс, искусственный интеллект,
# игровой контроллер, который считает побитые корабли.

from random import randint
#=========
# Исключения
# класс-родитель всех исключений
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


#=======================================

# Класс точка: класс Dot — класс точек на поле. Каждая точка описывается параметрами:
#
# Координата по оси x .
# Координата по оси y .
# Метод равенства _eq__, чтобы точки можно было проверять на равенство.
# Тогда, чтобы проверить, находится ли точка в списке, достаточно просто использовать оператор in, как мы делали это с числами .
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

#=======================================
# Класс корабль Ship — корабль на игровом поле, который описывается параметрами:
#
# Длина.
# Точка, где размещён нос корабля.
# Направление корабля (вертикальное/горизонтальное).
# Количеством жизней (сколько точек корабля еще не подбито).
# И имеет методы:
#
# Метод dots, который возвращает список всех точек корабля.
class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow # нос
        self.l = l # длина
        self.o = o # направление: 0 если горизонтально, 1 если вертикально
        self.lives = l #  в начальный момент игры количество жизней равно длин корабля

    @property
    def dots(self):
        ship_dots = [] # список точек корабля
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0: # горизонтальная, добавляем по x
                cur_x += i

            elif self.o == 1: # вертикальная, добавляем по y
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot): # попали ли в корабль
        return shot in self.dots



#=======================================
# класс Board — игровая доска. Доска описывается параметрами:
#
# Двумерный список, в котором хранятся состояния каждой из клеток.
# Список кораблей доски.
# Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
# Количество живых кораблей на доске.
# И имеет методы:
#
# Метод add_ship, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
# Метод contour, который обводит корабль по контуру. Он будет полезен и в ходе самой игры, и в при расстановке кораблей (помечает соседние точки, где корабля по правилам быть не может).
# Метод, который выводит доску в консоль в зависимости от параметра hid.
# Метод out, который для точки (объекта класса Dot) возвращает True, если точка выходит за пределы поля, и False, если не выходит.
# Метод shot, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, нужно выбрасывать исключения).
# # Класс игровой доски
#     "1. `size` - размер доски,
#     "2. `hid` - скрыты ли корабли на доске,
#     "3. `field` - двумерный список с игровым полем,
#     "4. `busy` - список занятых точек,
#     "5. `ships` - список кораблей на доске",
#     "6. `__str__` - метод, который вызывается при печати доски,
#     "7. `add_ship` - метод, который добавляет корабль на доску,
#     "8. `contour` - метод, который обводит корабль по контуру,
#     "9. `out` - метод, который проверяет, вышла ли точка за границу доски,
#     "10. `shot` - метод, который совершает выстрел в точку. Возвращает `bool` значение - может ли игрок повторить выстрел,
#     "11. `begin` - метод, который вызывается в начале игры, после расстановки кораблей"

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid # поле противнка должно быть скрыто, а свое видно

        self.count = 0 # сколько кораблей на доске уничтожено

        self.field = [["O"] * size for _ in range(size)]
        # точки поля, О, если клетка пустая, квадратик, если в точке корабль, Т, если в точку стреляли, Х если корабль в точке подбит

        self.busy = [] # список точек использованных
        self.ships = []

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False): # нельзя ставить корабли на соседние с уже стоящим кораблем клектки
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O") # скрываем корабли противника
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True # можно снова стрелять

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False # переход хода
    def begin(self):
        self.busy = []

#=======================================
# Класс Player — класс игрока в игру (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем. Игрок описывается параметрами:
#
# Собственная доска (объект класса Board)
# Доска врага.
# И имеет следующие методы:
#
# ask — метод, который «спрашивает» игрока, в какую клетку он делает выстрел.
# Пока мы делаем общий для AI и пользователя класс, этот метод мы описать не можем. Оставим этот метод пустым.
# Тем самым обозначим, что потомки должны реализовать этот метод.
# move — метод, который делает ход в игре. Тут мы вызываем метод ask, делаем выстрел по вражеской доске (метод Board.shot),
# отлавливаем исключения, и если они есть, пытаемся повторить ход.
# Метод должен возвращать True, если этому игроку нужен повторный ход (например если он выстрелом подбил корабль).
# Теперь нам остаётся унаследовать классы AI и User от Player и переопределить в них метод ask.
# Для AI это будет выбор случайной точка, а для User этот метод будет спрашивать координаты точки из консоли.
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
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

#=======================================

# класс Game. Игра описывается параметрами:
#
# Игрок-пользователь, объект класса User.
# Доска пользователя.
# Игрок-компьютер, объект класса Ai.
# Доска компьютера.
# И имеет методы:
#
# random_board — метод генерирует случайную доску.
# Для этого мы просто пытаемся в случайные клетки изначально пустой доски расставлять корабли
# (в бесконечном цикле пытаемся поставить корабль в случайную току, пока наша попытка не окажется успешной).
# Лучше расставлять сначала длинные корабли, а потом короткие.
# Если было сделано много (несколько тысяч) попыток установить корабль, но это не получилось,
#  значит доска неудачная и на неё корабль уже не добавить. В таком случае нужно начать генерировать новую доску.
# greet — метод, который в консоли приветствует пользователя и рассказывает о формате ввода.
# loop — метод с самим игровым циклом. Там мы просто последовательно вызываем метод mode для игроков и делаем проверку,
# сколько живых кораблей осталось на досках, чтобы определить победу.
# start — запуск игры. Сначала вызываем greet, а потом loop.
# И останется просто создать экземпляр класса Game и вызвать метод start.
class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


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

# основной сценарий:
answer = input("""Новая игра! Введите "s" для выхода, "n" для начала игры: """)

while check_countinue(answer):
        print("Игра началась")
        g = Game()
        g.start()
        print("Игра окончена")
        answer = input("""Сыграть еще раз? Введите "s" для выхода, "n" для начала игры: """)
        continue

