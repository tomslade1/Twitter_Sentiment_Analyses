###############################################################
#        EXAMPLE CONNECTION TO TWITTER REST APIs              #
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

# Showing an example REST API method - home_timeline grabs top 20 most recent
# tweets from defined account's feed

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# Example of using the REST API to access User acct info

# my_user = api.me()  # use '.me()' method to pull own acct info
# other_user = api.get_user('TomSlade15')  # use '.get_user()' for others

# # Access individual attributes
# print(other_user.location)
# print(other_user.status)

# # Pass all attributes into a dictionary
# print(other_user._json)

# Example of using the REST API to sample tweets given
# set parameters (no RTs & no Replies)

search_results = api.search(q="nowtv -filter:retweets AND -filter:replies",
                            tweet_mode='extended', count=10)

i = 0

for tweet in search_results:
    if tweet.user.followers_count > 0:
        i += 1
        print("Tweet Number:" + str(i), "User:" + tweet.user.screen_name,
              '"' + tweet.full_text, '"\n')
    else:
        pass
