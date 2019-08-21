import re
import tweepy
import json
from tweepy import OAuthHandler
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
# nltk.download('vader_lexicon')  # Download VADER dataset for word comparison

json_path = "\
C:\\Users\\TSL03\\OneDrive - Sky\\Documents\\Python_Working_Area\\\
Python_Code\\Project_Notebooks\\Twitter_Sentiment_Analysis\\Twitter_Keys.json"

with open(json_path) as json_file:
    json_data = json.load(json_file)

creds = json_data['Twitter_API_Credentials']


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        access_token = creds['access_token']
        access_token_secret = creds['access_token_secret']
        consumer_key = creds['consumer_key']
        consumer_secret = creds['consumer_secret']
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except ValueError():
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing tagged users (@..),
        special characters, and links using simple regex statements.
        '''
        return ' '.join(re.sub("""(@[A-Za-z0-9]+)
                                   |([^0-9A-Za-z \t])
                                   |(\w+:\/\/\S+)
                               """, " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using nltk's sentiment method  (using VADER)
        '''
        analyser = SentimentIntensityAnalyzer()
        # create VADER scores of passed tweet text
        score = analyser.polarity_scores(self.clean_tweet(tweet))
        # set sentiment
        if score['compound'] >= 0.05:
            return 'positive'
        elif (score['compound'] > -0.05) and (score['compound'] < 0.05):
            return 'neutral'
        elif score['compound'] <= -0.05:
            return 'negative'
        else:
            return 'non-categorised'

    def get_tweets(self, query, tweet_mode, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query,
                                             count=count,
                                             tweet_mode=tweet_mode)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.full_text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = \
                    self.get_tweet_sentiment(tweet.full_text)
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            # return parsed tweets
            return tweets
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(query, count, tweet_mode):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=query, count=count, tweet_mode=tweet_mode)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)
                                                    / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)
                                                    / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) -
                                                        len(ntweets) -
                                                        len(ptweets)) /
                                                   len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    # calling main function
    main(query='nowtv -filter:retweets AND -filter:replies',
         count=200,
         tweet_mode='extended')
