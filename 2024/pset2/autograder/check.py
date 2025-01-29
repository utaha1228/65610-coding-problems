from encrypt import enc
import json

q = (2 ** 67) - 1
n = 10
m = 20

s = [136525239469865021712, 138146514979163998923, 41780762499514054813, 80595720452531236909, 48810317605311974993, 64238149465018616518, 120250933917517996395, 68955489162057622758, 54869499637774367192, 139442203655814650431]
assert len(s) == n

def typecheck(a):
	assert isinstance(a, list)
	assert all(isinstance(x, int) for x in a)
	assert all(0 <= x < q for x in a)
	assert len(a) == n + 1

def decrypt(a):
	z = [-x % q for x in s] + [1]
	dec = sum(x * y for x, y in zip(a, z)) % q
	if q // 4 < dec < q // 4 * 3:
		return 1
	else:
		return 0


def check():
	ct = [enc(0), enc(0), enc(1), enc(1)]
	pt = [0, 0, 1, 1]

	for c in ct:
		typecheck(c)
	
	for mask in range(1, 16):
		c = [0] * (n + 1)
		expected_pt = 0
		for i in range(4):
			if mask & (1 << i):
				c = [(x + y) % q for x, y in zip(c, ct[i])]
				expected_pt ^= pt[i]

		assert decrypt(c) == expected_pt

if __name__ == "__main__":

	correct = {
		"score": 1,
	}
	wrong = {
		"score": 0,
	}

	with open('/autograder/results/results.json', 'w') as f:
		try:
			check()
			f.write(json.dumps(correct))
		except Exception as e:
			print(repr(e))
			f.write(json.dumps(wrong))
