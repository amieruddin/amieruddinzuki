'''
requirement
1. database
2. table
3. pip install mysql mysql_connect
'''

import mysql.connector
from datetime import datetime

# 1. config database
dell_db = mysql.connector.connect(
	host='127.0.0.1',
	user='root',
	password='',
	database='dell'
	)


print(dell_db)

# 2. connect to database
mycursor = dell_db.cursor()

# 3. set information
now = datetime.now()
query = 'INSERT INTO log(datetime, side, status) VALUES(%s,%s,%s)'
data = [(now, 'left', 'OK')]

# 4. insert to database
mycursor.executemany(query, data)
dell_db.commit()
print(mycursor.rowcount, "data successfull insert.")
