'''
Created on Jan 13, 2020

@author: natra
'''
import scipy.stats as st
#m=float(input())#mean
#sd=float(input())#standard deviation
m=100
sd=10
zscore=round(st.norm.ppf(0.90),2)
print(zscore)
#zcore=1.28
print(round(st.norm(100, 10).cdf(90),2))
x=1-round(st.norm(m, sd).cdf(90),2)
print(x)