class Party:
	def __init__(self, x_share, y_share, tim_triplets, p):
		self.x = x_share
		self.y = y_share
		self.A, self.B, self.AB = tim_triplets
		self.p = p

		self.stage = 0

	def run(self, info=None):
		if self.stage == 0:
			self.stage += 1
			return self.stage0()
		elif self.stage == 1:
			self.stage += 1
			self.x_plus_A = info
			return self.stage1()
		elif self.stage == 2:
			self.stage += 1
			self.y_plus_B = info
			return self.stage2()

	def stage0(self):
		return ("reconstruct", (self.x + self.A) % self.p)

	def stage1(self):
		return ("reconstruct", (self.y + self.B) % self.p)

	def stage2(self):
		share = (self.y * self.x_plus_A - self.A * self.y_plus_B + self.AB) % self.p
		return ("submit", share)