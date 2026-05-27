import math

def sequence_term_generator():
    a = 1
    b = 1
    k = 1

    while True:
        term = (2 ** k) / ((1 + a ** 2 + b ** 2) * math.factorial(k))
        yield term

        next_a = 3 * b + 2 * a
        next_b = 2 * a + b
        a = next_a
        b = next_b
        k += 1


n = int(input("n: "))

gen = sequence_term_generator()
total_sum = 0

for _ in range(n):
    total_sum += next(gen)

print(f"Сума = {total_sum}")