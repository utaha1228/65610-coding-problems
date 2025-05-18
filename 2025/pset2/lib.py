KEYSIZE = 40

def pi(m: int):  
	assert 0 <= m < 2 ** KEYSIZE

	MASK = (1 << KEYSIZE) - 1
	for i in range(4):
		m ^= (m >> 19)
		m = (m * 0x1337 + 0xabdeadbeef) & MASK
		m ^= (m << 17)
		m &= MASK

	return m

def pi_inv(m: int):
	assert 0 <= m < 2 ** KEYSIZE

	t = pow(0x1337, -1, 1 << KEYSIZE)
	MASK = (1 << KEYSIZE) - 1
	for i in range(4):
		m = m ^ (m << 17) ^ (m << 34)
		m &= MASK
		m = ((m - 0xabdeadbeef) * t) & MASK
		m = m ^ (m >> 19) ^ (m >> 38)

	return m

def enc(key: int, msg: int):
	assert 0 <= key < 2 ** KEYSIZE
	assert 0 <= msg < 2 ** KEYSIZE

	# omg 300-round cipher must be very secure
	msg ^= key
	for i in range(300):
		msg = pi(msg)
		msg ^= key

	return msg

def read_data():
	ciphertexts = []
	with open("data.txt", "rb") as f:
		for i in range(2 ** 20):
			ciphertexts.append(int.from_bytes(f.read(KEYSIZE // 8), "big"))

	return ciphertexts

if __name__ == "__main__":
	import random
	for _ in range(30):
		t = random.getrandbits(KEYSIZE)
		assert pi_inv(pi(t)) == t