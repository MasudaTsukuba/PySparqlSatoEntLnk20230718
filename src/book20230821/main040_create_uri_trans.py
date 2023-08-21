import csv

book_set = set()
book_list = []
with open('../../data/book20230821/csv/query_book_title.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        book_uri = row[0]
        book_id = row[0].split('/')[4]
        if book_id in book_set:
            pass
        else:
            book_set.add(book_id)
            book_list.append([book_id, book_uri])

with open('../../data/book20230821/uri/PREFIX_book.csv', 'w') as csvout:
    csv_writer = csv.writer(csvout)
    csv_writer.writerows(book_list)

author_set = set()
author_list = []
with open('../../data/book20230821/csv/query_book_author.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        author_id = row[2]
        author_uri = row[4]
        if author_id in author_set or author_id == '':
            pass
        else:
            author_set.add(author_id)
            author_list.append([author_id, author_uri])
        author_id = row[3]
        author_uri = row[5]
        if author_id in author_set or author_id == '':
            pass
        else:
            author_set.add(author_id)
            author_list.append([author_id, author_uri])

with open('../../data/book20230821/uri/PREFIX_author.csv', 'w') as csvout:
    csv_writer = csv.writer(csvout)
    csv_writer.writerows(author_list)
