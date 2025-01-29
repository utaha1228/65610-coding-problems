import random

q = 65537
n = 8
m = 170
B = 1

A = [[random.randrange(0, q) for j in range(n)] for i in range(m)]
s = [random.randrange(0, q) for j in range(n)]

u = [sum(A[i][j] * s[j] for j in range(n)) % q for i in range(m)]
# adding error terms
for i in range(m):
	u[i] = (u[i] + random.randint(-B, B)) % q

with open("output.txt", "w") as f:
	f.write(f"{q = }\n")
	f.write(f"{n = }\n")
	f.write(f"{m = }\n")
	f.write(f"{B = }\n")
	f.write(f"{A = }\n")
	f.write(f"{u = }\n")

print(f"{s = }")