import os
import pyodbc, struct
import argparse
from azure import identity

def get_conn(driver, serveraddress, dbname, username, password):
    connection_string = 'Driver=' + driver + ';Server=' + serveraddress + '.database.windows.net;Database=' + dbname + ';Uid=' + username + ';Pwd=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

    return pyodbc.connect(connection_string)

    # connection_string = 'Driver='+ driver +';Server=tcp:'+serveraddress+'.database.windows.net,1433;Database=' + dbname +';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

    try:
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

    except Exception as e:
        print("An error occured:", str(e))
    return conn

# get_conn()

parser = argparse.ArgumentParser(description='Process server address, database name, username and password.')
parser.add_argument('serveraddress', type=str, help='the server address')
parser.add_argument('dbname', type=str, help='the database name')
parser.add_argument('username', type=str, help='the username')
parser.add_argument('password', type=str, help='the password')

args = parser.parse_args()
server = args.serveraddress
database = args.dbname
username = args.username
password = args.password
driver= '{ODBC Driver 17 for SQL Server}'

print(f"Server Address: {server}")
print(f"Database Name: {database}")
print(f"Username: {username}")
print(f"Password: {password}")

rows = []
with get_conn(driver, server, database, username, password) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT @@version;") 
    row = cursor.fetchone() 
    while row: 
        print(row[0])
        row = cursor.fetchone()

print(rows)


"""
def get_conn(driver, serveraddress, dbname, username, password):
    connection_string = 'Driver='+ driver +';Server=tcp:'+serveraddress+'.database.windows.net,1433;Database=' + dbname +';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
"""