A = []
with open("input", "r") as inp:
	for line in inp:
		A = list(map(int, line[:-1].split()))
print(A)

A.sort()

with open("output", "w") as out:
	for number in A:
		out.write(str(number) + ' ')
	out.write('\n')
