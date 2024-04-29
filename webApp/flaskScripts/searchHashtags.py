"""

@author: Manas Maskar, Naga Satya Dheeraj Anumala
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge']

# Function to search for hashtags in MongoDB
# Function to search for hashtags in MongoDB
def search_hashtags(hashtag):
    # Search for tweets containing the given hashtag in all collections
    search_result = []
    collections = ['originalTweets', 'retweets', 'quotedStatus']
    for collection_name in collections:
        result = db[collection_name].find({'entities.hashtags.text': hashtag})
        for tweet in result:
            search_result.append({
                'id_str': tweet['id_str'],
                'text': tweet['text'],
                'hashtags': [tag['text'] for tag in tweet['entities']['hashtags']],  # Extract hashtag text
                'collection': collection_name,  # Add the collection name to identify where the tweet is from
                'user': {
                    'screen_name': tweet['user']['screen_name']
                }
            })

    return search_result, hashtag
