exec(open("output.txt").read())

Zq = GF(q)
R.<x1,x2,x3,x4,x5,x6,x7,x8> = PolynomialRing(Zq)
s = vector(R, [x1, x2, x3, x4, x5, x6, x7, x8])
A = matrix(R, A)
u = vector(R, u)
e = u - A * s 

equations = [(e[i] - 1) * e[i] * (e[i] + 1) for i in range(len(e))]
monomials = equations[0].monomials()
assert len(monomials) == 165  # 11 choose 3, includes constant term

M = []
v = []
for eq in equations:
	row = [eq.monomial_coefficient(mon) for mon in monomials if mon != 1]
	M.append(row)
	v.append(-eq.monomial_coefficient(R(1)))

M = matrix(Zq, M)
v = vector(Zq, v)

monomial_values = M.solve_right(v)

mp = {}
for mon, val in zip(monomials, monomial_values):
	mp[mon] = val

s = [int(mp[var]) for var in s]
print(s)

