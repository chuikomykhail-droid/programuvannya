def determinant_generator():
    yield 3
    yield 7

    d_prev2 = 3
    d_prev1 = 7

    while True:
        d_curr = 3 * d_prev1 - 2 * d_prev2
        yield d_curr
        d_prev2 = d_prev1
        d_prev1 = d_curr


n = int(input("n: "))

gen = determinant_generator()

result = 0
for _ in range(n):
    result = next(gen)

print(f"detD_{n} = {result}")