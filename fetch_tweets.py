import json
import datetime

import tweepy
from tweepy import OAuthHandler
from peewee import *

CONSUMER_KEY = 'TWITTER_KEY'
CONSUMER_SECRET = 'TWITTER_KEY'
ACCESS_TOKEN = 'TWITTER_KEY'
ACCESS_SECRET = 'TWITTER_KEY'

DATABASE = MySQLDatabase('trump', host='localhost', user='root',passwd='GITHUB_IS_AWESOME')
FOLLOWING = 'realDonaldTrump'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


class BaseModel(Model):
	class Meta:
		database = DATABASE


class Trump(BaseModel):
	trump_tweet_id = PrimaryKeyField()
	trump_tweet_text = CharField()
	trump_tweet_date_created = DateTimeField()
	trump_tweet_twitter_id = BigIntegerField(index=True, unique=True)


class Trump_Sentiment(BaseModel):
	trump_sentiment_id = PrimaryKeyField()
	trump_tweet_id = IntegerField(index=True)
	is_trump = BooleanField()
	positivity_index = DoubleField()


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Trump,Trump_Sentiment], safe=True)
	DATABASE.close()


def get_tweets():
	tweet_array = []
	tweets = api.user_timeline(screen_name=FOLLOWING, count=200)
	for tweet in tweets:
		tweet_json = tweet._json
		tweet_dict = {
			"created_at": tweet_json['created_at'],
			"id": tweet_json['id'],
			"text": tweet_json['text']
		}
		tweet_array.append(tweet_dict)
	return tweet_array

def save_tweet(tweets):
	for tweet in tweets:
		try:
			Trump.create(
				trump_tweet_text = tweet['text'],
				trump_tweet_date_created = datetime.datetime.now(),
				trump_tweet_twitter_id = tweet['id']
			)
		except Exception as e:
			print("There was an oopsy. Prolly crooked Hillary's fault. This was the problem: {}".format(e))

if __name__ == "__main__":
	initialize()
	save_tweet(get_tweets())