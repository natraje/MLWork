import pandas as pd
import numpy as np

#Read the files and convert the encoding scheme
companies=pd.read_csv('companies.txt',sep="\t", engine='python')
rounds2=pd.read_csv('rounds2.csv', engine='python')
rounds2['company_permalink']= rounds2['company_permalink'].str.encode('utf-8').str.decode('ascii', 'ignore')
companies['name']= companies['name'].str.encode('utf-8').str.decode('ascii', 'ignore')
companies['permalink']= companies['permalink'].str.encode('utf-8').str.decode('ascii', 'ignore')

## To make comparison simple convert the company names to lower case
print('Before Conversion Round, Company(name,link):',rounds2['company_permalink'].nunique(),companies['name'].nunique(),companies['permalink'].nunique())
companies['permalink']=companies['permalink'].str.lower()
rounds2['company_permalink']=rounds2['company_permalink'].str.lower()
companies['name']=companies['name'].str.lower()
print('After Conversion Round, Company(name,link):',rounds2['company_permalink'].nunique(),companies['name'].nunique(),companies['permalink'].nunique())

# Data Cleanng start 
#Find a duplicated and decide on the index key for company 
bool_series = companies['name'].duplicated()

print('Dup by Name:',companies['name'].nunique())
companies['name'].fillna( method ='backfill', inplace = True) 
CDf1=companies['permalink']
#companies.set_index('permalink',inplace=True)
##Find no of rows not present in Rounds table y comparing with company
notprsnt=rounds2[~rounds2['company_permalink'].isin(companies['permalink'])].size
companies.set_index('permalink',inplace=True)
print(rounds2.size)
#master_frame=rounds2.merge(companies, left_on='company_permalink', right_on='permalink')
master_frame=pd.merge(rounds2,companies, how='inner', left_on='company_permalink', right_on='permalink')
print(master_frame.head(5))

#CheckPint 

# Top 3 english countries
top3=pd.DataFrame({'Rank': [1,2,3],
         'code': ['USA', 'GBR', 'IND']})
country1=top3.loc[0].code
country2=top3.loc[1].code
country3=top3.loc[2].code

## Calculate average funding by requestd investment type and print them

oneMillion=1000000
ventureAvg=master_frame[master_frame['funding_round_type']=='venture']['raised_amount_usd'].mean()/oneMillion
print('Venture:',ventureAvg)
angelAvg=master_frame[master_frame['funding_round_type']=='angel']['raised_amount_usd'].mean()/oneMillion
print('Angel:',angelAvg)
seedAvg=master_frame[master_frame['funding_round_type']=='seed']['raised_amount_usd'].mean()/oneMillion
print('Seed:',seedAvg)
peAvg=master_frame[master_frame['funding_round_type']=='private_equity']['raised_amount_usd'].mean()/oneMillion
print('PE:',peAvg)

## Define the Ft
FT='venture'

master_frame.head()
top9=master_frame.groupby('country_code')['raised_amount_usd'].sum().sort_values(ascending=False).head(9)
print('Top 9 Countries details:',top9)

#Working with Sectors
## Parse the sector file and convert them as row mapping from column
main_sector=pd.read_csv('mapping.csv', engine='python')
main_sector
main_sector = main_sector.melt(id_vars="category_list",var_name="master_category")
# Convert columns as a sigle colum and remove the non primary sectors
main_sector = main_sector.loc[~(main_sector["value"]==0) ]
main_sector=main_sector.drop(columns="value")

# Remove the blank column
#print('mainsector:',main_sector.shape)
main_sector=main_sector[pd.notnull(main_sector['category_list'])]


#print('mainsector:',main_sector.shape)
## Checkpoint 5: 
#ventureOnly = master_frame[master_frame['funding_round_type']==FT]
startRange=5*oneMillion
maxRange=15*oneMillion
def getPS(sec): 
  return str(sec).split('|')[0]
print(master_frame.shape)
dfByRangeFT=master_frame[(master_frame['raised_amount_usd']>=startRange) & (master_frame['raised_amount_usd']<=maxRange )]
dfByRangeFT['primary_sector']=dfByRangeFT['category_list'].apply(getPS)
print(dfByRangeFT.shape)
#print(dfByRangeFT['raised_amount_usd'].max())
#print(dfByRangeFT.shape)
dfByRangeFT=pd.merge(dfByRangeFT,main_sector, how='left', left_on='primary_sector', right_on='category_list')
print(dfByRangeFT.head())
dfByRangeFT.rename(columns = {'master_category':'main_sector'}, inplace = True) 
#print(dfByRangeFT.head())
#print(dfByRangeFT.shape)
D1=dfByRangeFT.loc[dfByRangeFT.country_code==country1]
D2=dfByRangeFT.loc[dfByRangeFT.country_code==country2]
D3=dfByRangeFT.loc[dfByRangeFT.country_code==country3]
print('D1:',len(D1),(D1['raised_amount_usd'].sum()/oneMillion))
print('D2:',len(D2),(D2['raised_amount_usd'].sum()/oneMillion))
print('D3:',len(D3),(D3['raised_amount_usd'].sum()/oneMillion))
top3CountD1=D1.groupby('main_sector')['raised_amount_usd'].count().sort_values(ascending=False).head(3)
top3CountD2=D2.groupby('main_sector')['raised_amount_usd'].count().sort_values(ascending=False).head(3)
top3CountD3=D3.groupby('main_sector')['raised_amount_usd'].count().sort_values(ascending=False).head(3)
print(top3CountD1)
print(top3CountD2)
print(top3CountD3)

topCompanyD1=D1.groupby('name')['raised_amount_usd'].count().sort_values(ascending=False).head(2)
topCompanyD2=D2.groupby('name')['raised_amount_usd'].count().sort_values(ascending=False).head(2)
topCompanyD3=D3.groupby('name')['raised_amount_usd'].count().sort_values(ascending=False).head(2)
print(topCompanyD1)
print(topCompanyD2)
print(topCompanyD3)

#print(main_sector['master_category'].unique())
#print(D1['main_sector'].unique())
#print(D1['category_list'].str.contains(pat = 'is'))