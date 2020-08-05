'''
Created on Jan 9, 2020

@author: natra
'''
import numpy as np
n=5 
for i in range(1,n+1):
    s=''
    t=''
    for j in range(1,i+1):
        s=s+str(j)
        if (i-j)>0:
            t=t+str(i-j)
    print(s+t)
    
