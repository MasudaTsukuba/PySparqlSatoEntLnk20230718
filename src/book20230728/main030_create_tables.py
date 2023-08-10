import psycopg2
import csv
import os

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_username = 'masuda'
postgres_password = 'masuda'
cnx = psycopg2.connect(user=postgres_username, password=postgres_password, host='localhost', port=5432, database='book20230728')
cursor = cnx.cursor()
sql_drop_book_title = '''
DROP TABLE IF EXISTS book_title CASCADE;
'''
cursor.execute(sql_drop_book_title)
sql_create_book_title = '''
CREATE TABLE book_title (book_id VARCHAR(255) PRIMARY KEY, book_title VARCHAR(255));
'''
cursor.execute(sql_create_book_title)

sql_drop_author = '''
DROP TABLE IF EXISTS author CASCADE;
'''
cursor.execute(sql_drop_author)
sql_create_author = '''
CREATE TABLE author (author_id VARCHAR(255) PRIMARY KEY, author_name VARCHAR(255));
'''
cursor.execute(sql_create_author)

sql_drop_genre = '''
DROP TABLE IF EXISTS genre CASCADE;
'''
cursor.execute(sql_drop_genre)
sql_create_genre = '''
CREATE TABLE genre (genre_id VARCHAR(255) PRIMARY KEY, genre_label VARCHAR(255));
'''
cursor.execute(sql_create_genre)

sql_drop_book_author = '''
DROP TABLE IF EXISTS book_author;
'''
cursor.execute(sql_drop_book_author)
sql_create_book_author = '''
CREATE TABLE book_author (book_id VARCHAR(255), author_id VARCHAR(255), 
CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book_title (book_id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES author (author_id) ON DELETE CASCADE ON UPDATE CASCADE);
'''
sql_create_book_author = '''
CREATE TABLE book_author (book_id VARCHAR(255), author_id VARCHAR(255));
'''
cursor.execute(sql_create_book_author)

sql_drop_book_date = '''
DROP TABLE IF EXISTS book_date;
'''
cursor.execute(sql_drop_book_date)
sql_create_book_date = '''
CREATE TABLE book_date (book_id VARCHAR(255), pub_date VARCHAR(255), CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book_title (book_id) ON DELETE CASCADE ON UPDATE CASCADE);
'''
sql_create_book_date = '''
CREATE TABLE book_date (book_id VARCHAR(255), pub_date VARCHAR(255));
'''
cursor.execute(sql_create_book_date)

sql_drop_book_genre = '''
DROP TABLE IF EXISTS book_genre;
'''
cursor.execute(sql_drop_book_genre)
sql_create_book_genre = '''
CREATE TABLE book_genre (book_id VARCHAR(255), genre_id VARCHAR(255), 
CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book_title (book_id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_genre_id FOREIGN KEY (genre_id) REFERENCES genre (genre_id) ON DELETE CASCADE ON UPDATE CASCADE);
'''
sql_create_book_genre = '''
CREATE TABLE book_genre (book_id VARCHAR(255), genre_id VARCHAR(255));
'''
cursor.execute(sql_create_book_genre)
cnx.commit()

sql_drop_book_description = '''
DROP TABLE IF EXISTS book_description;
'''
cursor.execute(sql_drop_book_description)
sql_create_book_description = '''
CREATE TABLE book_description (book_id VARCHAR(255), book_description VARCHAR(255), 
CONSTRAINT fk_book_id FOREIGN KEY (book_id) REFERENCES book_title (book_id) ON DELETE CASCADE ON UPDATE CASCADE);
'''
sql_create_book_description= '''
CREATE TABLE book_description (book_id VARCHAR(255), book_description VARCHAR(255));
'''
cursor.execute(sql_create_book_description)
cnx.commit()

cursor.close()
cnx.close()
pass
