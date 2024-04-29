"""

@author: Manas Maskar, Aayush Pradhan
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge'] 
collection_names = db.list_collection_names() #This query is usually used in Mongosh (MongoShell) makes our job easy
#to pass it in a list.


#Implementing a TopTweets Metrics and taking the average of the sum.
def calculate_score(tweet): 
    quote_count_score = 15 if tweet['quote_count'] <= 1000 else \
                        25 if tweet['quote_count'] <= 10000 else \
                        35 if tweet['quote_count'] <= 100000 else \
                        55 if tweet['quote_count'] <= 1000000 else \
                        75

    reply_count_score = 45 if tweet['reply_count'] <= 1000 else \
                        55 if tweet['reply_count'] <= 10000 else \
                        85 if tweet['reply_count'] <= 100000 else \
                        95 if tweet['reply_count'] <= 1000000 else \
                        0

    retweet_count_score = 25 if tweet['retweet_count'] <= 1000 else \
                          35 if tweet['retweet_count'] <= 10000 else \
                          45 if tweet['retweet_count'] <= 100000 else \
                          65 if tweet['retweet_count'] <= 1000000 else \
                          0

    # Penalty to the user and tweet if sensitive content published!
    if 'sensitivity' in tweet:
        sensitivity_score = -15 if tweet['sensitivity'] else 10
    else:
        
        sensitivity_score = 0 

    total_score = quote_count_score + reply_count_score + retweet_count_score + sensitivity_score

    return total_score

#Select those top 10 tweets and print them accordingly using Descending order.
def get_top_tweets(collection):
    # Fetch all tweets from the collection
    all_tweets = db[collection].find()
    scored_tweets = []
    for tweet in all_tweets:
        tweet['total_score'] = calculate_score(tweet)
        tweet['collection'] = collection  
        scored_tweets.append(tweet)

    top_tweets = sorted(scored_tweets, key=lambda x: x['total_score'], reverse=True)[:10]

    return top_tweets

# Above function and this function together start to append tweets together top display the cummulative top10Tweets from all collections.
def combine_top_tweets():
    combined_tweets = []
    for collection in collection_names:
        top_tweets = get_top_tweets(collection)
        combined_tweets.extend(top_tweets)
    
    # Sort combined tweets by total score in descending order
    combined_tweets_sorted = sorted(combined_tweets, key=lambda x: x['total_score'], reverse=True)[:10]

    return combined_tweets_sorted

# Printing the results.
top_tweets_combined = combine_top_tweets()
for index, tweet in enumerate(top_tweets_combined, start=1):
    print(f"Top {index} Tweet:")
    print("Tweet ID:", tweet['id_str'])
    print("User Screen Name:", tweet['user']['screen_name'])
    print("Total Score:", tweet['total_score'])
    print("Collection:", tweet['collection'])
    print("-" * 50)
