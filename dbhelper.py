import pymysql

# connect to mysql
conn = pymysql.connect(host='127.0.0.1',
                        port=3306,
                        user='root',
                        passwd='',
                        db='simpleatcity',
                        charset='utf8')
curs = conn.cursor()

# execute SQL query
sql = "select * from recipes"
curs.execute(sql)

# fetch data
rows = curs.fetchall()
# all rows
print(rows)

# close connection
conn.close()
