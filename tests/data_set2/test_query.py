from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('data_set2')
path.set_mapping_file('mapping_revised.json')
execute = ExecuteQueryClass(path)
# tables = ['country', 'building', 'hotel', 'museum', 'heritage']


def test_q1():
    result = execute.execute_query('q1.txt')
    assert len(result) == 801
    result = execute.execute_query('q1_hotel_name_only.txt')  # q1 without country, only hotel id and name
    assert len(result) == 822
    result = execute.execute_query('q1_hotel_country_id.txt')  # q1 wit country_id, but without country name
    assert len(result) == 801
    result = execute.execute_query('q1_pred_hotel_get.txt')  # get predicate of rdf:type as a variable
    assert len(result) == 801
    result = execute.execute_query('q1_pred_get_hotel.txt')  # return predicate value
    assert len(result) == 801


def test_q2():
    result = execute.execute_query('q2.txt')
    assert len(result) == 2146


def test_q3a():
    result = execute.execute_query('q3a.txt')
    assert len(result) == 3732


def test_q3b():
    result = execute.execute_query('q3b.txt')
    assert len(result) == 3695  # 2023/5/8 ????  # 3732  # 2023/7/21  #


def test_q4():
    result = execute.execute_query('q4.txt')
    assert len(result) == 19533  # 19526  # 2023/6/1


def test_q5():
    result = execute.execute_query('q5.txt')  # with filter
    assert len(result) == 43999  # 43980  # 2023/6/1
    result = execute.execute_query('q5b.txt')  # without a filter
    assert len(result) == 43999
    result = execute.execute_query('q5c.txt')  # without a filter, with country_id
    assert len(result) == 43999


def test_q6():
    result = execute.execute_query('q6.txt')
    assert len(result) == 219


def test_q7b():
    result = execute.execute_query('q7b.txt')
    assert len(result) == 0


def test_q1pred_hotel():
    result = execute.execute_query('q1_pred_hotel.txt')
    assert len(result) == 801


def test_q1pred_build():
    result = execute.execute_query('q1_pred_building.txt')
    assert len(result) == 18470


def test_q1pred_museum():
    result = execute.execute_query('q1_pred_museum.txt')
    assert len(result) == 19533  # 19526  # 2023/6/1


def test_q1pred_heritage():
    result = execute.execute_query('q1_pred_heritage.txt')
    assert len(result) == 5195  # 5191  # 2023/6/1


# get types of nay entities
def test_query_type_object_hotel20230518():
    query = 'query_type_object20230518.txt'
    result = execute.execute_query(query)
    assert len(result) == 44678  # 45239  # 2023/6/1


def test_query_extract_hotels():
    result = execute.execute_query('query_extract_hotels20230519.txt')
    assert len(result) == 822


def test_query_extract_hotels_with_name():
    result = execute.execute_query('query_extract_hotels_with_name20230519.txt')
    assert len(result) == 822


def test_query_extract_buildings():
    result = execute.execute_query('query_extract_buildings20230519.txt')
    assert len(result) == 18556


def test_query_extract_museums():
    result = execute.execute_query('query_extract_museums20230519.txt')
    assert len(result) == 19958


def test_query_extract_heritages():
    result = execute.execute_query('query_extract_heritages20230519.txt')
    assert len(result) == 5154


# extract all entities that have labels
def test_query_extract_labels():
    result = execute.execute_query('query_extract_labels20230519.txt')
    assert len(result) == 44490
