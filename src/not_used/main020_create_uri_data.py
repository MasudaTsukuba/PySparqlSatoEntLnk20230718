# create URI_data.db
# 2023/6/1, Tadashi masuda

import os
import csv
import sqlite3
from src.PathClass import PathClass
from src.UriClass import Uri


# column_dict = {'PREFIX_Build': 'URI_Build', 'PREFIX_hotel': 'URI_hotel', 'PREFIX_museum': 'URI_museum', 'PREFIX_WH': 'URI_WH', 'PREFIX_Country': 'URI_Country'}


# store the contents of PREFIX*.csv files into a sqlite3 database named URI_data.db
# def csv_to_sqlite(csv_file, db_file, table_name):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     with open(csv_file, 'r') as input_file:
#         csv_reader = csv.reader(input_file)
#         header = ['ID', csv_file.split('/')[-1].replace('.csv', '').replace('PREFIX', 'uri')]  # next(csv_reader)
#         columns = [f'{column} TEXT' for column in header]
#         try:
#             drop_table_query = f'DROP TABLE {table_name}'  # drop the table to create from zero
#             cursor.execute(drop_table_query)
#         except:
#             pass
#         # create a table
#         create_table_query = f'CREATE TABLE {table_name} ({", ".join(columns)})'
#         cursor.execute(create_table_query)
#
#         # insert the csv data
#         insert_query = f'INSERT INTO {table_name} VALUES ({", ".join(["?"] * len(header))})'
#         for row in csv_reader:
#             cursor.execute(insert_query, row)
#     conn.commit()
#     conn.close()


# uri_path = path.working_path+'/data_set2/uri/'  # '../data_set2/uri/'
# files = os.listdir(uri_path)
# for file in files:
#     if file.startswith('PREFIX'):  # read all the file with a file name starting with 'PREFIX'
#         print(file)
#         csv_file = uri_path+file
#         db_file = uri_path+'URI_data.db'
#         table_name = file.replace('.csv', '')
#         csv_to_sqlite(csv_file, db_file, table_name)  # save the contents of the csv files into sqlite3 database
# pass

if __name__ == '__main__':
    path = PathClass('')
    uri = Uri(path, 'data_set2', 'uri')
    uri.create_uri_db()
