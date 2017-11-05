import math
import sys

n = int(sys.argv[1])

count = 0

for k in range(1, n+1):
    count += math.factorial(n)/(math.factorial(n-k)*math.factorial(k))

print(count)