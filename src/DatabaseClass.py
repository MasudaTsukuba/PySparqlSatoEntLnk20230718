# class for handling a relational database
# and execute sql query against the database
# 2023/6/1, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import os
import sqlite3
import mysql.connector
import psycopg2
import csv
# from src.PathClass import PathClass


class DataBase:
    def __init__(self, path, db_name, dbms='sqlite3', port=8080):
        self.path = path
        self.dataset_csv_path = path.dataset_path+'/csv/'
        self.database_path = self.dataset_csv_path+db_name
        if dbms == 'sqlite3':
            try:
                self.conn = sqlite3.connect(self.database_path)
            except Exception as e:
                with open(self.database_path, 'w') as file:  # create an empty file
                    pass
                pass
        elif dbms == 'mysql':
            mysql_username = os.environ.get('MYSQL_USERNAME')
            mysql_password = os.environ.get('MYSQL_PASSWORD')
            self.conn = mysql.connector.connect(user=mysql_username, password=mysql_password, host='localhost', database=db_name, port=port)
            pass
        elif dbms == 'postgres':
            postgres_username = os.environ.get('POSTGRES_USERNAME')
            postgres_password = os.environ.get('POSTGRES_PASSWORD')
            postgres_username = 'masuda'
            postgres_password = 'masuda'
            try:
                # self.conn = psycopg2.connect(f'postgresql://{postgres_username}:{postgres_password}@localhost/{db_name}')
                self.conn = psycopg2.connect(host='localhost', user=postgres_username, password=postgres_password, database=db_name)
                # self.conn = psycopg2.connect(host='localhost', user=postgres_username, password=postgres_password, port=5433, database=db_name)  # docker
            except (Exception, psycopg2.Error) as error:
                print('Error while connecting to the postgres database:', error)
            pass
        else:
            print('INVALID DATABASE MANAGEMENT SYSTEM. Choose from sqlite3, mysql and postgres. ')
        try:
            self.cur = self.conn.cursor()
        except Exception:
            print('cursor() failed. ')
        self.tables = None  # list of tables
        self.sqls = None  # list of sqls

    def close(self):
        self.conn.close()

    # execute sql query against a relational database
    def execute(self, sql):
        # print(sql)  # debug  # 2023/7/21
        xxx = self.cur.execute(sql)
        zzz = self.cur.rowcount
        return_list = self.cur.fetchall()  # execute sql and fetch the results
        headers = [col[0] for col in self.cur.description]  # extract the headers
        results = [list(i) for i in return_list]  # convert the results into 2-D list
        return results, headers

    def create_database(self, tables):  # create a sqlite3 database
        self.tables = tables
        conn = sqlite3.connect(self.database_path)
        conn.commit()
        conn.close()

    def create_table(self, sqls):  # create sqlite3 tables
        self.sqls = sqls
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        # tables = [
        #     "building", "building_country",
        #     "hotel", "hotel_country",
        #     "museum", "museum_country",
        #     "heritage", "heritage_country",
        #     "country"
        # ]
        for table in self.tables:
            sql = "DROP TABLE " + table + ";"
            try:
                cursor.execute(sql)
            except:
                print('DROP FAILED: ' + table)
                pass
            # finally:
            #     if cnx:
            #         cnx.close()

        # sqls = [
        #     "CREATE TABLE building (building_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        #     "CREATE TABLE building_country (building_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (building_id) REFERENCES building(building_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        #     "CREATE TABLE hotel (hotel_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        #     "CREATE TABLE hotel_country (hotel_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        #     "CREATE TABLE museum (museum_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        #     "CREATE TABLE museum_country (museum_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (museum_id) REFERENCES museum(museum_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        #     "CREATE TABLE heritage (heritage_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        #     "CREATE TABLE heritage_country (heritage_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (heritage_id) REFERENCES heritage(heritage_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        #     "CREATE TABLE country (country_id VARCHAR(255) PRIMARY KEY, country_name VARCHAR(255), country_description VARCHAR(255));"
        # ]

        for sql in sqls:
            try:
                cursor.execute(sql)
                print('CREATE TABLE SUCCEEDED: ' + sql)
                pass
            except:
                print('CREATE TABLE FAILED: ' + sql)
                pass
            # finally:
            #     if cnx:
            #         cnx.close()

        cursor.close()
        conn.commit()
        conn.close()

    def insert_data(self, path_tables, sqls):  # insert data into sqlite3 tables
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        # tables = [
        #     "building", "building_country",
        #     "hotel", "hotel_country",
        #     "museum", "museum_country",
        #     "heritage", "heritage_country",
        #     "country"
        # ]

        # path_tables = [
        #     "Building/Building", "Building/Building_Country",
        #     "Hotel/Hotel", "Hotel/Hotel_Country",
        #     "Museum/Museum", "Museum/Museum_Country",
        #     "Heritage/Heritage", "Heritage/Heritage_Country",
        #     "Country/Country",
        # ]
        # sqls = [
        #     "INSERT INTO building (building_id, name, description) VALUES (?, ?, ?)",
        #     "INSERT INTO building_country (building_id, country_id) VALUES (?, ?)",
        #     "INSERT INTO hotel (hotel_id, name, description) VALUES (?, ?, ?)",
        #     "INSERT INTO hotel_country (hotel_id, country_id) VALUES (?, ?)",
        #     "INSERT INTO museum (museum_id, name, description) VALUES (?, ?, ?)",
        #     "INSERT INTO museum_country (museum_id, country_id) VALUES (?, ?)",
        #     "INSERT INTO heritage (heritage_id, name, description) VALUES (?, ?, ?)",
        #     "INSERT INTO heritage_country (heritage_id, country_id) VALUES (?, ?)",
        #     "INSERT INTO country (country_id, country_name, country_description) VALUES (?, ?, ?)"
        # ]

        for table, path_table, sql in zip(self.tables, path_tables, sqls):
            file = self.dataset_csv_path + path_table + ".csv"  # data are read from csv files
            print(path_table)  # for debug
            with open(file, 'r') as csvfile:  # open a csv file
                reader = csv.reader(csvfile)
                first = True  # skip the title line
                for row in reader:
                    if first:
                        first = False  # title line has been skipped
                    else:
                        try:
                            # print(row)  # for debug
                            cursor.execute(sql, row)  # insert one line into a table
                        except Exception as e:  # something unexpected happened
                            print(e)
                            pass
                conn.commit()  # this is necessary to complete the insert
        cursor.close()
        conn.close()
