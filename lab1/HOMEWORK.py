import math

class Triangle():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.is_exist = a+b+c > 2*max(a,b,c)

    def Perimeter(self):
        return (self.a+self.b+self.c) if self.is_exist else 0

    def area(self):
        p=self.Perimeter()/2
        return (p*(p-self.a)*(p-self.b)*(p-self.c))**(1/2) if self.is_exist else 0

    def Print(self):
        return f"Triangle {self.a} {self.b} {self.c}"

class Rectangle():
    def __init__(self,a,b):
        self.a=a
        self.b=b

        self.is_exist = min(a,b)>0

    def Perimeter(self):
        return 2*(self.a+self.b) if self.is_exist else 0

    def area(self):
        return self.a*self.b if self.is_exist else 0

    def Print(self):
        return f"Rectangle {self.a} {self.b}"

class Trapze():
    def __init__(self,a1,a2,b1,b2):
        self.a1=a1
        self.b1=b1
        self.a2=a2
        self.b2=b2

        self.is_exist= a1 != a2 and abs(a1-a2)<b1+b2 and abs(b1-b2)<abs(a1-a2)


    def Perimeter(self):
        return (self.a1+self.b1+self.a2+self.b2) if self.is_exist else 0

    def area(self):
        a1=self.a1
        a2=self.a2
        b1=self.b1
        b2=self.b2

        return (a1+a2)/2 * (b1*b1-(((a1-a2)**2 + b1*b1-b2*b2)/(2*(a1-a2)))**2)**(1/2) if self.is_exist else 0

    def Print(self):
        return f"Trapeze {self.a1} {self.a2} {self.b1} {self.b2}"

class Parallelogram():
    def __init__(self,a,b,h):
        self.a=a
        self.b=b
        self.h=h

        self.is_exist = min(a,b,h)>0 and b>=h

    def Perimeter(self):
        return 2*(self.a+self.b) if self.is_exist else 0

    def area(self):
        return self.a*self.h if self.is_exist else 0

    def Print(self):
        return f"Parallelogram {self.a} {self.b} {self.h}"

class Circle():
    def __init__(self,radius):
        self.radius=radius

    def Perimeter(self):
        return 2*math.pi*self.radius

    def area(self):
        return math.pi*self.radius**2

    def Print(self):
        return f"Circle {self.radius}"

def get_figure(line):
    s=line.split()
    args=[int(a) for a in s[1:]]
    if s[0]=="Triangle":
        return Triangle(*args)
    if s[0]=="Rectangle":
        return Rectangle(*args)
    if s[0]=="Trapeze":
        return Trapze(*args)
    if s[0]=="Parallelogram":
        return Parallelogram(*args)
    if s[0]=="Circle":
        return Circle(*args)

def find_max(file, output):

    with open(file, 'r') as f:
        lines=f.readlines()
        maxS_figure = maxP_figure=get_figure(lines[0])
        maxS=maxS_figure.area()
        maxP=maxP_figure.Perimeter()

        for l in lines[1:]:
            f=get_figure(l)
            if f.area()>maxS:
                maxS=f.area()
                maxS_figure=f
            if f.Perimeter()>maxP:
                maxP=f.Perimeter()
                maxP_figure=f

        with open(output, 'a') as f:
            f.write(f"---{file}--- \n")
            f.write(f"Max perimeter: {maxP_figure.Print()} \n")
            f.write(f"Max area: {maxS_figure.Print()}\n \n")

if __name__=="__main__":
    find_max("input01.txt", "output.txt")
    find_max("input02.txt", "output.txt")
    find_max("input03.txt", "output.txt")