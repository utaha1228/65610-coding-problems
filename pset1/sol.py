from Crypto.Util.number import *

lb = [None] * 128

def add(n):
	for i in range(128):
		if n & (1 << i):
			if lb[i] is None:
				lb[i] = n
				return 0
			else:
				n ^= lb[i]
	return n

def main():
	pts = []
	cts = []
	with open("data.txt", "r") as f:
		for i in range(150):
			line = f.readline().strip()
			pt, ct = map(bytes.fromhex, line.split(" "))
			pts.append(pt)
			cts.append(ct)
	
	base = bytes_to_long(pts[0] + cts[0])
	for i in range(1, 150):
		add(bytes_to_long(pts[i] + cts[i]) ^ base)

	pt = b""
	with open("ciphertext.txt", "rb") as f:
		ct = f.read()

	for i in range(0, len(ct), 16):
		cur = bytes_to_long(ct[i:i+16])
		cur ^= base
		ret = add(cur)
		ret >>= 128
		pt += long_to_bytes(ret, 16)
	print(pt)


if __name__ == "__main__":
	main()