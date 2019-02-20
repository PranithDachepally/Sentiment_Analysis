# -*- coding: utf-8 -*-
import tweepy
import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

from credentials import *

#
def twitter_setup():
    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_token_secret)

    api = tweepy.API(auth)
    return api

extractor = twitter_setup()

tweets = extractor.user_timeline(screen_name='realDonaldTrump', count=200)
print("number of tweets extracted : "+str(len(tweets)))

print("5 recent tweets")
for tweet in tweets[:5]:
    print(tweet.text)

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
display(data.head(10))

print(dir(tweets[0]))
print(tweets[0].id)
print(tweets[0].created_at)
print(tweets[0].source)
print(tweets[0].favorite_count)
print(tweets[0].retweet_count)
print(tweets[0].geo)
print(tweets[0].coordinates)
print(tweets[0].entities)

data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

display(data.head(10))

mean = np.mean(data['len'])

print("The lenght's average in tweets is : {}".format(mean))

fav_max = np.max(data['Likes'])
rt_max = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt = data[data.RTs == rt_max].index[0]

#Max fav
print("The tweet with more likes is : {}".format(data['Tweets'][fav]))
print("Number of likes : {}".format(fav_max))
print("{} character. \n".format(data['len'][fav]))

#Max Rts
#print("The tweet with more retweets is : {}".format(data['Tweets'][rt]))
print("Number of likes : {}".format(rt_max))
print("{} character. \n".format(data['len'][rt]))

# We create time series for data:
tlen = pd.Series(data = data['len'].values,index = data['Date'])
tfav = pd.Series(data = data['Likes'].values,index = data['Date'])
tret = pd.Series(data = data['RTs'].values,index = data['Date'])
print(type(tlen))
tlen.plot(figsize=(16,4), label = 'length', legend = 'True')
tfav.plot(figsize=(16,4), label = 'Likes', legend = 'True')
tret.plot(figsize=(16,4), label = 'retweets', legend = 'True')
#plt.show()

#We obtain all possible sources
sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)

print("Creation of content sources:")
for soruce in sources:
    print("* {}".format(source))

#Creating Pie Chart
percent = np.zeros(len(sources))

for source in sources:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index]+=1


plt.clf()
pie_chart  = pd.Series(percent, index = sources, name = 'Sources')
pie_chart.plot.pie(fontsize = 11, autopct = '%.2f', figsize = (20,20))
#plt.show()

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity  > 0 :
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else :
        return -1

SA = []
for tweet in data['Tweets']:
    SA.append(analize_sentiment(tweet))

data['SA'] = np.array(SA)

display(data.head(10))

postive_tweets =[tweet for index, tweet in enumerate(data['Tweets'])if data['SA'][index]>0]
neutral_tweets =[tweet for index, tweet in enumerate(data['Tweets'])if data['SA'][index]==0]
negative_tweets =[tweet for index, tweet in enumerate(data['Tweets'])if data['SA'][index]<0]

print('Percentage of Positive tweets : {}%'.format((len(postive_tweets)*100)/len(data['Tweets'])))
print('Percentage of Neutral tweets : {}%'.format((len(neutral_tweets)*100)/len(data['Tweets'])))
print('Percentage of Negative tweets : {}%'.format((len(negative_tweets)*100)/len(data['Tweets'])))