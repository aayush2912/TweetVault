"""

@author: Naga Satya Dheeraj Anumala
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterLarge']

def search_tweets(word, sort_option=None):
    print("Search word:", word)
    print("Sort option:", sort_option)
    tweets_with_word = []
    # Search for tweets containing the word in the text field
    for collection_name in ['originalTweets', 'retweets', 'quotedStatus']:
        
        result = db[collection_name].find({'$text': {'$search': word}})
        for tweet in result:
            tweets_with_word.append({
                'id_str': tweet['id_str'],
                'text': tweet['text'],
                'collection': collection_name,  # Add the collection name
                'user': {
                    'screen_name': tweet['user']['screen_name']
                }
            })

    # Sort the tweets based on the sort_option
    if sort_option:
        tweets_with_word = sort_tweets(tweets_with_word, sort_option)
    
    print("Search results:", tweets_with_word)

    return tweets_with_word, word



def sort_tweets(tweets, sort_option):
    if sort_option == 'created_at_asc':
        tweets.sort(key=sort_by_created_at_asc)
    elif sort_option == 'created_at_desc':
        tweets.sort(key=sort_by_created_at_desc)
    elif sort_option == 'user_asc':
        tweets.sort(key=sort_by_user_asc)
    elif sort_option == 'user_desc':
        tweets.sort(key=sort_by_user_desc)
    elif sort_option == 'favorite_count_asc':
        tweets.sort(key=sort_by_favorite_count_asc)
    elif sort_option == 'favorite_count_desc':
        tweets.sort(key=sort_by_favorite_count_desc)
    elif sort_option == 'reply_count_asc':
        tweets.sort(key=sort_by_reply_count_asc)
    elif sort_option == 'reply_count_desc':
        tweets.sort(key=sort_by_reply_count_desc)

    return tweets


# Add these sorting functions to sort tweets based on different criteria
def sort_by_created_at_asc(tweet):
    return tweet.get('created_at', '')

def sort_by_created_at_desc(tweet):
    return tweet.get('created_at', '')

def sort_by_user_asc(tweet):
    return tweet.get('user', {}).get('screen_name', '')

def sort_by_user_desc(tweet):
    return tweet.get('user', {}).get('screen_name', '')

def sort_by_favorite_count_asc(tweet):
    return tweet.get('favorite_count', 0)

def sort_by_favorite_count_desc(tweet):
    return -int(tweet.get('favorite_count', 0))  # Convert favorite_count to integer before negating
  # Use negative sign to sort in descending order

def sort_by_reply_count_asc(tweet):
    return tweet.get('reply_count', 0)

def sort_by_reply_count_desc(tweet):
    return -int(tweet.get('reply_count', 0))  # Convert reply_count to integer before negating  # Use negative sign to sort in descending order
