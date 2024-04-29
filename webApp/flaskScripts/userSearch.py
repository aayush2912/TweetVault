"""

@author: Naga Satya Dheeraj Anumala, Rohit Kulkarni
"""

import pymysql
import time

# Establishing connection to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Plum@08901',
                             database='twitterLarge',
                             cursorclass=pymysql.cursors.DictCursor)

def search_users(search_criteria, sort_order=None):
    start_time = time.time()
    
    # Base SQL query
    sql_query = """
    SELECT * FROM users
    WHERE screen_name LIKE %s OR id_str = %s OR name LIKE %s
    """

    # Append sorting to the SQL query based on user input
    if sort_order == 'created_at_asc':
        sql_query += " ORDER BY created_at ASC"
    elif sort_order == 'created_at_desc':
        sql_query += " ORDER BY created_at DESC"
    elif sort_order == 'followers_count_asc':
        sql_query += " ORDER BY followers_count ASC"
    elif sort_order == 'followers_count_desc':
        sql_query += " ORDER BY followers_count DESC"
    elif sort_order == 'statuses_count_asc':
        sql_query += " ORDER BY statuses_count ASC"
    elif sort_order == 'statuses_count_desc':
        sql_query += " ORDER BY statuses_count DESC"

    search_criteria_with_wildcard = '%' + search_criteria + '%'

    with connection.cursor() as cursor:
        cursor.execute(sql_query, (search_criteria_with_wildcard, search_criteria, search_criteria_with_wildcard))
        users = cursor.fetchall()
    
    search_time = time.time() - start_time
    return users, search_time





'''
def sort_users(users, sort_option):
    if sort_option == 'created_at_asc':
        return sorted(users, key=lambda x: x.get('created_at', ''))
    elif sort_option == 'created_at_desc':
        return sorted(users, key=lambda x: x.get('created_at', ''), reverse=True)
    elif sort_option == 'followers_count_asc':
        return sorted(users, key=lambda x: x.get('followers_count', 0))
    elif sort_option == 'followers_count_desc':
        return sorted(users, key=lambda x: x.get('followers_count', 0), reverse=True)
    elif sort_option == 'statuses_count_asc':
        return sorted(users, key=lambda x: x.get('statuses_count', 0))
    elif sort_option == 'statuses_count_desc':
        return sorted(users, key=lambda x: x.get('statuses_count', 0), reverse=True)
    else:
        return users  # Default sorting: no sorting applied



def filter_verified(users):
    # Implement filtering logic to return only verified profiles
    # Example: filter users list to contain only profiles with 'verified' == 1
    return [user for user in users if user.get('verified') == 1]
'''