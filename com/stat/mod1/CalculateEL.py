'''
Created on Jan 4, 2020

@author: natraj
'''
import pandas as pd

#Read the file
df=pd.read_csv('C://NAT//ML & AI//testfiles/Inferential Statistics - Student Loan.csv')
print(df.columns) #['Customer No.', 'Exposure at Default (in lakh Rs.)', 'Recov)ery (%)',    'Probability of Default'],
df['Recovery']=df['Recovery ()']
df['LOSS']=pd.to_numeric(df['Exposure at Default (in lakh Rs.)']) - ((pd.to_numeric(df['Exposure at Default (in lakh Rs.)']) * pd.to_numeric(df['Recovery ()']))/100)
df['EL']=df['LOSS']* df['Probability of Default']
print(df.head())
print(df['EL'].sum())
