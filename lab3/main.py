import math


class Shape:
    def dimention(self):
        return None

    def perimetr(self):
        return None

    def square(self):
        return None

    def squareSurface(self):
        return None

    def squareBase(self):
        return None

    def height(self):
        return None

    def volume(self):
        return None


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    def dimention(self):
        return 2

    def perimetr(self):
        return self.a + self.b + self.c

    def square(self):
        p = self.perimetr() / 2
        x = p * (p - self.a) * (p - self.b) * (p - self.c)
        if x < 0:
            return 0
        return math.sqrt(x)

    def volume(self):
        return self.square()


class Rectangle(Shape):
    def __init__(self, a, b):
        self.a = float(a)
        self.b = float(b)

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.b

    def volume(self):
        return self.square()


class Trapeze(Shape):
    def __init__(self, a, b, c, d):
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.d = float(d)

    def dimention(self):
        return 2

    def perimetr(self):
        return self.a + self.b + self.c + self.d

    def square(self):
        if self.a == self.b:
            return 0
        x = (self.a - self.b) ** 2 + self.c ** 2 - self.d ** 2
        y = 2 * abs(self.a - self.b)
        if y == 0:
            return 0
        z = self.c ** 2 - (x / y) ** 2
        if z < 0:
            return 0
        h = math.sqrt(z)
        return ((self.a + self.b) / 2) * h

    def volume(self):
        return self.square()


class Parallelogram(Shape):
    def __init__(self, a, b, h):
        self.a = float(a)
        self.b = float(b)
        self.h = float(h)

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * (self.a + self.b)

    def square(self):
        return self.a * self.h

    def volume(self):
        return self.square()


class Circle(Shape):
    def __init__(self, r):
        self.r = float(r)

    def dimention(self):
        return 2

    def perimetr(self):
        return 2 * math.pi * self.r

    def square(self):
        return math.pi * self.r * self.r

    def volume(self):
        return self.square()


class Ball(Shape):
    def __init__(self, r):
        self.r = float(r)

    def dimention(self):
        return 3

    def volume(self):
        return (4 / 3) * math.pi * (self.r ** 3)


class TriangularPyramid(Triangle):
    def __init__(self, a, h):
        super().__init__(a, a, a)
        self.h = float(h)

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1 / 3) * self.squareBase() * self.h


class QuadrangularPyramid(Rectangle):
    def __init__(self, a, b, h):
        super().__init__(a, b)
        self.h = float(h)

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1 / 3) * self.squareBase() * self.h


class RectangularParallelepiped(Rectangle):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = float(c)

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.c

    def volume(self):
        return self.squareBase() * self.c


class Cone(Circle):
    def __init__(self, r, h):
        super().__init__(r)
        self.h = float(h)

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return (1 / 3) * self.squareBase() * self.h


class TriangularPrism(Triangle):
    def __init__(self, a, b, c, h):
        super().__init__(a, b, c)
        self.h = float(h)

    def dimention(self):
        return 3

    def squareBase(self):
        return super().square()

    def height(self):
        return self.h

    def volume(self):
        return self.squareBase() * self.h


files = ["input01.txt", "input02.txt", "input03.txt"]
output_file = open("results.txt", "w")

for filename in files:
    lines = []
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
    except:
        continue

    shapes = []
    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue
        name = parts[0]
        numbers = []
        for p in parts[1:]:
            try:
                numbers.append(float(p))
            except:
                pass

        if name == "Triangle" and len(numbers) == 3:
            shapes.append(Triangle(numbers[0], numbers[1], numbers[2]))
        elif name == "Rectangle" and len(numbers) == 2:
            shapes.append(Rectangle(numbers[0], numbers[1]))
        elif name == "Trapeze" and len(numbers) == 4:
            shapes.append(Trapeze(numbers[0], numbers[1], numbers[2], numbers[3]))
        elif name == "Parallelogram" and len(numbers) == 3:
            shapes.append(Parallelogram(numbers[0], numbers[1], numbers[2]))
        elif name == "Circle" and len(numbers) == 1:
            shapes.append(Circle(numbers[0]))
        elif name == "Ball" and len(numbers) == 1:
            shapes.append(Ball(numbers[0]))
        elif name == "TriangularPyramid" and len(numbers) == 2:
            shapes.append(TriangularPyramid(numbers[0], numbers[1]))
        elif name == "QuadrangularPyramid" and len(numbers) == 3:
            shapes.append(QuadrangularPyramid(numbers[0], numbers[1], numbers[2]))
        elif name == "RectangularParallelepiped" and len(numbers) == 3:
            shapes.append(RectangularParallelepiped(numbers[0], numbers[1], numbers[2]))
        elif name == "Cone" and len(numbers) == 2:
            shapes.append(Cone(numbers[0], numbers[1]))
        elif name == "TriangularPrism" and len(numbers) == 4:
            shapes.append(TriangularPrism(numbers[0], numbers[1], numbers[2], numbers[3]))

    max_measure = -1
    largest_shape = None

    for s in shapes:
        v = s.volume()
        if v != None and v > max_measure:
            max_measure = v
            largest_shape = s

    output_file.write(filename + ":\n")
    if largest_shape != None:
        output_file.write(type(largest_shape).__name__ + "\n")
        output_file.write(str(max_measure) + "\n")
    else:
        output_file.write("No shapes found\n")
    output_file.write("\n")

output_file.close()