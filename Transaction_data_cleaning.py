import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

url = r"C:\Users\HP\Desktop\Joshua's files\My Photos\UPI+Transactions (1).xlsx"
df = pd.read_excel(url)

#Accounting for whitespaces and ensuring the datatype is string
df['TransactionID'] = df['TransactionID'].str.strip()
df['TransactionID'] = df['TransactionID'].astype(str)

#SPliting my column based on numerals and alphabets
df['Transaction_Obj'] = df['TransactionID'].str.split(r'(\d+)').str[0]
df['Transaction_num'] = df['TransactionID'].str.split(r'(\d+)').str[1]


#Changing data type and separating based on hyphen
df['TransactionDate'] = df['TransactionDate'].astype(str)
df['Transaction_year'] = df['TransactionDate'].str.split('-').str[0]
df['Transaction_month'] = df['TransactionDate'].str.split('-').str[1]
df['Transaction_day'] = df['TransactionDate'].str.split('-').str[2]


#Spliting a column based on space
df['bank_name'] = df['BankNameReceived'].str.split(' ').str[0]
df['bank'] = df['BankNameReceived'].str.split(' ').str[1]

#Dropping unwanted columns
df.drop(['bank_name','bank'], axis=1,inplace=True)
df.drop(['TransactionID'],axis=1, inplace=True)
df.drop(['Transaction_Obj'],axis=1, inplace=True)
df.drop(['BankNameReceived'], axis=1, inplace=True)
df.drop(['TransactionDate'], axis=1, inplace=True)

#Transforming into numerical values fit for machine models.
from sklearn.preprocessing import OneHotEncoder
OHE = OneHotEncoder()
OHE_encoded = OHE.fit_transform(df[['Gender','Status','TransactionType','PaymentMethod','PaymentMode' ]]).toarray()
OHE_df = pd.DataFrame(OHE_encoded, columns= OHE.get_feature_names_out())


from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df['BankNameSent'] = pd.DataFrame(label_encoder.fit_transform(df[['BankNameSent']]))
df['City'] = pd.DataFrame(label_encoder.fit_transform(df[['City']]))
df['DeviceType'] = pd.DataFrame(label_encoder.fit_transform(df[['DeviceType']]))
df['MerchantName'] = pd.DataFrame(label_encoder.fit_transform(df[['MerchantName']]))
df['Purpose'] = pd.DataFrame(label_encoder.fit_transform(df[['DeviceType']]))
df['Currency'] = pd.DataFrame(label_encoder.fit_transform(df[['Currency']]))

#dropping Unwanted Columns that has been transformed
df.drop(['Gender','Status','TransactionType','PaymentMethod','PaymentMode' ], axis=1, inplace=True)

Final_df = pd.concat([OHE_df,df], axis=1)