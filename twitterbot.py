import tweepy
import time
from credentials import *
from time import sleep

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print("Bot started.")

while True:
    for tweet in tweepy.Cursor(api.search, q='@ratemyplate_').items():
        try:
            username = tweet.user.screen_name
            text = tweet.text
            location = tweet.user.location
            api.update_status('@' + username + ' here is an autoreply: ' + str(tweet.id), in_reply_to_status_id=tweet.id)
            print("Tweet received from ", username, text )
        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    time.sleep(5)


