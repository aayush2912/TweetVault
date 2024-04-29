"""

@author: Manas Maskar, Naga Satya Dheeraj Anumala
"""

import pymongo

# MongoDB connections setup
client = pymongo.MongoClient("mongodb://localhost:27017")
source_db = client["readingJsonFiles"]
source_collection = source_db["Corona-out-3"]
target_db = client["twitterLarge"]
target_collection = target_db["quotedStatus"]
cursor = source_collection.find()

#Start to loop in each JSON Object.
for document in cursor:
    # Check if the document contains a quoted status
    quoted_status = document.get("quoted_status")
    if quoted_status or document.get("is_quote_status", False):
        quoted_data = {
            "created_at": quoted_status.get("created_at") if quoted_status else None,
            "id": quoted_status.get("id") if quoted_status else None,
            "id_str": quoted_status.get("id_str") if quoted_status else None,
            "text": (quoted_status.get("extended_tweet", {}).get("full_text") if quoted_status and quoted_status.get("truncated") else None) or (quoted_status.get("text") if quoted_status else None),
            "source": quoted_status.get("source") if quoted_status else None,
            "truncated": quoted_status.get("truncated") if quoted_status else None,
            "user": {
                "id_str": quoted_status["user"].get("id_str") if quoted_status and quoted_status.get("user") else None,
                "screen_name": quoted_status["user"].get("screen_name") if quoted_status and quoted_status.get("user") else None
            },
            "geo": quoted_status.get("geo") if quoted_status else None,
            "coordinates": quoted_status.get("coordinates") if quoted_status else None,
            "place": quoted_status.get("place") if quoted_status else None,
            "contributors": quoted_status.get("contributors") if quoted_status else None,
            "is_quote_status": quoted_status.get("is_quote_status") if quoted_status else None,
            "quote_count": quoted_status.get("quote_count") if quoted_status else None,
            "reply_count": quoted_status.get("reply_count") if quoted_status else None,
            "retweet_count": quoted_status.get("retweet_count") if quoted_status else None,
            "favorite_count": quoted_status.get("favorite_count") if quoted_status else None,
            "entities": {},
            "favorited": quoted_status.get("favorited") if quoted_status else None,
            "retweeted": quoted_status.get("retweeted") if quoted_status else None,
            "filter_level": quoted_status.get("filter_level") if quoted_status else None,
            "lang": quoted_status.get("lang") if quoted_status else None
        }
        quoted_data["sensitivity"] = quoted_status.get("possibly_sensitive") 
        # if quoted_status else False

        # Check if 'entities' key exists in quoted_status dictionary
        if quoted_status and "entities" in quoted_status:
            # Access the 'entities' dictionary
            entities = quoted_status["entities"]
            # Check if 'media' key exists within 'entities'
            if "media" in entities:
                # Access the 'media' list
                media_list = entities["media"]
                # Check if 'media' is a list
                if isinstance(media_list, list):
                    # Extract the 'type' value from each media item
                    quoted_data["entities"]["media"] = [media.get("type") for media in media_list]
                else:
                    # If media is not present in the list this is the case trigerred.
                    pass
            else:
                # In case media is out of entities.
                pass
        else:
            # If entities are not present in the code.
            pass

        # Check if the quoted tweet is already present in the DB.
        existing_quoted_tweet = target_collection.find_one({"id": quoted_status.get("id")}) if quoted_status else None
        if existing_quoted_tweet:
            print(f"Quoted tweet with ID {quoted_status.get('id')} already exists. Skipping insertion.")
        else:
            target_collection.insert_one(quoted_data)

print("Quoted Tweets Inserted Successfully")
