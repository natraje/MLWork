'''
Created on Jan 8, 2020

@author: natra
'''
import numpy as np
import pandas as pd
import scipy.stats as st
import math

score=float(input("Enter your Confidence:"))

df=pd.read_csv('C://NAT//ML & AI//testfiles/Inferential Statistics - Powai Flats Rent.csv')
mean1 = df['Monthly Rent'].mean()
print(mean1)
std1 = df['Monthly Rent'].std() 
print(std1)
max1 = df['Monthly Rent'].max()
min1 = df['Monthly Rent'].min()
Nsize = df['Monthly Rent'].count()
print(Nsize)
median1 = df['Monthly Rent'].median() 
std1 = df['Monthly Rent'].std() 
var1 = df['Monthly Rent'].var()
print(score/100)
zscore=st.norm.ppf((score/100))  #st.norm.cdf(1.64)
print(zscore)
std1=7438.85
margin_of_error = ((zscore*std1)/math.sqrt(Nsize))
ConfIntervalMin=mean1-margin_of_error
ConfIntervalMax=mean1+margin_of_error
print(ConfIntervalMin,',',ConfIntervalMax)