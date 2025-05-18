import random
from tqdm import tqdm
from lib import KEYSIZE, enc

if __name__ == "__main__":
	for _ in range(30):
		t = random.getrandbits(KEYSIZE)

	key = random.getrandbits(KEYSIZE)
	with open("secret.txt", "w") as f:
		f.write(f"The secret key is {key}")

	with open("data.txt", "wb") as f:
		for i in tqdm(range(2 ** 20)):
			ct = enc(key, i)
			f.write(ct.to_bytes(5, "big"))


