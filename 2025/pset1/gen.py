import random

KEYSIZE = 40
def f(m):
	key = int(b"BTHDY".hex(), 16)
	m ^= key

	for i in range(4):
		m ^= (m >> 31)
		m = (m * 0x1337 + 0xabdeadbeef) % (2 ** KEYSIZE)
		m ^= (m << 17)

	return m ^ key


def mul_matrix(A, B):
	size = len(A)
	ret = [[0] * size for _ in range(size)]
	for i in range(size):
		for j in range(size):
			for k in range(size):
				ret[i][k] ^= A[i][j] * B[j][k]
	return ret

def random_upper(size):
	upper = [[0] * size for _ in range(size)]
	upper_inv = [[0] * size for _ in range(size)]
	for i in range(size):
		for j in range(i, size):
			if i == j:
				upper[i][j] = 1
			else:
				upper[i][j] = random.getrandbits(1)

	for i in range(size-1, -1, -1):
		for j in range(i, size):
			if i == j:
				upper_inv[i][j] = 1
			else:
				upper_inv[i][j] = sum(upper[i][t] * upper_inv[t][j] for t in range(size)) & 1

	tmp = mul_matrix(upper, upper_inv)
	for i in range(size):
		for j in range(size):
			assert tmp[i][j] == int(i==j)

	return upper, upper_inv

def random_binary_matrix(size):
	upper, upper_inv = random_upper(size)
	lower, lower_inv = random_upper(size)
	for i in range(size):
		for j in range(i):
			lower[i][j], lower[j][i] = lower[j][i], lower[i][j]
			lower_inv[i][j], lower_inv[j][i] = lower_inv[j][i], lower_inv[i][j]

	M = mul_matrix(lower, upper)
	M_inv = mul_matrix(upper_inv, lower_inv)

	tmp = mul_matrix(M, M_inv)
	for i in range(size):
		for j in range(size):
			assert tmp[i][j] == int(i==j)

	return M, M_inv



def step(ID="a"):
	counter = 0
	key = 284881863769
	M0, M0_inv = random_binary_matrix(KEYSIZE + 1)

	goal = [[i==j for j in range(KEYSIZE + 1)] for i in range(KEYSIZE + 1)]
	for i in range(KEYSIZE):
		if key & (1 << i):
			goal[i][-1] ^= 1

	for i in range(19, KEYSIZE):
		goal[i-19] = [x ^ y for x, y in zip(goal[i-19], goal[i])]

	for i in range(KEYSIZE):  # invert every bit
		goal[i][-1] ^= 1


	M1 = mul_matrix(goal, M0_inv)
	tmp = mul_matrix(M1, M0)
	for i in range(len(tmp)):
		assert tmp[i] == goal[i]

	# M0 * message
	lines = []
	offsets = [random.randrange(KEYSIZE) for _ in range(KEYSIZE + 1)]
	for i in range(KEYSIZE+1):
		expr = []
		for j in range(KEYSIZE):
			if M0[i][j]:
				if offsets[i] > j:
					expr.append(f"m<<{offsets[i]-j}")
				else:
					expr.append(f"m>>{j-offsets[i]}")

		rnd = random.getrandbits(KEYSIZE) | (1 << offsets[i])
		if M0[i][-1]:  # constaint 1
			expr.append(str(rnd))
		else:  # constaint 1
			expr.append(str(0xffffffffff^rnd))

		expr = "^".join(expr)
		lines.append(f"{ID}{counter}={expr}")
		counter += 1

	var = [None] * KEYSIZE
	perm = [i for i in range(KEYSIZE)]
	random.shuffle(perm)

	for i in perm:  # M1 * (M0 * message), dropping the last entry
		expr = []
		for j in range(KEYSIZE + 1):
			if M1[i][j]:
				offset = offsets[j]
				# adjust the info to position i
				if offset < i:
					expr.append(f"{ID}{j}<<{i-offset}")
				else:
					expr.append(f"{ID}{j}>>{offset-i}")

		expr = "^".join(expr)
		# lower the prob that a bit is set to hide the removed bit position
		# 7-bit space to compute
		num = (random.getrandbits(KEYSIZE) & random.getrandbits(KEYSIZE)) | (1 << i)
		num &= (0xffffffffff ^ (0b1111110 << i))
		lines.append(f"{ID}{counter}=({expr})&{num}")
		var[i] = f"{ID}{counter}"
		counter += 1

	# expr = []
	# for i in range(KEYSIZE):
	# 	expr.append(f"({var[i]} & (1 << {i}))")
	# expr = "^".join(expr)
	# lines.append(f"A={expr}")

	# A = (A * 0xffffffecc9 + 0xabdeadabb8)
	var_ = []
	for i in range(KEYSIZE):  # calculate bit i value
		expr = []
		for j in range(i+1):
			if (0xffffffecc9 >> j) & 1:
				expr.append(f"({var[i-j]}>>{i-j})")
		if (0xabdeadabb8 >> i) & 1:
			num = random.getrandbits(KEYSIZE) & random.getrandbits(KEYSIZE)
			num = ((num >> 7) << 7) + 1
			expr.append(str(num))

		# carry
		tmp = (random.getrandbits(KEYSIZE) >> 7) << 7
		tmp ^= 0b0111111
		if len(var_):
			expr.append(f"({var_[-1]}>>1)&{tmp}")

		random.shuffle(expr)
		lines.append(f"{ID}{counter}=sum([{','.join(expr)}])")
		var_.append(f"{ID}{counter}")
		counter += 1

	constant = 0

	exprs = []

	for i in range(17):
		# (key[i]^var[i]) * (2 ** i)
		if key & (1 << i):
			if random.getrandbits(1):
				exprs.append(random.choice([
					f"((({var_[i]}<<{i})^(1<<{i}))&(1<<{i}))",
					f"((({var_[i]}&1)<<{i})^(1<<{i}))",
					f"((({var_[i]}&1)^1)<<{i})",
				]))
			else:
				constant += (1 << i)
				exprs.append(random.choice([
					f"(-(({var_[i]}<<{i})&(1<<{i})))",
					f"(-(({var_[i]}&1)<<{i}))",
				]))
		else:
			exprs.append(random.choice([
				f"(({var_[i]}&1)<<{i})",
				f"(({var_[i]}<<{i})&(1<<{i}))",
			]))

	for i in range(17, KEYSIZE):
		# (key[i]^var[i] ^ var[i-17]) * (2 ** i)
		if key & (1 << i):
			if random.getrandbits(1):
				constant += (1 << i)
				exprs.append(f"(-((({var_[i]}^{var_[i-17]})&1)<<{i}))")
			else:
				exprs.append(f"(((1^{var_[i]}^{var_[i-17]})&1)<<{i})")
		else:
			exprs.append(f"((({var_[i]}^{var_[i-17]})&1)<<{i})")

	exprs.append(str(constant))
	random.shuffle(exprs)
	exprs = "+".join(exprs)
	lines.append(f"m={exprs}")

	# expr = []
	# for i in range(KEYSIZE):
	# 	expr.append(f"({var_[i]} & 1) << {i}")
	# expr = "^".join(expr)
	# lines.append(f"A={expr}")

	return lines
	
	

lines = sum([step() for _ in range(4)], start=[])
for line in lines:
	print(line)