def sum_generator():
    total_sum = 0
    i = 2
    while True:
        total_sum += 1 / ((i - 1) * i)
        yield total_sum
        i += 1

n = int(input("n: "))

gen = sum_generator()
result = 0

for _ in range(n - 1):
    result = next(gen)

print(f"S_n = {result}")