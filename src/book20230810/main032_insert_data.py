import psycopg2
import csv
import os

postgres_username = os.environ.get('POSTGRES_USERNAME')
postgres_password = os.environ.get('POSTGRES_PASSWORD')
postgres_username = 'masuda'
postgres_password = 'masuda'
cnx = psycopg2.connect(user=postgres_username, password=postgres_password, host='localhost', port=5432, database='book20230810')
cursor = cnx.cursor()

book_set = set()
print('book_data')
with open('../../data/book20230810/csv/data.csv', 'r') as file:
    first = True

    sql = '''
    INSERT INTO data (id, title, author_name, author_name2, date, work_category, comment) VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    id_number = 1
    for line in file:
        if first:
            first = False
            continue
        row = line.strip().split('|')
        try:
            cursor.execute(sql, [id_number, row[0], row[1], row[2], row[3], row[4], row[5]])
            # book_set.add(book_id)
        except Exception as e:
            print(e)
            print(row)
            pass
            # break
        pass
        id_number += 1
    cnx.commit()

cursor.close()
cnx.close()
pass
