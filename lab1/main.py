import random
import time
from multiprocessing import Process

def quicksort(nums, frst, lst, reverse = False):
   if frst >= lst: return
 
   i, j = frst, lst
   pivot = nums[random.randint(frst, lst)]
   if reverse:
    while i <= j:
        while int(nums[i][:16], 16) > int(pivot[:16], 16): i += 1
        while int(nums[j][:16], 16) < int(pivot[:16], 16): j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
    quicksort(nums, frst, j, True)
    quicksort(nums, i, lst, True)
   else:
     while i <= j:
        while int(nums[i][:16], 16) < int(pivot[:16], 16): i += 1
        while int(nums[j][:16], 16) > int(pivot[:16], 16): j -= 1
        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i, j = i + 1, j - 1
     quicksort(nums, frst, j)
     quicksort(nums, i, lst)

def merge_sort(nums, reverse = False): 
    if len(nums) > 1: 
        mid = len(nums)//2
        left = nums[:mid] 
        right = nums[mid:]
        if reverse:
          merge_sort(left, True) 
          merge_sort(right, True)
        else:
          merge_sort(left) 
          merge_sort(right)
        i = j = k = 0
        if reverse:
          while i < len(left) and j < len(right): 
              if int(left[i][:16], 16) > int(right[j][:16], 16): 
                  nums[k] = left[i] 
                  i+=1
              else: 
                  nums[k] = right[j] 
                  j+=1
              k+=1
        else:
          while i < len(left) and j < len(right):
              if  int(left[i][:16], 16) < int(right[j][:16], 16): 
                  nums[k] = left[i] 
                  i+=1
              else: 
                  nums[k] = right[j] 
                  j+=1
              k+=1    
        while i < len(left): 
            nums[k] = left[i] 
            i+=1
            k+=1
        while j < len(right): 
            nums[k] = right[j] 
            j+=1
            k+=1

def m(nums, reverse = False):
  nums1 = nums.copy()
  start1 = time.time()
  merge_sort(nums, reverse)
  t1 = time.time() - start1
  start2 = time.time()
  merge_sort(nums1, True)
  t2 = time.time() - start2
  with open("merge", "w") as out:
    for line in nums:
      out.write(line +'\n')
  print(f"merge - {t1}")
  with open("merge_rev", "w") as out:  
    for line in nums1:
      out.write(line +'\n')
  print(f"merge reverse - {t2}")

def q(nums, frst, lst, reverse = False):
  nums1 = nums.copy()
  start1 = time.time()
  quicksort(nums, frst, lst, reverse)
  t1 = time.time() - start1
  start2 = time.time()
  quicksort(nums1, frst, lst, True)
  t2 = time.time() - start2
  with open("quick", "w") as out:
    for line in nums:
      out.write(line + '\n')
  print(f"quick - {t1}")
  with open("quick_rev", "w") as out:  
    for line in nums1:
      out.write(line +'\n')
  print(f"quick reverse - {t2}")

print("Please, enter input filepath")
filepath = input()
A = []
with open(filepath, "r") as inp:
	for line in inp:
		A.append(line[:-1])
B = [i for i in A]

if __name__ == "__main__":  
   process1 = Process(target= m, args=(A, ))  
   process2 = Process(target= q, args=(B, 0, len(B) - 1, ))  
  
   process1.start()  
   process2.start()  
   
   process1.join()  
   process2.join()

