import math

def taylor_sinh_generator(x):
    term = x
    n = 1

    while True:
        yield term
        term = term * (x ** 2) / ((2 * n) * (2 * n + 1))
        n += 1


x = float(input("x: "))
epsilon = float(input("eps: "))

gen = taylor_sinh_generator(x)
total_sum = 0

for term in gen:
    if abs(term) < epsilon:
        break
    total_sum += term

math_sinh = math.sinh(x)

print(f"sh x: {total_sum}")
print(f"math.sh:  {math_sinh}")