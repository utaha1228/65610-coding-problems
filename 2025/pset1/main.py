from enc import enc

KEYSIZE = 40
# the random permutation `pi` is the same for the one in `enc.py`
def pi(m: int):  
	assert 0 <= m < 2 ** KEYSIZE

	MASK = (1 << KEYSIZE) - 1
	for i in range(4):
		m ^= (m >> 19)
		m = (m * 0x1337 + 0xabdeadbeef) & MASK
		m ^= (m << 17)
		m &= MASK

	return m

class EvenMansour:
	def __init__(self, key: int):
		assert 0 <= key < 2 ** KEYSIZE
		self.key = key

	def encrypt(self, m: int):
		assert 0 <= m < 2 ** KEYSIZE
		k = self.key
		return k ^ pi(m ^ k)


def birthday_attack(f) -> int:
	"""
	Args:
	  `f` is a function that takes a single integer message and outputs
	  its encryption (as an integer). Both integer should be bounded by
	  [0, 2^keysize).
	Return:
	  the key of `f`, if `f` is correctly implement a Even-Mansour
	  encryption.
	"""

	# YOUR CODE STARTS HERE
	return 0


if __name__ == "__main__":
	key = int.from_bytes(b"6.5610IsFun", "big") % (2 ** KEYSIZE)
	cipher = EvenMansour(key)

	assert pi(0) == 751329286025, f"Don't touch the `pi` function! {pi(0)}"

	test_key = birthday_attack(lambda x: cipher.encrypt(x))

	print(f"Testing")
	print(f"  Key recovered: {hex(test_key)}")
	print(f"  Actual key:    {hex(key)}")

	secret_key = birthday_attack(enc)

	print(f"Challenge in enc.py")
	print(f"  Key recovered: {hex(secret_key)}")
	# if the code fails on the following line, you got the wrong key.
	print(f"  {secret_key.to_bytes(8, 'big').decode('ascii')}!")



