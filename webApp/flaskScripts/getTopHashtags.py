"""

@author: Manas Maskar, Aayush Pradhan
"""

from pymongo import MongoClient

def get_top_10_hashtags():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitterLarge']
    tweets_collection = db['originalTweets']
    retweets_collection = db['retweets']
    quoted_status_collection = db['quotedStatus']
    
    # Hashtags saved in key value pair
    all_hashtags = {}
    
    #Find and update hashtags
    def update_hashtag_counts(collection):
        collection.create_index([('entities.hashtags.text', 1)]) #Indexing for fast search
        query = {'entities.hashtags.text': {'$exists': True, '$ne': []}} #Pass the hastag and check everywhere in the data.
        projection = {'entities.hashtags.text': 1, 'id_str': 1} #Basically a select statement to avoid passing of excess data.
        #Improves search efficiency
        for item in collection.find(query, projection):
            hashtags = item.get('entities', {}).get('hashtags', [])
            for hashtag_data in hashtags:
                hashtag_text = hashtag_data.get('text', '')
                if hashtag_text:
                    if hashtag_text not in all_hashtags:
                        all_hashtags[hashtag_text] = {'count': 0, 'ids': set()}
                    all_hashtags[hashtag_text]['count'] += 1
                    if 'id_str' in item:
                        all_hashtags[hashtag_text]['ids'].add(item['id_str'])
    
 #check and update the count from all the collections in the database.
    update_hashtag_counts(tweets_collection)
    update_hashtag_counts(retweets_collection)
    update_hashtag_counts(quoted_status_collection)
    #Sort and print top10Hashtags this will be used further to display!!!
    top_hashtags = sorted(all_hashtags.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
    
    # Print the fetched data
    print("Fetched top 10 hashtags data:")
    if top_hashtags:
        for i, (hashtag, data) in enumerate(top_hashtags, 1):
            print(f"{i}. Hashtag: {hashtag}, Count: {data['count']}, IDs: {', '.join(data['ids'])}")
    else:
        print("No top hashtags found.")
    
    return top_hashtags or []  # Return an empty list if no top hashtags found

if __name__ == "__main__":
    top_hashtags = get_top_10_hashtags()
