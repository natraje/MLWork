'''
Created on Feb 13, 2020

@author: natra
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels
import statsmodels.api as sm
import sklearn

#Read the file
advertisingDF=pd.read_csv('C://NAT//ML & AI//testfiles/ML1/advertising.csv')
print('Columns:',advertisingDF.columns)
print(advertisingDF.head())
print('Size:',advertisingDF.shape)
print(advertisingDF.info())
print('Summary of the dataframe\n',advertisingDF.describe())

#Visualize the dataset to further analyse
sns.set(color_codes=True)
sns.regplot(x='TV', y='Sales', data=advertisingDF,color="g") ## Green color

sns.regplot(x='Radio', y='Sales', data=advertisingDF,color="b") ## Blue colour
sns.regplot(x='Newspaper', y='Sales', data=advertisingDF,color="r") ## Red
plt.show()

# Regplot is not good for comparison and Pairplot should be used to compare the data columns
sns.pairplot(x_vars=['TV','Radio','Newspaper'], y_vars='Sales', data=advertisingDF) 
plt.show()