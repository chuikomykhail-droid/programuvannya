import turtle


class Figure:
    def __init__(self):
        self.x = 0
        self.y = 0

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self, color):
        pass

    def show(self):
        self.draw("black")

    def hide(self):
        self.draw("white")


class Board(Figure):
    def draw(self, color):
        turtle.pencolor(color)
        turtle.pensize(3)
        turtle.penup()

        for x in [-100, 100]:
            turtle.goto(x, 300)
            turtle.pendown()
            turtle.goto(x, -300)
            turtle.penup()

        for y in [-100, 100]:
            turtle.goto(-300, y)
            turtle.pendown()
            turtle.goto(300 , y)
            turtle.penup()


class Cross(Figure):
    def draw(self, color):
        turtle.pencolor(color)
        turtle.pensize(5)
        turtle.penup()
        turtle.goto(self.x - 40, self.y + 40)
        turtle.pendown()
        turtle.goto(self.x  + 40, self.y - 40)
        turtle.penup()
        turtle.goto(self.x +  40 , self.y + 40)
        turtle.pendown()
        turtle.goto(self.x - 40, self.y - 40)
        turtle.penup()


class Nought(Figure):
    def draw(self, color):
        turtle.pencolor(color)
        turtle.pensize(5)
        turtle.penup()
        turtle.goto(self.x, self.y - 40)
        turtle.pendown()
        turtle.circle(40)
        turtle.penup()


turn = "X"
grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
game_over = False


def check_win():
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0] != 0:
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i] != 0:
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] != 0:
        return True
    if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] != 0:
        return True
    return False


def click(x, y):
    global turn, game_over

    if game_over:
        return

    col = -1
    if -300 < x < -100:
        col = 0
    elif -100 <= x <= 100:
        col = 1
    elif 100 < x < 300:
        col = 2

    row = -1
    if 100 < y < 300:
        row = 0
    elif -100 <= y <= 100:
        row = 1
    elif -300 < y < -100:
        row = 2

    if col != -1 and row != -1 and grid[row][col] == 0:
        grid[row][col] = turn

        cx = (col - 1) * 200
        cy = (1 - row) * 200

        if turn == "X":
            c = Cross()
            c.setPosition(cx, cy)
            c.show()
            if check_win():
                game_over = True
            else:
                turn = "O"
        else:
            n = Nought()
            n.setPosition(cx, cy)
            n.show()
            if check_win():
                game_over = True
            else:
                turn = "X"


turtle.speed(0)
turtle.hideturtle()
turtle.title("krestiki noliki")

b = Board()
b.show()

turtle.onscreenclick(click)
turtle.listen()
turtle.done()