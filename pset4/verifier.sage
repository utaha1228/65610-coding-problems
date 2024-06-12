from prover import Prover
import random

def test():
	# parameter setup
	q = 65537
	Zq = GF(q)
	num_vars = 4
	R.<x1, x2, x3, x4> = PolynomialRing(Zq)
	variables = [x1, x2, x3, x4]
	d = 4
	monomials = ((x1 + x2 + x3 + x4 + 1) ** d).monomials()
	f = sum([Zq.random_element() * mon for mon in monomials])  # a random polynomial
	H = [0, 1, 2]

	# create a prover class for further interaction
	P = Prover(R, d, f, H)

	# start the verification process
	beta = P.send_answer()

	for i in range(num_vars):
		g = P.send_polynomial()

		# check it's only using variables[i] as variable
		for j in range(num_vars):
			assert j == i or g.degree(variables[j]) == 0

		# check if it sums up to the correct number
		S = 0
		for num in H:
			inp = [0] * num_vars
			inp[i] = num
			S += g(*inp)

		assert S == beta

		# send prover the new number
		new_num = random.choice(H)
		P.receive_number(new_num)
		inp = [0] * num_vars
		inp[i] = new_num
		beta = g(*inp)

if __name__ == "__main__":
	for _ in range(100):
		test()
