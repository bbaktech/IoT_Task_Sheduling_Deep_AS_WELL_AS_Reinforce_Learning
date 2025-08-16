from collections import deque
import random

import numpy as np

# val = [2,4,6,8,10,12]

# meen = 0
# for itm in val:
#     meen = meen+ itm
# meen = meen/len(val)
# print ('meen:'+str(meen))

# var = 0
# for itm in val:
#     var = var + pow((itm - meen),2)
# var = var /len(val)
# print ('var:'+ str(var))

epson = 1.0
dec_epson = .99
stop_epson = 0.01
i = 0
while epson > stop_epson:
    i+=1
    print(f"Indx: {i} Count is: {epson}")
    epson *= dec_epson
else:
    print(f"Loop finished, epson is no longer less than: {stop_epson}.")
