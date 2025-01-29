import itertools

class Prover:
	def __init__(self, R, d, f, H):
		self.R = R
		self.d = d
		self.f = f
		self.H = H
		self.num_vars = 4

		self.round = 0
		self.path = []
		self.var_names = ["x1", "x2", "x3", "x4"]

	def send_answer(self):
		S = self.R(0)
		for tp in itertools.product(self.H, repeat=self.num_vars):
			S += self.f(tp)
		return S

	def send_polynomial(self):
		base = {}
		for i in range(self.round):
			base[self.var_names[i]] = self.path[i]

		poly = 0

		for tp in itertools.product(self.H, repeat=self.num_vars - 1 - self.round):
			dic = base.copy()
			for i in range(self.round + 1, self.num_vars):
				dic[self.var_names[i]] = tp[i - (self.round + 1)]
			poly += self.f(**dic)

		return poly

	def receive_number(self, num):
		self.round += 1
		self.path.append(num) 