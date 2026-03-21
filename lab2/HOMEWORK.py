import turtle
import random
import math


class Stem:
    def __init__(self, length):
        self.length = length
        self.color = "darkgreen"
        self.thickness = 5

    def draw(self, base_x, base_y, heading):
        turtle.penup()
        turtle.goto(base_x, base_y)
        turtle.setheading(heading)
        turtle.pendown()
        turtle.color(self.color)
        turtle.pensize(self.thickness)
        turtle.forward(self.length)
        turtle.pensize(1)


class Leaf:
    def __init__(self, size):
        self.size = size
        self.color = "green"

    def draw(self, x, y, heading):
        turtle.penup()
        turtle.goto(x, y)
        turtle.setheading(heading)
        turtle.pendown()
        turtle.color(self.color)
        turtle.fillcolor(self.color)

        turtle.begin_fill()
        turtle.circle(self.size, 90)
        turtle.left(90)
        turtle.circle(self.size, 90)
        turtle.end_fill()


class Petal:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def draw(self, x, y, heading):
        turtle.penup()
        turtle.goto(x, y)
        turtle.setheading(heading)
        turtle.pendown()
        turtle.color(self.color)
        turtle.fillcolor(self.color)

        turtle.begin_fill()
        turtle.circle(self.size, 60)
        turtle.left(120)
        turtle.circle(self.size, 60)
        turtle.end_fill()


class Flower:
    # Оставили только 4 обязательных позиционных аргумента
    def __init__(self, x, y, scale, tilt):
        self.x = x
        self.y = y
        self.scale = scale
        self.tilt = tilt

        self.stem = Stem(280 * scale)
        self.leaf = Leaf(50 * scale)

        colors = ["red", "magenta", "orange", "pink", "blue", "cyan", "lightblue"]
        random_color = random.choice(colors)
        self.petal = Petal(80 * scale, random_color)

        self.center_color = "yellow"

    def draw(self):
        stem_heading = 90 + self.tilt
        stem_rad = math.radians(stem_heading)

        self.stem.draw(self.x, self.y, stem_heading)

        head_x = self.x + self.stem.length * math.cos(stem_rad)
        head_y = self.y + self.stem.length * math.sin(stem_rad)

        d_leaf = self.stem.length * 0.5
        leaf_x = self.x + d_leaf * math.cos(stem_rad)
        leaf_y = self.y + d_leaf * math.sin(stem_rad)

        self.leaf.draw(leaf_x, leaf_y, 20 + self.tilt)
        self.leaf.draw(leaf_x, leaf_y, 200 + self.tilt)

        petals_count = 8
        angle_step = 360 / petals_count
        for i in range(petals_count):
            self.petal.draw(head_x, head_y, i * angle_step + self.tilt)

        offset_d = 15 * self.scale
        offset_rad = math.radians(stem_heading - 90)

        turtle.penup()
        turtle.goto(head_x, head_y - 15 * self.scale)
        turtle.setheading(0)
        turtle.pendown()
        turtle.color(self.center_color)
        turtle.fillcolor(self.center_color)
        turtle.begin_fill()
        turtle.circle(15 * self.scale)
        turtle.end_fill()


if __name__ == '__main__':
    turtle.hideturtle()
    turtle.tracer(0)

    bouquet = [
        Flower(0, -200, 1.25, 8),
        Flower(0, -200, 0.9, 22),
        Flower(0, -200, 1.1, -15),
        Flower(0, -200, 0.95, 40),
        Flower(0, -200, 1.0, -32),
        Flower(0, -200, 0.95, -5),
        Flower(0, -200, 0.75, 55),
        Flower(0, -200, 0.8, -48),
        Flower(0, -200, 1, 12)
    ]

    for flower in bouquet:
        flower.draw()

    turtle.update()
    turtle.mainloop()