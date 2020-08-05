'''
Created on Jan 28, 2020

@author: natra
'''
import psycopg2 as psy
import pandas as pd
from sqlalchemy import create_engine,MetaData,Table, Column, Integer, String, TIMESTAMP
#Create connection
engine=create_engine("postgresql://postgres:secret@localhost/MLAI")
connection = engine.connect()
loanLists=pd.read_csv('loan.csv',engine='python',dtype={'next_pymnt_d': 'str'})
trans = connection.begin()
print('test 1')
loanLists.to_sql(con=connection, name='Loans2', schema='testnat', index=False, if_exists='replace',dtype={"collections_12_mths_ex_med": String()})
trans.commit()
print('test nat')
result1 = connection.execute("select member_id from testnat.loans")
for row in result1:
    print(row['member_id'])
connection.close()