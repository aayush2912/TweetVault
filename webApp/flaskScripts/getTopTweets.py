"""

@author: Manas Maskar, Aayush Pradhan
"""

from pymongo import MongoClient,DESCENDING

client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge'] 
collection_names = db.list_collection_names() 

def calculate_tweet_score(tweet):
    quote_count_score = 15 if tweet['quote_count'] <= 1000 else \
                        25 if tweet['quote_count'] <= 10000 else \
                        35 if tweet['quote_count'] <= 100000 else \
                        50 if tweet['quote_count'] <= 1000000 else \
                        75

    reply_count_score = 45 if tweet['reply_count'] <= 1000 else \
                        100 if tweet['reply_count'] <= 10000 else \
                        140 if tweet['reply_count'] <= 100000 else \
                        200 if tweet['reply_count'] <= 1000000 else \
                        0

    retweet_count_score = 150 if tweet['retweet_count'] <= 1000 else \
                          300 if tweet['retweet_count'] <= 10000 else \
                          450 if tweet['retweet_count'] <= 100000 else \
                          600 if tweet['retweet_count'] <= 1000000 else \
                          0

    sensitivity_score = -15 if tweet.get('sensitivity', False) else 10

    total_score = quote_count_score + reply_count_score + retweet_count_score + sensitivity_score
    return total_score




def get_top_tweets():
    top_tweets = []
    for collection_name in collection_names:
        tweets = db[collection_name].find().sort([('retweet_count', DESCENDING)]).limit(10)
        for tweet in tweets:
            tweet['collection'] = collection_name  # Add collection name to the tweet
            tweet['total_score'] = calculate_tweet_score(tweet)  # Calculate total score
            top_tweets.append(tweet)
    return top_tweets

