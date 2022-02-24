from hashlib import sha1
import random

print("Please, enter number of elements:")
c = int(input())
#A = [0] * c
with open("input", "w") as inp:
	for i in range(c):
  		inp.write(sha1(str(random.randint(0, 100000)).encode()).hexdigest() + '\n')

