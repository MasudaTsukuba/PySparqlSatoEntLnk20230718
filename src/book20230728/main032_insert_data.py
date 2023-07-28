import psycopg2
import csv
import os

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_username = 'masuda'
postgres_password = 'masuda'
cnx = psycopg2.connect(user=postgres_username, password=postgres_password, host='localhost', port=5432, database='book20230728')
cursor = cnx.cursor()

with open('../../data/book20230728/csv/book_title.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO book_title (id, title) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        book_title = row[1]
        try:
            cursor.execute(sql, [book_id, book_title])
        except:
            pass
        pass

with open('../../data/book20230728/csv/author_label.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO author (author_id, name) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        author_id = row[0].split('/')[4]
        name = row[1]
        try:
            cursor.execute(sql, [author_id, name])
        except:
            pass
        pass

with open('../../data/book20230728/csv/genre_label.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO genre (genre_id, genre_label) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        genre_id = row[0].split('/')[4]
        genre_label = row[1]
        try:
            cursor.execute(sql, [genre_id, genre_label])
        except:
            pass
        pass

with open('../../data/book20230728/csv/book_author.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO book_title (id, author_id) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        author_id = row[1]
        try:
            cursor.execute(sql, [book_id, author_id])
        except:
            pass
        pass

with open('../../data/book20230728/csv/book_genre.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO book_title (id, genre_id) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        genre_id = row[1]
        try:
            cursor.execute(sql, [book_id, genre_id])
        except:
            pass
        pass

with open('../../data/book20230728/csv/book_date.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO book_title (id, pub_date) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        pub_date = row[1]
        try:
            cursor.execute(sql, [book_id, pub_date])
        except:
            pass
        pass

with open('../../data/book20230728/csv/book_description.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    first = True

    sql = '''
    INSERT INTO book_title (id, description) VALUES (%s, %s);
    '''
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        description = row[1]
        try:
            cursor.execute(sql, [book_id, description])
        except:
            pass
        pass

cnx.commit()
cursor.close()
cnx.close()
pass
