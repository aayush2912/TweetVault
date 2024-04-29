#Code for backup if the main app crashes.

from flask import Flask, render_template, request
from userSearch import search_users
from userTweets_fetch import fetch_tweets
from getTopUsers import get_top_users
from getTopTweets import get_top_tweets, calculate_tweet_score
from getTopHashtags import get_top_10_hashtags
from searchHashtags import search_hashtags
from searchTweets import search_tweets
from cache import Cache

app = Flask(__name__, template_folder='/Users/manasmaskar/Rutgers/Spring24/DBMS/Twitter3/webApp/templates')
cache = Cache(max_size=5, expiry_time=30)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_criteria = request.form.get('username', '')
        sort_option = request.form.get('sort')

        # Check if the result is already cached
        cached_result = cache.get((search_criteria, sort_option))
        if cached_result:
            users, search_time = cached_result
        else:
            # Perform search operation
            users, search_time = search_users(search_criteria, sort_option)
            # Cache the result
            cache.set((search_criteria, sort_option), (users, search_time))

        return render_template('searchUsers.html', users=users, search_time=search_time, search_criteria=search_criteria)
    else:
        return redirect(url_for('index'))



  # Using user_id_str to be clear
@app.route('/user/<user_id_str>') 
def user_tweets(user_id_str):
    original_tweets = fetch_tweets(user_id_str, 'originalTweets')
    retweets = fetch_tweets(user_id_str, 'retweets')
    quoted_tweets = fetch_tweets(user_id_str, 'quotedStatus')
    print("Data for template:", original_tweets, retweets, quoted_tweets)  # Debugging output
    return render_template('userTweets.html', original_tweets=original_tweets,
                           retweets=retweets, quoted_tweets=quoted_tweets)

@app.route('/top10Users')
def top10Users():
    # Get top users' metrics
    top_users = get_top_users()
    return render_template('top10Users.html', top10Users=top_users)

@app.route('/top10Tweets')
def top10Tweets():
    top_tweets = get_top_tweets()
    return render_template('top10Tweets.html', top_tweets = top_tweets)


@app.route('/viewTweet/<collection_name>/<tweet_id>')
def view_tweet(collection_name, tweet_id):
    from pymongo import MongoClient
    from bson import ObjectId
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitterLarge']
    tweet_data = db[collection_name].find_one({'id_str': tweet_id})
    return render_template('viewTweet.html', tweet=tweet_data)

@app.route('/top_hashtags')
def top_hashtags():
    top10Hashtags = get_top_10_hashtags()  # Call the function here to fetch top hashtags
    return render_template('top10Hashtags.html', top10Hashtags=top10Hashtags)

@app.route('/search_hashtags', methods=['POST'])
def search_hashtags_route():  # Rename the route handler function
    hashtag = request.form['hashtag']
    search_result, searched_hashtag = search_hashtags(hashtag)
    print("Search Result:", search_result)  # Add this line for debugging
    return render_template('searchHashtags.html', search_result=search_result, searched_hashtag=searched_hashtag)

# Add this route for handling sorting requests
@app.route('/search_tweets', methods=['POST'])
def search_tweets_route():
    search_word = request.form.get('search_word', '')
    sort_option = request.form.get('sort_option', '')  # Add this line to get the sorting option
    tweets_with_word, word = search_tweets(search_word, sort_option)  # Pass the sort_option to the search_tweets function
    print("Search Results:", tweets_with_word)  # Debugging output
    print("Search Word:", word)  # Debugging output
    return render_template('searchTweets_result.html', tweets_with_word=tweets_with_word, search_word=word)

@app.teardown_appcontext
def save_cache_on_exit(exception=None):
    cache.save_checkpoint('cache.pkl')

if __name__ == "__main__":
    app.run(debug=True)

