from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('book20230821')
path.set_mapping_file('mapping.json')
execute = ExecuteQueryClass(path, 'book20230821', dbms='postgres')


def test_query_q1():
    result = execute.execute_query('q1.txt')
    assert len(result) == 113816


def test_query_q1_book_type():
    result = execute.execute_query('q1_book_type.txt')
    assert len(result) == 113816


def test_query_q3():
    result = execute.execute_query('q3.txt')
    assert len(result) == 2


def test_query_q3_where():
    result = execute.execute_query('q3_where.txt')
    assert len(result) == 2


def test_query_q4_book_author():
    result = execute.execute_query('q4_book_author.txt')
    assert len(result) == 201163


def test_query_q5():
    result = execute.execute_query('q5.txt')
    assert len(result) == 21
