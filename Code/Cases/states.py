from datetime import date, timedelta, datetime
import time
import csv
import pandas as pd
from twarc import Twarc
import tweepy
#from geopy.geocoders import Nominatim
#import countries

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
start_date = date(2020, 5, 14)
end_date = date(2020, 7, 13) #end date, datetime.date(datetime.now()) (this second option is dynamic and changes by date but depends on timezone)

OAUTH_TOKEN = "1029186921438883845-AQjxqWPxZlURJ47eWFqRFRkSCkDPFh"
OAUTH_TOKEN_SECRET = "YgxeTz31ItxBrJubvwZpZaqa57LLhWRKLMM4t82pdEtsv"
CONSUMER_KEY = "Y70ckEEL2TdQzyq9NqI5RriiB"
CONSUMER_SECRET = "YWQJJlJyzXxkaPXCEdFrANgHFf4Dyd0PtkT4f5TvXFUJLUtpvU"
t = Twarc(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')
states = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'DC': 'District of Columbia',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming'
         }

def extract_place(status):
    if type(status) is tweepy.models.Status:
        status = status.__dict__
    #Try to get the place from the place data inside the status dict
    if status['place'] is not None:
        place = status['place']
        if place['country'] != 'United States':
            return place['country']
        elif place['place_type'] == 'admin':
            return place['name']
        elif place['place_type'] == 'city':
            return states.get(place['full_name'].split(', ')[-1])
    #If the status dict has no place info, get the place from the user data
    else:
        place = status['user']['location']
        try:
            place = place.split(', ')[-1].upper()
        except AttributeError:
            return None
        if place in states:
            return states[place]
        else:
            return place

for date in daterange(start_date, end_date):
    after = date + timedelta(1)
    print(date.strftime("%B%-d").lower()+"_"+after.strftime("%B%-d").lower()+".csv")
    filename=date.strftime("%B%-d").lower()+"_"+after.strftime("%B%-d").lower()+".csv"
    if (date.strftime("%B%-d").lower() != "march29"):
        with open(date.strftime("%B%-d").lower()+"_"+after.strftime("%B%-d").lower()+".csv", 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=' ', quotechar='|')
            """
            for row in data:
                print (row)
                break    
            """

            
            totaldata=pd.read_csv(filename, header=None)
            dataframe=totaldata[0]
            numberfile = "number_corona_tweets"+ date.strftime("%B%-d").lower() +".txt"
            readyfile = "ready_corona_tweets"+ date.strftime("%B%-d").lower() +".csv"
            dataframe.to_csv(numberfile, index=False, header=None)
            for tweet in t.hydrate(open(numberfile)):
                #print (tweet["place"]["country"])
                if (tweet["place"] == None):
                    continue
                if (tweet["place"]["country"] == None):
                    continue
                '''
                if ("place" not in tweet):
                    print ("gibberish")
                    continue
                if ("country" not in tweet["place"]):
                    #print ("sdjfksldf")
                    continue
                '''
                if (tweet["place"]["country"] == "United States"):
                    #print("sdkjf")
                    '''
                    with open (readyfile, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile, delimiter=' ', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
                        csvwriter.writerow([tweet["full_text"]])
                    '''
                    
                    with open (readyfile, 'a', newline='') as csvfile:
                        #fieldnames = ['tweet','state']
                        writer = csv.writer(csvfile)
                        valState = extract_place(tweet)
                        somedict = {'tweet': tweet["full_text"], 'state': valState}
                        for value in somedict.items():
                            writer.writerow(value)
                    
                    '''
                    with open(readyfile,'a') as csvfile:
                        try:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow({'tweet': tweet["full_text"], 'location': extract_place(tweet)})
                        except:
                            pass
                    
                    with open (readyfile, 'a', newline='') as csvfile:
                        #fieldnames = ['tweet','state']
                        #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        valState = extract_place(tweet)
                        somedict = {'tweet': tweet["full_text"], 'state': valState}
                        for key,value in somedict.items():
                            print(somedict['tweet'])
                            print('ok then')
                            print(somedict['state'])
                            writer.writerow([key,value])
                    '''
                    #wr = open(readyfile, 'a')
                    #wr.write(tweet["full_text"])
                #print(tweet["full_text"])
            break
            
            
    break

'''
open()
with open('eggs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
'''
