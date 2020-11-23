#python libraries
import datetime
import tweepy
import csv
import re
from apscheduler.schedulers.blocking import BlockingScheduler
from textblob import TextBlob

#Keys and access for Twitter
consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'
access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def data_gatherer():
    #Add time your file was created to discriminate date/time after running the crontab file
    filename = 'twitter_data_analysis'+(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+'.csv'

    #Steps 1 & 2
    with open (filename, 'a+', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)

        #using tweepy Cursor
        for tweet in tweepy.Cursor(api.search, q='covid19vaccine', lang = 'en', count=10000).items():
            #writing a csv file
            tweets_encoded = tweet.text.encode('utf-8')
            tweets_decoded = tweets_encoded.decode('utf-8')
            clean_tweet = remove_url(tweets_decoded)
            analysis = TextBlob(tweet.text)
            
            if analysis.sentiment[0]>0:
                sentiment = 'Positive'
            elif analysis.sentiment[0] == 0:
                sentiment = 'Neutral'
            else:
                neg_sentiment = 'Negative'
                csvWriter.writerow([datetime.datetime.now().strftime("%Y-%m-%d  %H:%M"), clean_tweet, analysis.sentiment[0], neg_sentiment])

            
            print(clean_tweet)
            print(analysis.sentiment[0])
            print(sentiment)
            
#            csvWriter.writerow([datetime.datetime.now().strftime("%Y-%m-%d  %H:%M"), clean_tweet, analysis.sentiment[0], sentiment])

scheduler = BlockingScheduler()
scheduler.add_job(data_gatherer, 'interval', minutes=2)
scheduler.start()