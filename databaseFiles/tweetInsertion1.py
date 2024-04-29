import pymongo

# MongoDB connection for reading data
client = pymongo.MongoClient("mongodb://localhost:27017")
source_db = client["readingJsonFiles"]
source_collection = source_db["Corona-out-3"]

# MongoDB connection for storing data
target_db = client["twitterLarge"]
target_collection = target_db["originalTweets"]

# Fetch data from the source collection
cursor = source_collection.find()

# Iterate over each document in the source collection
for document in cursor:
    # Check if the main tweet text starts with "RT"
    if not document["text"].startswith("RT"):
        # Store main tweet data
        tweet_data = {
            "id": document["id"],
            "id_str": document["id_str"],
            "created_at": document["created_at"],
            "text": document["text"],
            "entities": {
                "hashtags": document["entities"]["hashtags"],
                "user_mentions": document["entities"]["user_mentions"]
            },
            "quote_count": document.get("quote_count", 0),
            "is_quote_status": document["is_quote_status"],
            "reply_count": document.get("reply_count", 0),
            "retweet_count": document.get("retweet_count", 0),
            "sensitivity": document.get("possibly_sensitive", False),
            "filter_level": document.get("filter_level", "")
        }

        # Check if media entities exist
        if "media" in document["entities"]:
            tweet_data["entities"]["media"] = [media["type"] for media in document["entities"]["media"]]

        # Extract user information
        user_info = {
            "id_str": document["user"]["id_str"],
            "screen_name": document["user"]["screen_name"]
        }

        # Add user information to tweet data
        tweet_data["user"] = user_info

        # Check if the tweet with the same id already exists in the target collection
        existing_tweet = target_collection.find_one({"id": document["id"]})
        if existing_tweet:
            print(f"Tweet with ID {document['id']} already exists. Skipping insertion.")
        else:
            target_collection.insert_one(tweet_data)

    else:
        # Check for retweeted_status if present
        if "retweeted_status" in document:
            retweeted_status = document["retweeted_status"]
            # Check if retweeted tweet text starts with "RT"
            if not retweeted_status["text"].startswith("RT"):
                # Store retweet data
                retweet_data = {
                    "id": retweeted_status["id"],
                    "id_str": retweeted_status["id_str"],
                    "created_at": retweeted_status["created_at"],
                    "text": retweeted_status["text"],
                    "entities": {
                        "hashtags": retweeted_status["entities"]["hashtags"],
                        "user_mentions": retweeted_status["entities"]["user_mentions"]
                    },
                    "quote_count": retweeted_status.get("quote_count", 0),
                    "is_quote_status": retweeted_status["is_quote_status"],
                    "reply_count": retweeted_status.get("reply_count", 0),
                    "retweet_count": retweeted_status.get("retweet_count", 0)
                }

                # Check if media entities exist
                if "media" in retweeted_status["entities"]:
                    retweet_data["entities"]["media"] = [media["type"] for media in retweeted_status["entities"]["media"]]

                # Extract user information
                user_info = {
                    "id_str": retweeted_status["user"]["id_str"],
                    "screen_name": retweeted_status["user"]["screen_name"]
                }

                # Add user information to retweet data
                retweet_data["user"] = user_info

                # Check if the retweet with the same id already exists in the target collection
                existing_retweet = target_collection.find_one({"id": retweeted_status["id"]})
                if existing_retweet:
                    print(f"Retweet with ID {retweeted_status['id']} already exists. Skipping insertion.")
                else:
                    target_collection.insert_one(retweet_data)
    print("Data Inserted Successfully")
