import random
from party import Party

n = 50            # number of parties
p = 2 ** 64 - 59  # modulus

def main():
	# generate shares for x and y
	x = random.randrange(0, p)
	y = random.randrange(0, p)
	x_shares = generate_shares(x)
	y_shares = generate_shares(y)

	# preprocess triplets
	A = random.randrange(0, p)
	B = random.randrange(0, p)
	AB = A * B % p
	triplets = []
	for t in zip(generate_shares(A), generate_shares(B), generate_shares(AB)):
		triplets.append(t)

	# Initiate all the parties
	parties = []
	for i in range(n):
		parties.append(Party(x_shares[i], y_shares[i], triplets[i], p))
	
	# Start computation
	info = None
	output = None
	for round_num in range(100):
		results = []
		for i in range(n):
			results.append(parties[i].run(info))
		# each result has to be a tuple in one of the following forms
		#   * ("reconstruct", share: int)
		#   * ("submit", share: int)

		assert all(results[i][0] == results[0][0] for i in range(n)), "All parties have to agree on the action"

		if results[0][0] == "reconstruct":
			info = sum(results[i][1] for i in range(n)) % p
		elif results[0][0] == "submit":
			output = sum(results[i][1] for i in range(n)) % p
			break
		else:
			raise 

	assert output == x * y % p, "Wrong result"
	print("Success")

def generate_shares(val):
	shares = [random.randrange(0, p) for _ in range(n-1)]
	return shares + [(val - sum(shares)) % p]

if __name__ == "__main__":
	main()