import psycopg2
import csv
import os

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_username = 'masuda'
postgres_password = 'masuda'
cnx = psycopg2.connect(user=postgres_username, password=postgres_password, host='localhost', port=5432, database='book20230821')
cursor = cnx.cursor()

book_set = set()
book_dict = {}
print('book_data')
with open('../../data/book20230821/csv/query_book_title.csv', 'r') as file:
    csv_reader = csv.reader(file)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        book_title = row[1]
        book_dict[book_id] = {}
        book_dict[book_id]['book_title'] = book_title

    with open('../../data/book20230821/csv/query_book_author.csv', 'r') as file:
        csv_reader = csv.reader(file)
        first = True
        for row in csv_reader:
            if first:
                first = False
                continue
            book_id = row[0].split('/')[4]
            book_author = row[2]
            book_author2 = row[3]
            try:
                book_dict[book_id]['book_author'] = book_author
                book_dict[book_id]['book_author2'] = book_author2
            except KeyError:
                pass

    with open('../../data/book20230821/csv/query_book_info.csv', 'r') as file:
        csv_reader = csv.reader(file)
        first = True
        for row in csv_reader:
            if first:
                first = False
                continue
            book_id = row[0].split('/')[4]
            book_date = row[2]
            book_work_category = row[3]
            book_comment = row[4]
            try:
                book_dict[book_id]['book_date'] = book_date
                book_dict[book_id]['book_work_category'] = book_work_category
                book_dict[book_id]['book_comment'] = book_comment
            except KeyError:
                pass

sql = '''
    INSERT INTO data (id, title, author_name, author_name2, date, work_category, comment) VALUES (%s, %s, %s, %s, %s, %s, %s);
'''
# id_number = 1
for key, value in book_dict.items():
    try:
        book_title = ''
        try:
            book_title = value['book_title']
        except KeyError:
            pass
        book_author = ''
        try:
            book_author = value['book_author']
        except KeyError:
            pass
        book_author2 = ''
        try:
            book_author2 = value['book_author2']
        except KeyError:
            pass
        book_date = ''
        try:
            book_date = value['book_date']
        except KeyError:
            pass
        book_work_category = ''
        try:
            book_work_category = value['book_work_category']
        except KeyError:
            pass
        book_comment = ''
        try:
            book_comment = value['book_comment']
        except KeyError:
            pass
        cursor.execute(sql, [key, book_title, book_author, book_author2, book_date, book_work_category, book_comment])
        book_set.add(book_id)
    except Exception as e:
        print(e)
        print(key)
        pass
        # break
    pass
    # id_number += 1
cnx.commit()

cursor.close()
cnx.close()
pass
