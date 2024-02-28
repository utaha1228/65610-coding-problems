import random

random.seed(65610)

q = 147573952589676412927  # (2 ** 67) - 1
n = 10
m = 20


s = [random.randrange(0, q) for j in range(n)]
A = [[random.randrange(0, q) for j in range(n)] for i in range(m)]

u = [sum(A[i][j] * s[j] for j in range(n)) % q for i in range(m)]
# adding error terms
for i in range(m):
	u[i] = (u[i] + random.randint(-10, 10)) % q

print(f"{s = }")
print(f"{A = }")
print(f"{u = }")
