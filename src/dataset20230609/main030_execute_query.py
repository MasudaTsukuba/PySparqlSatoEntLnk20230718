# main030_execute_query for execute sparql queries
# for dataset20230609
# 2023/6/14, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass


if __name__ == '__main__':
    path = PathClass('dataset20230609')
    execute = ExecuteQueryClass(path)
    query = '3_q1.txt'  # uncomment to select a query
    query = '3_q2.txt'
    query = '3_q3.txt'
    query = 'query_with_OR_in_filter20230615.txt'
    query = 'query_with_AND_in_filter20230616.txt'
    query = 'query_with_OR_AND_in_filter20230616.txt'
    # query = 'query_with_OR_OR_AND_in_filter20230616.txt'
    query = 'query_with_NOT_in_filter20230616.txt'
    execute.execute_query(query)
