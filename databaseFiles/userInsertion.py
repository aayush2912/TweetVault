"""

@author: Manas Maskar, Naga Satya Dheeraj Anumala
"""

import pymysql
import pymongo
from datetime import datetime

# Connect to MongoDB
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['readingJsonFiles']  
mongo_collection = mongo_db['Corona-out-3']  

# Establish a connection to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Plum@08901',
    database='twitterLarge'
)

cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS users (
    id_str VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    screen_name VARCHAR(255),
    location VARCHAR(255),
    url VARCHAR(255),
    description TEXT,
    translator_type VARCHAR(255),
    protected BOOLEAN,
    verified BOOLEAN,
    followers_count INT,
    friends_count INT,
    following BOOLEAN,
    listed_count INT,
    favourites_count INT,
    statuses_count INT,
    created_at DATETIME,
    lang VARCHAR(255),
    default_profile BOOLEAN,
    default_profile_image BOOLEAN
)
"""
cursor.execute(create_table_query)

# Function to extract user information and insert into the table
def extract_user_info(user_data, cursor):
    created_at = datetime.strptime(user_data['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S')
    
    # Extract specific user information
    user_info = (
        user_data['id_str'],
        user_data['name'],
        user_data['screen_name'],
        user_data['location'],
        user_data.get('url', ''),  
        user_data['description'],
        user_data.get('translator_type', ''),  
        user_data['protected'],
        user_data['verified'],
        user_data['followers_count'],
        user_data['friends_count'],
        user_data['following'],
        user_data['listed_count'],
        user_data['favourites_count'],
        user_data['statuses_count'],
        created_at,
        user_data.get('lang', ''),  
        user_data['default_profile'],
        user_data['default_profile_image']
    )

    cursor.execute("SELECT id_str FROM users WHERE id_str = %s", (user_data['id_str'],))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        cursor.execute("""
            INSERT INTO users (id_str, name, screen_name, location, url, description, translator_type,
            protected, verified, followers_count, friends_count, following, listed_count, favourites_count,
            statuses_count, created_at, lang, default_profile, default_profile_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, user_info)
        print(f"User {user_data['name']} added")

def extract_users(tweet, cursor):
    user_data = tweet.get('user')
    if user_data:
        extract_user_info(user_data, cursor)

    if 'retweeted_status' in tweet:
        extract_users(tweet['retweeted_status'], cursor)

    if 'quoted_status' in tweet:
        extract_users(tweet['quoted_status'], cursor)

users_added_count = 0


for tweet in mongo_collection.find():
    extract_users(tweet, cursor)
    users_added_count += 1

print(f"Total users added from {users_added_count} tweets ")
