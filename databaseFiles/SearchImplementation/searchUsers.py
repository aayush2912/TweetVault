"""

@author: Manas Maskar, Aayush Pradhan
"""

import pymysql
import json
import time

# Establishing connection to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Plum@08901',
                             database='twitterLarge',
                             cursorclass=pymysql.cursors.DictCursor)

#enter search criteria
search_criteria = input("Enter search criteria (username, user ID_str, or full name): ")


start_time_user = time.time()

# SQL query to fetch all columns based on search criteria
sql_query = """
SELECT * FROM users
WHERE screen_name LIKE %s OR id_str = %s OR name LIKE %s
"""
search_criteria_with_wildcard = '%' + search_criteria + '%'
with connection.cursor() as cursor:
    cursor.execute(sql_query, (search_criteria_with_wildcard, search_criteria, search_criteria_with_wildcard))

    # Fetch all matching user records
    result = cursor.fetchall()
    
    for user in result:
        print(user)  

end_time_user = time.time()


print("--------------------------->>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<------------------------------")
print(f"Search time: {end_time_user - start_time_user} seconds")

