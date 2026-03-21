import time
import turtle
from random import randint
import math
import math

class Triangle:

    def __init__(self, x1, y1, x2, y2):
        self.position=(0,0)
        self.vertex1=(x1,y1)
        self.vertex2=(x2,y2)

        self.color="black"

    @property
    def Vertex1(self):
        return self.vertex1

    @property
    def Vertex2(self):
        return self.vertex2

    def set_position(self, pos):
        self.position=pos

    def set_color(self, color):
        self.color=color

    def rotated_copy(self, angle):
        pos = Triangle.rotate_point(self.position, self.pivot, angle)
        v1 =Triangle.rotate_point(self.vertex1, self.pivot, angle)
        v2 = Triangle.rotate_point(self.vertex2, self.pivot, angle)

        res=Triangle(v1[0], v1[1], v2[0], v2[1])
        res.set_position(pos)
        res.set_color(self.color)
        return res

    def set_pivot(self, pivot):
        self.pivot=pivot

    def rotate_animation(self, angle, step):
        turtle.tracer(0)
        current_angle=0

        while current_angle < angle:
            turtle.clear()

            turtle.penup()
            turtle.goto(self.pivot[0], self.pivot[1])
            turtle.dot(8, "red")

            current_angle += step
            self.rotated_copy(current_angle).draw()

            turtle.update()

            time.sleep(0.005)
    def draw(self):
        turtle.penup()
        turtle.goto(self.position[0], self.position[1])
        turtle.pendown()
        turtle.color(self.color)
        turtle.goto(self.vertex1[0], self.vertex1[1])
        turtle.goto(self.vertex2[0], self.vertex2[1])
        turtle.goto(self.position[0], self.position[1])

    @staticmethod
    def rotate_point(point, pivot, angle):
        x = point[0]
        y = point[1]
        xp = pivot[0]
        yp = pivot[1]
        x1 = xp + (x - xp) * math.cos(angle) - (y - yp) * math.sin(angle)
        y1 = yp + (x - xp) * math.sin(angle) + (y - yp) * math.cos(angle)
        return [x1, y1]

    @staticmethod
    def random_triangle():
        x1=randint(-300,300)
        y1=randint(-300,300)
        x2=randint(-300,300)
        y2=randint(-300,300)
        x3=randint(-300,300)
        y3=randint(-300,300)
        colors=["red","green","blue","yellow","magenta","cyan"]
        triangle=Triangle(x1,y1,x2,y2)
        triangle.position=(x3,y3)
        triangle.color = colors[randint(0,len(colors)-1)]

        return triangle



if __name__ == '__main__':
    turtle.hideturtle()
    turtle.speed(50000)

    #for i in range(100):
    #    triangle=Triangle.random_triangle()
    #    triangle.draw()

    triangle=Triangle.random_triangle()
    triangle.draw()
    triangle.set_pivot([0,0])
    triangle.rotate_animation(10, 0.005)

    turtle.mainloop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
