import itertools

class Prover:
	def __init__(self, R, d, f, H):
		# feel free to change the constructor
		self.R = R
		self.d = d
		self.f = f
		self.H = H
		self.num_vars = 4
		self.var_names = ["x1", "x2", "x3", "x4"]

	def send_answer(self):
		# TODO: roughly 5-10 lines

	# The following two functions should be stateful. In other
	# words, you should store the previous communication with the
	# verifier.

	# In total, roughly 15-30 lines for these two functions

	def send_polynomial(self):
		# TODO

	def receive_number(self, num):
		# TODO