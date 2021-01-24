import sqlite3
import pandas as pd
from pandas import DataFrame

#If you want to write entire DB to DF-----------------------------------------------------------------------------------
conn = sqlite3.connect('TestDB1.db')
df = pd.read_sql_query("SELECT * FROM CARS", conn)

print(df)



#If you want to write DB to DF, but only select data--------------------------------------------------------------------
conn = sqlite3.connect('TestDB1.db') #just opens connection, doesnt query it
TableName = 'CARS' #Enter in table name

c = conn.cursor() #Creating Cursor - which is needed to fetch results (get rows back)

#Gets list of columns in Table
query = conn.execute("SELECT * From "+TableName)
cols = [column[0] for column in query.description]
print(cols)

#Gets max price from the price column
c.execute('''
SELECT Brand, max(price) FROM CARS
          ''')

#Puts in DF
df = DataFrame(c.fetchall(), columns=['Brand','Price'])
print (df)
