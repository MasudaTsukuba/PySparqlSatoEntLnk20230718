from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('npd20230626')
path.set_mapping_file('mapping.json')
execute = ExecuteQueryClass(path, 'npd20230626', dbms='postgres')


def test_q1():
    query = 'q1.txt'
    results = execute.execute_query(query)
    assert len(results) == 910


def test_q2_movable_facility():
    query = 'q2_MoveableFacility.txt'
    results = execute.execute_query(query)
    assert len(results) == 192


def test_q3():
    query = 'q3.txt'
    results = execute.execute_query(query)
    assert len(results) == 910


def test_q4a():
    query = 'q4a.txt'
    results = execute.execute_query(query)
    assert len(results) == 0


def test_q5():
    query = 'q5.txt'
    results = execute.execute_query(query)
    assert len(results) == 98


def test_npd_q01():
    query = 'npd_q01.txt'
    results = execute.execute_query(query)
    assert len(results) == 14333


def test_npd_q08():
    query = 'npd_q08.txt'
    results = execute.execute_query(query)
    assert len(results) == 4372
