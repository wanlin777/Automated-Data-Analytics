
#!/usr/bin/env python
# coding: utf-8

import os, sys
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default='Sample4.xlsx')
parser.add_argument('-l','--line', default=1, help = '')
opts = parser.parse_args()
# print(args.accumulate(args.integers))

newDataFrame = dict()
try:
    df = pd.read_excel('Sample4.xlsx')
except:
    print("No data detected...")
    os._exit(0)

feature = df.iloc[int(opts.line)].tolist()
features = df.keys()
personInfo = features[:-5]
prop = features[-5:]
print('Personal info', personInfo.tolist(), 'and property', prop.tolist())
propNum = [i[-1] for i in df[prop].select_dtypes(include = np.number).columns.tolist()]
propCat = [i[-1] for i in df[prop].select_dtypes(exclude = np.number).columns.tolist()]
print('Splitting properties into numerical property', propNum, 'and categorical property', propCat)
for item in ['personalInfo', 'numericalProperty', 'categoricalProperty']: newDataFrame.update({item :[]})
for info in feature[:-5]: newDataFrame['personalInfo'].append(info)
if newDataFrame['personalInfo'][2] != 'nan': newDataFrame['personalInfo'][2] = int(newDataFrame['personalInfo'][2])
if newDataFrame['personalInfo'][3] != 'nan': ssn = str(int(newDataFrame['personalInfo'][3])); newDataFrame['personalInfo'][3] = str(ssn[0:3] + '-' + ssn[3:5] + '-' + ssn[5:]); 
for ind in propNum: newDataFrame['numericalProperty'].append(feature[-5:][int(ind) -1])
for ind in propCat: newDataFrame['categoricalProperty'].append(feature[-5:][int(ind) - 1])
print('New row in the new dataframe', newDataFrame)

#display feature importance
total_col=len(df.columns) 
total_rows=len(df)
print("number of property columns:",total_col-5,"number of property rows:",total_rows)
df_prop=df.iloc[:,5:(total_col)]
#print(df_prop)

numeric_header=[]
categorical_header=[]
for i in propNum: 
    numeric_header+=[df_prop.columns[int(i)-1]]
for i in propCat:
    categorical_header+=[df_prop.columns[int(i)-1]]
print("numeric properties header:",numeric_header,"categorical_header:",categorical_header)

num_prop=df_prop.loc[:,numeric_header]
cat_prop=df_prop.loc[:,categorical_header]
#print(numeric_prop)
#print(cat_prop)


#data cleaning: Null info of df
df_null = df.isnull().sum()
print("Null sum is:",df.isnull().sum())

#For numerical prop, fill null with mean
num_prop=df_prop.loc[:,numeric_header]
#num_prop.isnull.sum()
for col in num_prop.columns:
    num_prop[col].fillna(num_prop[col].mean(), inplace = True)

#For categorical prop, fill null with 'other'
cat_prop=df_prop.loc[:,categorical_header]
for col in cat_prop.columns:
    cat_prop[col].fillna('others',inplace = True)

#data cleaning: Null info of df
df_null = df.isnull().sum()
print("Null sum after processing is:",num_prop.isnull().sum())
print("Null sum after processing is:",cat_prop.isnull().sum())

#Label encoding:convert categorical columns into numeric columns
stacked = cat_prop.stack().astype('category')
le_cat_prop = stacked.cat.codes.unstack()
#print(le_cat_prop)

new_num_prop=pd.concat([num_prop,le_cat_prop],axis = 1)
print(new_num_prop.head(3))

#display correlation table
corr=new_num_prop.corr()
print("Correlation Table:",corr.head(3))

#set threshold=0.9
threshold=0.9
print("Here we use threshold---0.9 to be our cut-off.")
columns = np.full((corr.shape[0],), True, dtype=bool)
for i in range(corr.shape[0]):
    for j in range(i+1, corr.shape[0]):
        if corr.iloc[i,j]>=threshold:
            if columns[j]:
                columns[j]=False
selected_columns=new_num_prop.columns[columns]
num_prop_updated=new_num_prop[selected_columns]

selectedCol_header=[]
for i in range(len(selected_columns)): 
    selectedCol_header+=[selected_columns[i]]
print("selected property:",selectedCol_header)

#Visualization
#df = pd.read_excel('Sample.xlsx') # File Name

print(df.head())

print(df.dtypes)

def hm(df):
    plt.subplots(figsize=(len(df.columns),len(df.columns)))
    sns.heatmap(df.corr(), annot=True, vmax=1, square=True, cmap="Reds")
img=hm(df.corr())
print(img)

plt.savefig('Group4_HeatMap')
plt.close(img)
#----------

col = df.columns
i = 0
while i < len(col):
    print(col[i])
    i += 1

#---------


col = df.columns
i = 0

while i < len(col):
    if df[col[i]].dtype.name == 'int64':

        plt.figure(i)
        sns.distplot(df[col[i]], kde=False)
        
        plt.savefig('Group4_%s' %df[col[i]].name)
    
    elif df[col[i]].dtype.name == 'object':

        plt.figure(i)
        sns.countplot(x=df[col[i]].name, data=df, order=df[col[i]].value_counts().index)
        
        plt.savefig('Group4_%s' %df[col[i]].name)
        
    elif df[col[j]].dtype.name == 'float64':

        plt.figure(i)
        sns.boxplot(x=df[col[i]])        
        
        plt.savefig('Group4_%s' %df[col[i]].name)
        
    else:
        print('XXX')
    i += 1
    
#----------
#df.groupby('First_Name_Customer').count()
