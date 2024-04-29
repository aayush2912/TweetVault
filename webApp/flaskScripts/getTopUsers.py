"""

@author: Manas Maskar, Aayush Pradhan
"""

import pymysql 

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Plum@08901',
    database='twitterLarge'
)

cursor = connection.cursor()

def get_top_users():
    top10_uQuery = """
SELECT 
    id_str,
    screen_name,
    (
        -- Points for default image
        CASE WHEN default_profile_image = 1 THEN -15 ELSE 10 END +
        -- Points for default profile
        CASE WHEN default_profile = 1 THEN -15 ELSE 10 END +
        -- Points for verified profile
        CASE WHEN verified = 1 THEN 100 ELSE 0 END +
        -- Points for URL
        CASE WHEN url IS NOT NULL THEN 25 ELSE -30 END +
        -- Points for description
        CASE WHEN description IS NOT NULL THEN 25 ELSE -30 END +
        -- Points for followers count
        CASE 
            WHEN followers_count BETWEEN 11 AND 30 THEN 5
            WHEN followers_count BETWEEN 31 AND 90 THEN 10
            WHEN followers_count BETWEEN 91 AND 150 THEN 20
            WHEN followers_count BETWEEN 151 and 400 THEN 30
			WHEN followers_count BETWEEN 401 and 1000 THEN 45
			WHEN followers_count BETWEEN 1001 and 3500 THEN 50
			WHEN followers_count BETWEEN 3501 and 7000 THEN 70
            WHEN followers_count BETWEEN 7001 and 12000 THEN 90
            WHEN followers_count BETWEEN 12001 and 30000 THEN 100
            WHEN followers_count BETWEEN 30001 and 99998 THEN 200
            WHEN followers_count BETWEEN 99999 and 1000000 THEN 300
            WHEN followers_count > 1000000 THEN 400
            ELSE 0
        END +
        CASE 
            WHEN listed_count BETWEEN 11 AND 30 THEN 5
            WHEN listed_count BETWEEN 31 AND 90 THEN 10
            WHEN listed_count BETWEEN 91 AND 150 THEN 20
            WHEN listed_count BETWEEN 151 and 400 THEN 30
			WHEN listed_count BETWEEN 401 and 1000 THEN 45
			WHEN listed_count BETWEEN 1001 and 3500 THEN 50
			WHEN listed_count BETWEEN 3501 and 7000 THEN 70
            WHEN listed_count BETWEEN 7001 and 12000 THEN 90
            WHEN listed_count BETWEEN 12001 and 30000 THEN 100
            WHEN listed_count BETWEEN 30001 and 99998 THEN 200
            WHEN listed_count BETWEEN 99999 and 1000000 THEN 300
            WHEN listed_count > 1000000 THEN 400
            ELSE 0
		END +
		CASE 
            WHEN favourites_count BETWEEN 11 AND 30 THEN 5
            WHEN favourites_count BETWEEN 31 AND 90 THEN 10
            WHEN favourites_count BETWEEN 91 AND 150 THEN 20
            WHEN favourites_count BETWEEN 151 and 400 THEN 30
			WHEN favourites_count BETWEEN 401 and 1000 THEN 45
			WHEN favourites_count BETWEEN 1001 and 3500 THEN 50
			WHEN favourites_count BETWEEN 3501 and 7000 THEN 70
            WHEN favourites_count BETWEEN 7001 and 12000 THEN 90
            WHEN favourites_count BETWEEN 12001 and 30000 THEN 100
            WHEN favourites_count BETWEEN 30001 and 99998 THEN 200
            WHEN favourites_count BETWEEN 99999 and 1000000 THEN 300
            WHEN favourites_count > 1000000 THEN 400
            ELSE 0
		END + 
        CASE 
            WHEN statuses_count BETWEEN 11 AND 30 THEN 5
            WHEN statuses_count BETWEEN 31 AND 90 THEN 10
            WHEN statuses_count BETWEEN 91 AND 150 THEN 20
            WHEN statuses_count BETWEEN 151 and 400 THEN 30
			WHEN statuses_count BETWEEN 401 and 1000 THEN 45
			WHEN statuses_count BETWEEN 1001 and 3500 THEN 50
			WHEN statuses_count BETWEEN 3501 and 7000 THEN 70
            WHEN statuses_count BETWEEN 7001 and 12000 THEN 90
            WHEN statuses_count BETWEEN 12001 and 30000 THEN 100
            WHEN statuses_count BETWEEN 30001 and 99998 THEN 200
            WHEN statuses_count BETWEEN 99999 and 1000000 THEN 300
            WHEN statuses_count > 1000000 THEN 400
            ELSE 0
        END
    ) / 9 AS metric1_score
FROM 
    users
ORDER BY 
    metric1_score DESC
LIMIT 
    10;
"""
    cursor.execute(top10_uQuery)
    topUsers = cursor.fetchall()
    return topUsers
