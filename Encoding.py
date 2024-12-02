#importing my libraries
import seaborn as sns
import pandas as pd

#Loading my dataset from seaborn library
df = sns.load_dataset('Tips')

#Renaming of my columns
df['Bill'] = df['total_bill']

#one hot encoding 
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
encoding = encoder.fit_transform(df[['sex','smoker']]).toarray()
encoded_df = pd.DataFrame(encoding, columns=encoder.get_feature_names_out())

#Renaming of my columns
encoded_df['Female'] = encoded_df['sex_Female']
encoded_df['Male'] = encoded_df['sex_Male']

#Deleting unwanted columns
encoded_df.drop(['sex_Female','sex_Male'], axis=1, inplace=True)
df.drop(['sex','smoker'], axis=1, inplace=True)

#Label Encoding
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df['Day']= pd.DataFrame(label_encoder.fit_transform(df[['day']]))
df.drop(['day'], axis=1,inplace=True)

#Ordinal Encoder
from sklearn.preprocessing import OrdinalEncoder
Ordinal_encoding = OrdinalEncoder(categories=[['Dinner','Lunch']])
df['time'] = Ordinal_encoding.fit_transform(df[['time']])

#Final Table
Featured_table = pd.concat([encoded_df,df], axis=1)

#Targeted Ordinal Encoder
df = sns.load_dataset('Tips') #The dataset was reloaded from seaborn
df.drop(['total_bill', 'tip', 'sex', 'smoker','time'], axis=1, inplace=True)
Grouped_df = df.groupby('day')['size'].mean().to_dict()
df['day'] = df['day'].map(Grouped_df)
df.drop(['day'],axis=1,inplace=True)



