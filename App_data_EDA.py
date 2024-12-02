#importing important Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#acessing the dataset to be analysed
url=r"C:\Users\HP\Downloads\Play Store Data.csv"
df=pd.read_csv(url)

#thorough inspection was made on the data set
df.head(2)
df.info()
df.describe()
df.isnull().sum()

#Observations and insights
df['Reviews'].unique() #To check for uniques values
df['Reviews'].str.isnumeric().sum() #to check for sum of numeric values
df[~df['Reviews'].str.isnumeric()] #to acess the row that has a non numeric value

#to avoid tampering the original dataset, let me create a copy, run my tests and then used the codes used to clean to apply to thr main data set
df_copy=df.copy()
df_copy=df_copy.drop(df_copy.index[10472]) #to delete a complete row

df_copy[~df_copy['Reviews'].str.isnumeric()] #to check if there are other rows where the reviews are non numeric

df_copy['Reviews'].astype(int) #converting it back to integers

df_copy.Size.unique() #checking for unique values

#replacing and making the values in the column to be uniform
df_copy['Size']=df_copy['Size'].str.replace('M','000')
df_copy['Size']=df_copy['Size'].str.replace('K','')
df_copy['Size']=df_copy['Size'].str.replace('k','')
df_copy['Size']=df_copy['Size'].replace('Varies with device',np.nan)
df_copy['Size']=df_copy['Size'].astype(float)

#checking for unique values
df_copy['Installs'].unique() 
df_copy['Price'].unique()

#To clean the install and price columns simultaneously
Not_needed =['+',',','$']
columns_to_clean=['Installs','Price']
for item in Not_needed:
    for cols in columns_to_clean:
        df_copy[cols]=df_copy[cols].str.replace(item,' ')

#changing datatypes from str to integer and float respectively
df_copy['Installs']=df_copy['Installs'].astype(int)
df_copy['Price']=df_copy['Price'].astype(float)

#converted to a dataframe and then seperate date, month and year automatically
df_copy['Last Updated']=pd.to_datetime(df_copy['Last Updated'])
df_copy['Day']=df_copy['Last Updated'].dt.day
df_copy['Month']=df_copy['Last Updated'].dt.month
df_copy['Year']=df_copy['Last Updated'].dt.year

df_copy.drop(['Last Updated'],axis=1,inplace=True) #Deleting the unwanted column

#replacing missing values with the mode
mode_value = df_copy['Rating'].mode()[0]
df_copy['Rating'] = df_copy['Rating'].fillna(mode_value,inplace=False)

#observation
#duplicates observed, so we have to drop them
#the keep='first' is to retain the first original figure
df_copy['App'].duplicated().sum()
df_copy.drop_duplicates(subset=['App'],keep='first')
df_copy.head(1)

#to separate between categorical and numerical columns
numeric_features = [x for x in df_copy.columns if df_copy[x].dtype != 'O']
categorical_features = [x for x in df_copy.columns if df_copy[x].dtype == 'O']

#Data vizualization, although id always use Power BI for most of my Data visualization
# Proportion of count data on numerical columns
plt.figure(figsize=(15, 15))
plt.suptitle('Univariate Analysis of Numerical Features', fontsize=20, fontweight='bold', alpha=0.8, y=1.)

for i in range(0, len(numeric_features)): #Used to iterate over the number of numerical columns
    plt.subplot(5, 3, i+1)
    sns.kdeplot(x=df_copy[numeric_features[i]],shade=True, color='red')
    plt.xlabel(numeric_features[i])
    plt.tight_layout()


# categorical columns, count plot is always for categorical fetrures
plt.figure(figsize=(20, 15))
plt.suptitle('Univariate Analysis of Categorical Features', fontsize=20, fontweight='bold', alpha=0.8, y=1.)
category = [ 'Type', 'Content Rating']
for i in range(0, len(category)):
    plt.subplot(2, 2, i+1)
    sns.countplot(x=df[category[i]],palette="Set2")
    plt.xlabel(category[i])
    plt.xticks(rotation=45)
    plt.tight_layout() 

#plotting a pie chart
df_copy['Category'].value_counts().plot.pie(y=df_copy['Category'],figsize=(15,15))

#Converting my categorical series into a dataframe based on count
Category=pd.DataFrame(df['Category'].value_counts())
Category.rename(columns={'Category':'count'},inplace=True)

# top 10 app categories
plt.figure(figsize=(15,16))
sns.barplot(x=Category.index[:10], y ='count',data = Category[:10],palette='hls')
plt.title('Top 10 App categories')
plt.xticks(rotation=90)
plt.show()

#category with the highest number of installs
df_cat_installs = df_copy.groupby(['Category'])['Installs'].sum().sort_values(ascending = False).reset_index() #The group by function was used to make it easy
df_cat_installs.Installs = df_cat_installs.Installs/1000000000# converting into billions
df2 = df_cat_installs.head(10)
plt.figure(figsize = (14,10))
sns.set_context("talk")
sns.set_style("darkgrid")
ax = sns.barplot(x = 'Installs' , y = 'Category' , data = df2 )
ax.set_xlabel('No. of Installations in Billions')
ax.set_ylabel('')
ax.set_title("Most Popular Categories in Play Store", size = 20)

#Visualisation of four categorised apps
dfa = df_copy.groupby(['Category' ,'App'])['Installs'].sum().reset_index()
dfa = dfa.sort_values('Installs', ascending = False)
apps = ['GAME', 'COMMUNICATION', 'PRODUCTIVITY', 'SOCIAL' ]
sns.set_context("poster")
sns.set_style("darkgrid")
plt.figure(figsize=(40,30))

for i,app in enumerate(apps):
    df2 = dfa[dfa.Category == app]
    df3 = df2.head(5)
    plt.subplot(4,2,i+1)
    sns.barplot(data= df3,x= 'Installs' ,y='App' )
    plt.xlabel('Installation in Millions')
    plt.ylabel('')
    plt.title(app,size = 20)
    
plt.tight_layout()
plt.subplots_adjust(hspace= .3)
plt.show()

#top rating apps
rating = df_copy.groupby(['Category','Installs', 'App'])['Rating'].sum().sort_values(ascending = False).reset_index()
toprating_apps = rating[rating['Rating'] == 5.0] ##this is used to sort for columns within a dataframe that has rating 5.0
toprating_apps.head(5)