from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('book20230810')
path.set_mapping_file('mapping.json')
execute = ExecuteQueryClass(path, 'book20230810', dbms='postgres')


def test_query_q1():
    result = execute.execute_query('q1.txt')
    assert len(result) == 86471


def test_query_q14_book_author():
    result = execute.execute_query('q4_book_author.txt')
    assert len(result) == 172933
