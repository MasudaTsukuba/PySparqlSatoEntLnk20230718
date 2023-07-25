from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('stock_exchange_20230705')
path.set_mapping_file('mapping_gav.json')
execute = ExecuteQueryClass(path, 'stock_exchange_20230629', dbms='postgres')


def test_q1():
    query = 'Q1.txt'
    results = execute.execute_query(query)
    assert len(results) == 15
