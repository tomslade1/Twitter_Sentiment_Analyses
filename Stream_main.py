###############################################################
#        EXAMPLE CONNECTION TO TWITTER STREAM API             #
###############################################################

import tweepy
import json

json_path = "\
C:\\Users\\TSL03\\OneDrive - Sky\\Documents\\Python Working Area\\\
Python_Code\\Project_Notebooks\\Twitter_Sentiment_Analysis\\Twitter_Keys.json"

with open(json_path) as json_file:
    json_data = json.load(json_file)

creds = json_data['Twitter_API_Credentials']

access_token = creds['access_token']
access_token_secret = creds['access_token_secret']
consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create a connection to twitter's REST APIs using our auth
api = tweepy.API(auth)


# Create a 'StreamListener'
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.txt", "w")

    def on_status(self, status):
        tweet = status._json
        self.file.write(json.dumps(tweet) + '\n')
        self.num_tweets += 1
        if self.num_tweets < 100:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)
