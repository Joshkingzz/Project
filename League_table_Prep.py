#Importing libraries
import pandas as pd
from io import StringIO

#Getting my data table from the internet and filtering
url = 'https://www.premierleague.com/tables'   
df = pd.read_html(url, match='Position',header=0)[0]

df=df.iloc[::2] #Removing the alternate rows that are not needed
df = df.reset_index() ##reseting the index

#Dropping unwanted tables
df.drop(['index'], axis=1, inplace=True) #3deleting index and unnamed columns
df.drop(['Unnamed: 12'], axis=1, inplace=True)

#Renaming and dropping unwanted Tables
df['Position'] = df['Position  Pos'].str.split(' ').str[0]
df.drop(['Position  Pos'],axis=1, inplace=True)

#Column rearrangement
last_column = df.columns[-1]
df = df[[last_column] + list(df.columns[:-1])]


df['Club']= df['Club'].astype(str) #Changing data type
df['Club']= df['Club'].str.strip() #Striping white spaces
df['Abb'] = df['Club'].str.extract(r'([A-Z]+)$')  # Extract the uppercase abbreviation at the end
df['Team'] = df['Club'].str.replace(r'([A-Z]+)$', '', regex=True).str.strip() #replacing the extracxted values with space
df.drop(['Club'], axis=1, inplace = True) #Dropping the table


#Rearranging the columns
last_two_columns = df.columns[-2:] 
remaining_columns = df.columns[:-2]
df = df[list(last_two_columns) + list(remaining_columns)]


#Spliting a couln and assigning names to a column
df['Form'] = df['Form'].str.strip()
df['Win form'] =df['Form'].str.split(' ').str[0]
#df['Win Day'] =df['Form'].str.split(' ').str[1]
df['Win Day'] =df['Form'].str.split(' ').str[2]
df['Date'] =df['Form'].str.split(' ').str[3]
df['Month'] =df['Form'].str.split(' ').str[4]
df['Year'] =df['Form'].str.split(' ').str[5]
#df['Win team'] =df['Form'].str.split(' ').str[6]

#Renaming column
df['Next Match'] =df['Next'].str.split(' ').str[0]

#Dropping unwanted colummns
df.drop(['Form'], axis=1, inplace= True)
df.drop(['Next'], axis=1, inplace= True)

#Transforming for machine learning
from sklearn.preprocessing import OneHotEncoder
encoded = OneHotEncoder()
M_encoder = encoded.fit_transform(df[['Month']]).toarray()
M_df = pd.DataFrame(M_encoder, columns=encoded.get_feature_names_out())

F_encoder = encoded.fit_transform(df[['Win form']]).toarray()
F_df = pd.DataFrame(F_encoder, columns=encoded.get_feature_names_out())

D_encoder = encoded.fit_transform(df[['Win Day']]).toarray()
D_df = pd.DataFrame(D_encoder, columns=encoded.get_feature_names_out())

from sklearn.preprocessing import LabelEncoder
Lbl_encoded = LabelEncoder()
df['Team'] = pd.DataFrame(Lbl_encoded.fit_transform(df[['Team']]))
df['Next Match'] = pd.DataFrame(Lbl_encoded.fit_transform(df[['Next Match']]))
df['Abb'] = pd.DataFrame(Lbl_encoded.fit_transform(df[['Abb']]))

df.drop(['Win Day', 'Month','Win form'], axis=1,inplace=True) #dropping unwanted column

Final_df = pd.concat([df,M_df,D_df,F_df], axis=1)
