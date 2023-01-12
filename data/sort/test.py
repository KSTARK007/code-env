import sys
import random

n = int(sys.argv[1])

for a in range(n):
	x = random.randint(1, 10000)
	arr = [random.randint(1, 10000) for b in range(x)]

	with open("ip"+str(a+1), "w") as file:
		file.write(str(x)+"\n")
		file.write(" ".join([str(s) for s in  arr]))

	arr.sort()
	with open("op"+str(a+1), "w") as file:
		file.write(" ".join([str(s) for s in  arr]))

