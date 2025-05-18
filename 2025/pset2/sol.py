import random
from tqdm import tqdm
from lib import KEYSIZE, enc, pi, pi_inv, read_data

if __name__ == "__main__":
	# encryption of number `x` is `ciphertexts[x]` for 0 <= x < 2 ** 20
	ciphertexts = read_data()

	mp = dict([(pi_inv(i) ^ ciphertexts[i], i) for i in range(2 ** 20)])

	for m0 in tqdm(range(2 ** 20)):
		magic = pi(ciphertexts[m0]) ^ m0

		m1 = mp.get(magic, None)
		if m1 is not None:
			key = pi_inv(m1) ^ m0

			if enc(key, 0) == ciphertexts[0]:
				print(f"Found the key: {key}")
				exit(0)