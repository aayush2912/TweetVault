"""

@author: Manas Maskar, Naga Satya Dheeraj Anumala
"""

import pymongo
#Connection setup -->
client = pymongo.MongoClient("mongodb://localhost:27017")
source_db = client["readingJsonFiles"]
source_collection = source_db["Corona-out-3"]

target_db = client["twitterLarge"]
target_collection = target_db["originalTweets"]
cursor = source_collection.find()

# Looping in each JSON Object Starts
for document in cursor:
    
    if not document["text"].startswith("RT"):   # <-- Check if the "main tweet" is a retweet.
        tweet_data = {
            "id": document["id"],
            "id_str": document["id_str"],
            "created_at": document["created_at"],
            "entities": document["entities"],
            "truncated":document["truncated"],
            "user": {
                            "id_str": document["user"].get("id_str"),
                            "screen_name": document["user"].get("screen_name")
                            },
            "quote_count": document.get("quote_count", 0),
            "reply_count": document.get("reply_count", 0),
            "retweet_count": document.get("retweet_count", 0),
            "favorite_count": document.get("favorite_count", 0),
            "filter_level": document.get("filter_level", ""),
            "sensitivity":document.get("possibly_sensitive"),
            "lang": document.get("lang", ""),
            "timestamp_ms": document.get("timestamp_ms", "")
        }

        #Check if the truncated stmt is true, if yes use the extended tweet as text while storing
        if document.get("truncated", True):
            extended_tweet_data = document.get("extended_tweet", {})
            tweet_data["text"] = extended_tweet_data.get("full_text", document["text"])
            tweet_data["entities"] = extended_tweet_data.get("entities", document["entities"])

        else:
            tweet_data["text"] = document["text"]

        target_collection.insert_one(tweet_data)

    else:
        # There are few scenarios where the main tweet is retweet of a main tweet and thus looping retweet status as well 
        if "retweeted_status" in document:
            retweeted_status = document["retweeted_status"]
            #Again Retweet or not is checked!!
            if not retweeted_status["text"].startswith("RT"):
                retweet_data = {
                    "id": retweeted_status["id"],
                    "id_str": retweeted_status["id_str"],
                    "created_at": retweeted_status["created_at"],
                    "entities": retweeted_status["entities"],
                    "truncated":retweeted_status["truncated"],
                    "user": {
                            "id_str": retweeted_status["user"].get("id_str"),
                            "screen_name": retweeted_status["user"].get("screen_name")
                            },
                    "quote_count": retweeted_status.get("quote_count", 0),
                    "reply_count": retweeted_status.get("reply_count", 0),
                    "retweet_count": retweeted_status.get("retweet_count", 0),
                    "favorite_count": retweeted_status.get("favorite_count", 0),
                    "filter_level": retweeted_status.get("filter_level", ""),
                    "sensitivity":retweeted_status.get("possibly_sensitive"),
                    "lang": retweeted_status.get("lang", ""),
                    "timestamp_ms": retweeted_status.get("timestamp_ms", "")
                }

                #Check for truncated attribute
                if retweeted_status.get("truncated", True):
                    extended_tweet_data = retweeted_status.get("extended_tweet", {})
                    retweet_data["text"] = extended_tweet_data.get("full_text", retweeted_status["text"])
                    retweet_data["entities"] = extended_tweet_data.get("entities", retweeted_status["entities"])

                else:
                    retweet_data["text"] = retweeted_status["text"]

                target_collection.insert_one(retweet_data)
#Debug Phase to check if all data inserted or not.
print("Data Inserted Successfully")
