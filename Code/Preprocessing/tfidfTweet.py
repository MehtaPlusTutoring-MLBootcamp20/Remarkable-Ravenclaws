import numpy as np 
import pandas as pd 
from datetime import date, timedelta, datetime
import time
import csv

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
start_date = date(2020, 4, 12)
end_date = date(2020, 7, 13) #end date, datetime.date(datetime.now()) (this second option is dynamic and changes by date but depends on timezone)

state_names = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
states = pd.get_dummies(state_names)
#print(states)

articlesFile = "articles2.csv"
#articles.to_csv(articlesFile)
articles = pd.read_csv(articlesFile)
#articles = articles.drop(columns = ['Unnamed: 0'])
#print(articles.head(5))
'''
def getCases(date, location):
    date = pd.to_datetime(date)
    print(date)
    cases = pd.read_csv(date.strftime("%m-%d-%Y.csv"))
    return int(cases[cases['Province_State']==location]['Confirmed'])

articles['Confirmed'] = articles.apply(lambda x: getCases(x['date'], x['location']), axis=1)
articleFile = "articles2.csv"
articles = articles.drop(columns = ['Unnamed: 0'])
articles.to_csv(articleFile)
print(articles.columns)
'''
import sklearn
from sklearn import feature_extraction

 # Generate bag of words object with maximum vocab size of 1000
counter = sklearn.feature_extraction.text.CountVectorizer(max_features = 1000)
# Generate tf-idf object with maximum vocab size of 1000
tf_counter = sklearn.feature_extraction.text.TfidfVectorizer(max_features = 1000)

#for date in daterange(start_date, end_date):
# Get bag of words model as sparse matrix
bag_of_words = counter.fit_transform(articles['tweet'].apply(lambda x: np.str_(articles['tweet'])))
#print(bag_of_words)

# Get tf-idf matrix as sparse matrix
tfidf = tf_counter.fit(articles['tweet'].apply(lambda x: np.str_(articles['tweet'])))
df = articles


#print(df['location'])

#for date in daterange(start_date, end_date):
'''
words="finalTweets"+date.strftime("%B%d").lower()+".csv"
df = pd.read_csv(words)
df = df.drop(columns = ['Unnamed: 0'])
'''
#df['tfidf'] = tf_counter.transform(df['tweet'])
#df[['location','tfidf']].groupby('location').mean()
#print(df[['location','tfidf']].groupby('location').mean())
#print(df.dtypes)
data = []
#counter = 1

for date in daterange(start_date, end_date):
    print(date)
    #insert other pre-processing here, ex: date since start
    #print(df['date'])
    #print(start_date)
    df['date-since'] = (date - start_date)
    #d = datetime.today() - timedelta(days=days_to_subtract)

    #print('bystate: ', bystate)
    #print(data)
    #counter += 1
tfidf = tf_counter.transform(df['tweet'])
tfidf = pd.DataFrame(tfidf.toarray(), columns = tf_counter.get_feature_names())
df = pd.concat([df, tfidf], axis=1)
df = df.drop(columns = ['date','Unnamed: 0'])
bystate = df.groupby(['location', 'date-since']).mean()
#data = bystate.values
# Get the words corresponding to the vocab index
tf_counter.get_feature_names()
#print (tf_counter.get_feature_names())

tfidfConverted = "tfidf4.csv"
bystate.to_csv(tfidfConverted)