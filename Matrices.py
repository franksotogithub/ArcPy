import numpy as np
a = np.array([[3, 2], [6, 2], [3, 6], [3, 4], [5, 3]])
idx=np.lexsort((a[:,1],a[:,0]))

print a
print a[idx]


