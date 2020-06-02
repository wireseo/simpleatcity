import pymysql
import pandas as pd

# connect to mysql
db = pymysql.connect(host='simpleatcitydb.crbqchzceqdz.ap-southeast-1.rds.amazonaws.com',
                        port=3306,
                        user='westmoon',
                        passwd='simpleatcity',
                        db='simpleatcitydb',
                        charset='utf8')
curs = db.cursor()

# execute SQL query
sql = "SELECT * from recipes"
curs.execute(sql)

# fetch data
rows = curs.fetchall()

# all rows
print(rows[0])

# close connection
db.close()
