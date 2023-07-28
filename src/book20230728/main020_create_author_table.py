import csv

author_set = set()
author_list = []
with open('../../data/book20230728/csv/book_author.csv', 'r') as input_file:
    csv_reader = csv.reader(input_file)

    first = True
    for line in csv_reader:
        if first:
            first = False
            continue
        author_uri = line[1]
        author_label = line[2]
        if author_uri in author_set:
            pass
        else:
            author_list.append([author_uri, author_label])
            author_set.add(author_uri)

with open('../../data/book20230728/csv/author_label.csv', 'w', encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["author_uri", "author_label"])
    csv_writer.writerows(author_list)
