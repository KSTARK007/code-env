import sys
import random

n = int(sys.argv[1])

for a in range(n):
	x = random.randint(1, 10000)
	arr = [random.randint(1, 10000) for b in range(x)]
	y = random.randint(1, 10000)

	with open("ip"+str(a+1), "w") as file:
		file.write(str(x)+"\n")
		file.write(" ".join([str(s) for s in  arr]))
		file.write("\n"+str(y))

	with open("op"+str(a+1), "w") as file:
		try:
			file.write(str(arr.index(y)+1))
		except:
			file.write("-1")

