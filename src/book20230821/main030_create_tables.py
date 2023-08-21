import psycopg2
import csv
import os

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_username = 'masuda'
postgres_password = 'masuda'
cnx = psycopg2.connect(user=postgres_username, password=postgres_password, host='localhost', port=5432, database='book20230821')
cursor = cnx.cursor()
sql_drop_book_title = '''
DROP TABLE IF EXISTS data CASCADE;
'''
cursor.execute(sql_drop_book_title)
sql_create_data_table = '''
CREATE TABLE data (id VARCHAR(255) PRIMARY KEY, title VARCHAR(255), author_name VARCHAR(255), author_name2 VARCHAR(255), date VARCHAR(255), work_category VARCHAR(255), comment VARCHAR(255));
'''
cursor.execute(sql_create_data_table)

cnx.commit()

cursor.close()
cnx.close()
pass
