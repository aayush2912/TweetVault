"""

@author: Manas Maskar, Aayush Pradhan
"""

from pymongo import MongoClient
import re

# #Connections to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge']  # MongoDB database name
tweets_collection = db['originalTweets']
retweets_collection = db['retweets']
quoted_status_collection = db['quotedStatus']

#Passing search word
tweet_to_search = input("Enter the tweet you want to search for: ").lower()

#  Expression pattern to match hashtags
tweet_pattern = re.compile(rf'\b{tweet_to_search}\b', flags=re.IGNORECASE)

# Function to extract relevant data from the document
def extract_data(doc):
    data = {
        'tweet_id': doc.get('id_str'),
        'tweet_text': doc.get('text'),
        'quote_count': doc.get('quote_count', 0),
        'reply_count': doc.get('reply_count', 0),
        'filter_level': doc.get('filter_level'),
        'user_id_str': doc.get('user', {}).get('id_str')
    }
    return data

# Search in tweets collection
tweets_with_hashtag = tweets_collection.find({
    'text': {'$regex': tweet_pattern}
})

print("Results from Tweets:")
for tweet in tweets_with_hashtag:
    tweet_data = extract_data(tweet)
    print(tweet_data)

# Search in retweets collection
retweets_with_hashtag = retweets_collection.find({
    'text': {'$regex': tweet_pattern}
})

print("\nResults from Retweets:")
for retweet in retweets_with_hashtag:
    retweet_data = extract_data(retweet)
    print(retweet_data)

# Search in quotedStatus collection
quoted_with_hashtag = quoted_status_collection.find({
    'text': {'$regex': tweet_pattern}
})

print("\nResults from Quoted Statuses:")
for quote in quoted_with_hashtag:
    quote_data = extract_data(quote)
    print(quote_data)
