import numpy as np
table = np.full(3268760, 255, dtype=np.uint8, order='C')
table[-1]=0

table.tofile("v10_fevertime_table.bin")




















