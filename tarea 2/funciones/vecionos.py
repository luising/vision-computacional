import numpy as np
a = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]])
f, c = a.shape

for y in range(f):
    for x in range(c):
        xf = x - 1 if x > 0 else 0
        yf = y - 1 if y > 0 else 0
        v = a[yf:y + 2, xf:x + 2]
        print(v)
