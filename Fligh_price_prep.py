#to import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#accesses data to be analysed
file_path=r"C:\Users\HP\Downloads\flight_price.xlsx"
df=pd.read_excel(file_path)

#drops the route coluns permamnently
df.drop(['Route'],inplace=True,axis=1)

#encodes the columns to be fit for machine learning
from sklearn.preprocessing import OneHotEncoder
encoder=OneHotEncoder()
encoded=encoder.fit_transform(df[['Airline','Source','Destination','Additional_Info']]).toarray()
Encoded_df=pd.DataFrame(encoded,columns=encoder.get_feature_names_out())

#drops the colums not needed
df.drop(['Airline','Source','Destination','Additional_Info'],axis=1,inplace=True)

#Filling the missing values with the mode and then assigning numerical values using map function
mode_value=df['Total_Stops'].mode()[0] 
df['Total_Stops']=df['Total_Stops'].fillna(mode_value, inplace=False)
df['Total_Stops']=df['Total_Stops'].map({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4})

#Spliting date of journey and coverting into integers making it fit for machine learning.
df['Date']=df['Date_of_Journey'].str.split('/').str[0]
df['Month']=df['Date_of_Journey'].str.split('/').str[1]
df['Year']=df['Date_of_Journey'].str.split('/').str[2]
df['Date']=df['Date'].astype(int)
df['Month']=df['Month'].astype(int)
df['Year']=df['Year'].astype(int)

#Spliting dparture time and coverting into integers making it fit for machine learning.
df['Dep_hour']=df['Dep_Time'].str.split(':').str[0]
df['Dep_minute']=df['Dep_Time'].str.split(':').str[1]
df['Dep_hour']=df['Dep_hour'].astype(int)
df['Dep_minute']=df['Dep_minute'].astype(int)

#Performing a nested spliting to split the column
df['Duration_hour']=df['Duration'].str.split(' ').str[0].str.split('h').str[0]
df['Duration_minute']=df['Duration'].str.split(' ').str[1].str.split('m').str[0]

#FIlling the missing values with zero, replacing values with M and converting to integers
mode_value=df['Duration_minute'].mode()[0] 
df['Duration_minute']=df['Duration_minute'].fillna(mode_value, inplace=False)
df['Duration_hour'].replace('5m', '5', inplace=True)
df['Duration_hour']=df['Duration_hour'].astype(int)
df['Duration_minute']=df['Duration_minute'].astype(int)

#using lambda function to separate some values as the data strcture is not consistent
df['Arrival_Time']=df['Arrival_Time'].apply(lambda x:x.split(' ')[0])
df['Arrival_hour']=df['Arrival_Time'].str.split(':').str[0]
df['Arrival_min']=df['Arrival_Time'].str.split(':').str[1]

#drops the colums not needed
df.drop(['Date_of_Journey'],axis=1,inplace=True)
df.drop(['Dep_Time'], axis=1,inplace=True)
df.drop(['Duration'],inplace=True,axis=1)

final_df=pd.concat([Encoded_df,df],axis=1)


##to access data on a large scale
numeric_features = [x for x in df_copy.columns if df_copy[x].dtype != 'O']
categorical_features = [x for x in df_copy.columns if df_copy[x].dtype == 'O']

# print columns
print('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
print('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))






