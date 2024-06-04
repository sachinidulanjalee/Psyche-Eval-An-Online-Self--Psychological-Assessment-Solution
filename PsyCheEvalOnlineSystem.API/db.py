import pyodbc

SERVER = 'LT-PE4-29\\SQLEXPRESS'  # Double backslashes in the server name
DATABASE = 'PsycheEval'
USERNAME = 'sa'
PASSWORD = '#compaq123'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

#
# cursor = conn.cursor()
#
# # Now, you can execute your SQL queries
# cursor.execute("INSERT INTO [User] (fullname, username, [password]) VALUES (?, ?, ?)", (535, 'Scott', 'Manager'))
# conn.commit()  # Commit the transaction
#
# cursor.execute("SELECT * FROM [User]")
# row = cursor.fetchone()
# while row:
#     print(row)
#     row = cursor.fetchone()
#
# # Close the cursor and the connection when you're done
# cursor.close()
# conn.close()
