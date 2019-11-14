import sys
import random

def factorial(n):
	if n==0:
		return 1
	return n*factorial(n-1)

n = int(sys.argv[1])

for a in range(n):
	x = random.randint(1, 40)

	with open("ip"+str(a+1), "w") as file:
		file.write(str(x)+"\n")

	with open("op"+str(a+1), "w") as file:
		file.write(str(factorial(x)))
