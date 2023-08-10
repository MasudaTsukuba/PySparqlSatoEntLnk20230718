# main030_execute_query for execute sparql queries
# for npd20230626 dataset
# 2023/7/3, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass
from src.TimingClass import TimingClass


if __name__ == '__main__':
    path = PathClass('stock_exchange_20230705')
    path.set_mapping_file('mapping.json')
    execute = ExecuteQueryClass(path, 'stock_exchange_20230629', dbms='postgres')

    TimingClass.set_file_name('timing_stock_20230801.csv', initialize=True, time_stamp=True)
    for i in range(5):
        query = 'Q1.txt'  # uncomment to select a query
        execute.execute_query(query)
        TimingClass.store_timing()

        query = 'Q2.txt'
        execute.execute_query(query)
        TimingClass.store_timing()
