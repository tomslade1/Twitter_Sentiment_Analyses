#########################################################
#        EXAMPLE CONNECTION TO TWITTER APIs              #
#########################################################

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

# Showing an example REST API method - home_timeline grabs top 20 most recent
# tweets from defined account's feed

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# Example of using the REST API to access User acct info

# my_user = api.me()  # use '.me()' method to pull own acct info
# other_user = api.get_user('TomSlade15')  # use '.get_user()' for others

# # Access individual attributes
# print(other_user.location)
# print(other_user.status)

# # Pass all attributes into a dictionary
# print(other_user._json)


# class MyStreamListener(tweepy.StreamListener):
#     def __init__(self, api=None):
#         super(MyStreamListener, self).__init__()
#         self.num_tweets = 0
#         self.file = open("tweets.txt", "w")

#     def on_status(self, status):
#         tweet = status._json
#         self.file.write( json.dumps(tweet) + '\n' )
#         self.num_tweets += 1
#         if self.num_tweets < 100:
#             return True
#         else:
#             return False
#         self.file.close()

#     def on_error(self, status):
#         print(status)
