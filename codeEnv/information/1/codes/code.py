n = int(input())

l = []
x = [int(a) for a in input().split(" ")]

x.sort()

x = [str(a) for a in x]

print(" ".join(x))