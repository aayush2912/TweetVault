"""
@author: Manas Maskar, Aayush Pradhan
"""

import pymongo

def fetch_tweets(user_id_str, collection_name):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["twitterLarge"]
    collection = db[collection_name]
    query = {"user.id_str": user_id_str} 
    #print("Running query on collection:", collection_name, "with query:", query) 
    cursor = collection.find(query)
    tweets = [tweet for tweet in cursor]
    return tweets

