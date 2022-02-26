Check = ["merge", "merge_rev", "quick", "quick_rev"]
for j in range(4):
  ok = 1
  with open(Check[j], "r") as s:
    A = s.readlines()
  if j % 2 == 0:
    for i in range(1, len(A) - 1):
      if int(A[i][:16], 16) < int(A[i - 1][:16], 16):
        print("Error, don`t right sort")
        ok = 0
        break
  else:
    for i in range(1, len(A) - 1):
      if int(A[i][:16], 16) > int(A[i - 1][:16], 16):
        print("Error, don`t right sort")
        ok = 0
        break
  if ok == 1:
    print(f"Sort {Check[j]} is right")
