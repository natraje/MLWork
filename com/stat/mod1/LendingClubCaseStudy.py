'''
Created on Jan 28, 2020

@author: natra
'''
## Section 1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

pd.set_option('display.max_columns', None)

#Loading the file into dataframe
orgLoanLists=pd.read_csv('loan.csv',engine='python')
print('Total Size (Row,Column)',orgLoanLists.shape)  ##39717

# Dropping the columns which does not have values
loanLists = orgLoanLists.dropna(axis = 1, how ='all') 

print('Total Size after removing NA columns (Row,Column)',loanLists.shape) 
loanLists.drop(columns=['policy_code', 'id','desc','url'],axis=1,inplace=True)
print('Total Size after removing irrelevant columns (Row,Column)',loanLists.shape) 
# Find the unique value columns and drop them
uniqueValCols=[]
for col in loanLists.columns:
    if (len(loanLists[col].unique())) == 1:
        uniqueValCols.append(col)
loanLists.drop(columns=uniqueValCols,axis=1,inplace=True)
print('Total Size after removing unique value cols (Row,Column)',loanLists.shape)

# Based on the meta data analysis mths_since_last_record and next_pymnt_d columns not needed
loanLists.drop(columns=['mths_since_last_record','next_pymnt_d'],axis=1,inplace=True)
print('Total Size after removing irrelevant value cols (Row,Column)',loanLists.shape)
loanLists.head(5)

## Section 2
# Analyze the data dictionary to identify the coulmn types
metadata = pd.read_excel('Data_Dictionary.xlsx') # Loading in the data dictionary
print('Data dictionary size (row,columns)',metadata.shape[0])
metadata=metadata[metadata.LoanStatNew.isin(loanLists.columns)]
print('Data dictionary size after trimming (row,columns)',metadata.shape[0])
metadata = metadata.rename(columns={'LoanStatNew': 'column', 'Description': 'description'})

# Find the datatype and merge
loanLists_dtypes = pd.DataFrame(loanLists.dtypes,columns=['dtypes'])
loanLists_dtypes = loanLists_dtypes.reset_index()
loanLists_dtypes['column'] = loanLists_dtypes['index']
loanLists_dtypes = loanLists_dtypes[['column','dtypes']]
loanLists_dtypes['first value'] = loanLists.loc[0].values
ddwithTypeList = loanLists_dtypes.merge(metadata, on='column',how='left')
ddwithTypeList.head(46)

## Section 3
#### member_id - System generated value 
#### Lending club assigns interest rate based on grade drop sub grade and interest rate (refer: https://www.lendingclub.com/investing/investor-education/interest-rates-and-fees)
#### Drop zip_code: It is not given completely and instead state can be used 
#### Funded columns are future columns derived after approval and hence not needed for analysis
#### Overhead columns like emp_title
#### Remove columns with more than 1% empty values
##'total_rec_prncp',
missingValues=round(100*(loanLists.isnull().sum()/len(loanLists.index)),2) ## What % values is null in each column
print('Missing Values %:',missingValues)
futureDerivedColumns=['funded_amnt','funded_amnt_inv','issue_d','out_prncp','out_prncp_inv','total_pymnt','total_pymnt_inv','total_rec_int','total_rec_late_fee','recoveries','collection_recovery_fee','last_pymnt_d','last_pymnt_amnt']
autogeneratedcols=['member_id']
redundantcols=['int_rate','sub_grade','emp_title','zip_code']
novalueCols=['collections_12_mths_ex_med','chargeoff_within_12_mths','tax_liens']
#Drop columns which has more than 1% empty values
toomanyNAValCols=['pub_rec_bankruptcies','mths_since_last_delinq']
loanLists.drop(columns=futureDerivedColumns,axis=1,inplace=True)
loanLists.drop(columns=autogeneratedcols,axis=1,inplace=True)
loanLists.drop(columns=redundantcols,axis=1,inplace=True)
loanLists.drop(columns=novalueCols,axis=1,inplace=True)
loanLists.drop(columns=toomanyNAValCols,axis=1,inplace=True)
print('Total Size after removing based analysis (Row,Column)',loanLists.shape)
loanLists.head(5)

## Section 4
## Risk prediction has to be done for the fully paid loans and defaulted loans. So the data set need to
## be filtered only for fully paid and defaulted categories
# Further analysis on the rest of the coumns

#print(loanLists["loan_status"].value_counts())
print('Total rows before filtering -',loanLists.shape)
## Filter only fully paid and chrged off loans since that is relevant to the analysis
desiredLoans=loanLists[(loanLists.loan_status=='Charged Off') | (loanLists.loan_status=='Fully Paid')]
print('Total rows after filtering -',desiredLoans.shape)
#print(desiredLoans["verification_status"].value_counts())
#desiredLoans=desiredLoans.replace(to_replace = np.nan, value =0)
desiredLoans["verification_status"]=loanLists["verification_status"].replace(to_replace ="Source Verified", value ="Verified")
mapping_dictionary = {"loan_status":{ "Fully Paid": 1, "Charged Off": 0}}
desiredLoans = desiredLoans.replace(mapping_dictionary)
desiredLoans.head(5)

## Further analyze on the columns to find the categorical values
## title and purpose looks similar and do some more research on these 
## Based on the coulmn type, revol_util and terms looks like a numbers (int and float)
print("Data types and their frequency in desired set \n{}".format(desiredLoans.dtypes.value_counts()))
object_columns_df = desiredLoans.select_dtypes(include=['object'])
print(object_columns_df.iloc[0])
print(desiredLoans["term"].value_counts())
desiredLoans['revol_util'] = desiredLoans['revol_util'].str.rstrip('%').astype('float')
desiredLoans['term'] = desiredLoans['term'].str.rstrip(' months')
object_columns_df1 = desiredLoans.select_dtypes(include=['object'])
print(object_columns_df1.iloc[0])

print(desiredLoans.columns)
print(desiredLoans["purpose"].value_counts())
print(desiredLoans["title"].value_counts())

## Since title is derived column of purpose, we could drop title
desiredLoans.drop(columns=['title'],axis=1,inplace=True)
print(desiredLoans.shape)
print(desiredLoans.head(5))

## Find out the categorical values
print(desiredLoans["term"].value_counts())
print(desiredLoans["grade"].value_counts())
print(desiredLoans["term"].value_counts())
print(desiredLoans["emp_length"].value_counts())
print(desiredLoans["home_ownership"].value_counts())
print(desiredLoans["verification_status"].value_counts())
print(desiredLoans["purpose"].value_counts())
print(desiredLoans["addr_state"].value_counts())

map_dict_el_gr = {
"emp_length": {
"10+ years": 10,
"9 years": 9,
"8 years": 8,
"7 years": 7,
"6 years": 6,
"5 years": 5,
"4 years": 4,
"3 years": 3,
"2 years": 2,
"1 year": 1,
"< 1 year": 0,
"n/a": 0
},
"grade":{
"A": 1,
"B": 2,
"C": 3,
"D": 4,
"E": 5,
"F": 6,
"G": 7
}
}
#desiredLoans = desiredLoans.replace(map_dict_el_gr)
print(desiredLoans.describe())

## Section 5