def sequence_generator(x):
    term = 1.0
    k = 0
    while True:
        yield term
        k += 1
        term = term * (-x ** 2) / ((2 * k - 1) * (2 * k))

x = float(input("x: "))
k = int(input("k: "))

gen = sequence_generator(x)
result = 0

for _ in range(k + 1):
    result = next(gen)

print(f"x_k = {result}")