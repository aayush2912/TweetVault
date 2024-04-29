"""

@author: Manas Maskar, Aayush Pradhan
"""


from pymongo import MongoClient
import re

#Connections to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge']  
tweets_collection = db['originalTweets']
retweets_collection = db['retweets']
quoted_status_collection = db['quotedStatus']

#Search Implementation Started -->
hashtag_to_search = input("Enter the hashtag you want to search for: ").lower()

#More filters to make hashtag efficient 
hashtag_pattern = re.compile(rf'\b{hashtag_to_search}\b', flags=re.IGNORECASE)


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

# Original Tweets Collection -->
tweets_with_hashtag = tweets_collection.find({
    'text': {'$regex': hashtag_pattern}
})

print("Results from Tweets:")
for tweet in tweets_with_hashtag:
    tweet_data = extract_data(tweet)
    print(tweet_data)

# Retweets Collection -->
retweets_with_hashtag = retweets_collection.find({
    'text': {'$regex': hashtag_pattern}
})

print("\nResults from Retweets:")
for retweet in retweets_with_hashtag:
    retweet_data = extract_data(retweet)
    print(retweet_data)

# QuotedStatus Collection -->
quoted_with_hashtag = quoted_status_collection.find({
    'text': {'$regex': hashtag_pattern}
})

print("\nResults from Quoted Statuses:")
for quote in quoted_with_hashtag:
    quote_data = extract_data(quote)
    print(quote_data)
