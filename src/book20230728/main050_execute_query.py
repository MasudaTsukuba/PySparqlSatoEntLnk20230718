# main030_execute_query for execute sparql queries
# for book20230728 dataset
# 2023/7/28, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass
from src.TimingClass import TimingClass


if __name__ == '__main__':
    path = PathClass('book20230728')
    path.set_mapping_file('mapping.json')
    execute = ExecuteQueryClass(path, 'book20230728', dbms='postgres')
    # uncomment to select a query
    query = 'q1.txt'
    # query = 'q1_book_type.txt'
    # query = 'q1_author_type.txt'
    # query = 'q1_author_name.txt'
    # query = 'q1_genre_type.txt'
    # query = 'q1_genre_name.txt'
    # query = 'q2.txt'
    query = 'q3.txt'
    # query = 'q4_author.txt'
    # query = 'q4_book_author.txt'

    TimingClass.set_file_name('timing_book20230728.csv', initialize=True, time_stamp=True)
    execute.execute_query(query)
    TimingClass.store_timing()
