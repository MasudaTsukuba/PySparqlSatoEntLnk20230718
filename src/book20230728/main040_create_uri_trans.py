import csv

book_set = set()
book_list = []
with open('../../data/book20230728/csv/book_title.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        book_id = row[0].split('/')[4]
        book_uri = row[0]
        if book_id in book_set:
            pass
        else:
            book_set.add(book_id)
            book_list.append([book_id, book_uri])

with open('../../data/book20230728/uri/PREFIX_book.csv', 'w') as csvout:
    csv_writer = csv.writer(csvout)
    csv_writer.writerows(book_list)

author_set = set()
author_list = []
with open('../../data/book20230728/csv/author_label.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        author_id = row[0].split('/')[4]
        author_uri = row[0]
        if author_id in author_set:
            pass
        else:
            author_set.add(author_id)
            author_list.append([author_id, author_uri])

with open('../../data/book20230728/uri/PREFIX_author.csv', 'w') as csvout:
    csv_writer = csv.writer(csvout)
    csv_writer.writerows(author_list)

genre_set = set()
genre_list = []
with open('../../data/book20230728/csv/genre_label.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    first = True
    for row in csv_reader:
        if first:
            first = False
            continue
        genre_id = row[0].split('/')[4]
        genre_uri = row[0]
        if genre_id in genre_set:
            pass
        else:
            genre_set.add(genre_id)
            genre_list.append([genre_id, genre_uri])

with open('../../data/book20230728/uri/PREFIX_genre.csv', 'w') as csvout:
    csv_writer = csv.writer(csvout)
    csv_writer.writerows(genre_list)

