from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('dataset20230609')
path.set_mapping_file('mapping_revised.json')
execute = ExecuteQueryClass(path)


def test_query():
    result = execute.execute_query('3_q1.txt')
    assert len(result) == 4
    result = execute.execute_query('3_q2.txt')
    assert len(result) == 3
    result = execute.execute_query('3_q3.txt')
    assert len(result) == 3
    result = execute.execute_query('query_with_OR_in_filter20230615.txt')
    assert len(result) == 2
    result = execute.execute_query('query_with_AND_in_filter20230616.txt')
    assert len(result) == 1
    result = execute.execute_query('query_with_OR_AND_in_filter20230616.txt')
    assert len(result) == 1
    result = execute.execute_query('query_with_OR_OR_AND_in_filter20230616.txt')
    assert len(result) == 2
    result = execute.execute_query('query_with_NOT_in_filter20230616.txt')
    assert len(result) == 3
