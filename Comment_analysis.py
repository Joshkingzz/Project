#importing libraries
import pandas as pd
import numpy as np
import re

url = r"C:\Users\HP\Downloads\all_comments.json"
df=pd.read_json(url)

df=df.astype(str) #converting data type to string
df['Comments'] = df[0] #renaming my column
df['Comments'].str.strip() #removing whitespaces in the comments

#extracting comments with website links in them
url_pattern = r'(https?://\S+|www\.\S+)' #Define a regex pattern to match website links

#Filtering comments containing website links
web_comments_df = df[df['Comments'].str.contains(url_pattern, na=False, regex=True)]

# Saving the filtered comments to a CSV file
web_comments_df.to_csv('Web_comment.csv', index=False)

#Extract all website links from the comments
df['Websites'] = df['Comments'].apply(lambda x: re.findall(url_pattern, x) if isinstance(x, str) else [])

#Flatten the list of URLs and create a new DataFrame
websites = [url for urls in df['Websites'] for url in urls]
websites_df = pd.DataFrame(websites, columns=['Websites'])

#Save the extracted websites to a CSV file
websites_df.to_csv('only_websites.csv', index=False)

df.drop(['Websites'],axis=1,inplace=True)

df = df[~df['Comments'].str.contains(url_pattern, na=False, regex=True)] #removing comments that contains website links


words = ' '.join(df['Comments']).lower().split() #joining all the words inside a column, coverting to lower case and and spliting 

#Creating DataFrame with word 
word_df = pd.Series(words)
word_df = pd.DataFrame(word_df)

word_df['word'] = word_df[0] #Renaming the column
word_df.drop([0],axis=1,inplace=True) #dropping unwanted columns

word_df=word_df.drop_duplicates(keep='first') #Dropping duplicates
word_df['Clean'] = word_df['word'].str.replace(r'[^a-zA-Z\s]', ' ', regex=True).str.strip() #creating a new column where regular expressions are removed

word_df.drop(['word'],axis=1,inplace=True) #dropping uncleaned column
word_df=word_df.drop_duplicates(subset='Cleaned_word',keep='first') #dropping duplicates again
word_df=word_df.sort_values(by='Cleaned_word', ascending=True) #sorting words alphabetically

words_df = word_df[word_df['Clean'].str.match(r'^[A-Z][a-z]*$', na=False)] #extracting words that start with capital letter and end with small letter

# words-df was exported and app names were extracted manually and then imported back to python
import pandas as pd
url = r"C:\Users\HP\Documents\App names.csv"
df=pd.read_csv(url)
word_list = df['App names'].to_list() #converting my app names into a list

#Going back to my source file
url = r"C:\Users\HP\Downloads\all_comments.json"
df=pd.read_json(url)

df=df.astype(str) #converting data type to string
df['Comments'] = df[0] #renaming my column
df['Comments'].str.strip() #removing whitespaces in the comments
df.drop([0],axis=1,inplace=True) #removing unwanted columns

word_list  #list used for iteration

#Creating an empty list to collect the comments
App_comments = []

#Iterate over the word list and check if the word is in any comment
for word in word_list:
    Apps = df[df['Comments'].str.contains(word, case=False, na=False)] # Filter comments that contain the word (case insensitive)
    App_comments.append(Apps) # Add these filtered comments to the list

#Concatenate all filtered comments into a new DataFrame
App_df = pd.concat(App_comments).drop_duplicates().reset_index(drop=True)


#Deleting the comments that contains both appnames and website links
# unction to check if a comment contains a website link
def contains_link(text):
    return bool(re.search(r'http[s]?://\S+|www\.\S+', text)) #Re to match URLs

#Filter out rows where the 'comment' column contains a website link
Appz_df = df[~df['Comments'].apply(contains_link)]

Appz_df['Comments'] = Appz_df['Comments'].str.strip()