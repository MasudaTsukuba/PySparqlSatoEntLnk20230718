# main030_execute_query for execute sparql queries
# for npd20230626 dataset
# 2023/7/3, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass
from src.TimingClass import TimingClass


if __name__ == '__main__':
    path = PathClass('npd20230626')
    path.set_mapping_file('mapping.json')
    execute = ExecuteQueryClass(path, 'npd20230626', dbms='postgres')
    # query = 'q1.txt'  # uncomment to select a query
    # query = 'q2a.txt'
    # query = 'q2b.txt'
    # query = 'q2c.txt'
    # query = 'q2_MoveableFacility.txt'
    # query = 'q3a.txt'
    # query = 'q3b.txt'
    # query = 'q3c.txt'
    # query = 'q3.txt'
    # query = 'q4a.txt'
    # query = 'q4b.txt'
    # query = 'q4.txt'
    # query = 'q4_ProductionLicence.txt'
    # query = 'q5a.txt'
    # query = 'q5b.txt'
    # query = 'q5b2.txt'
    # query = 'q5c.txt'
    # query = 'q5d.txt'
    # query = 'q5e.txt'
    # query = 'q5.txt'
    query = 'q6a.txt'
    # query = 'q7a.txt'
    # query = 'q8a.txt'
    # query = 'q9a.txt'
    # query = 'q10a.txt'
    # query = 'npd_q01a.txt'
    # query = 'npd_q01b.txt'
    # query = 'npd_q01b0.txt'
    # query = 'npd_q01b2.txt'
    # query = 'npd_q01c.txt'
    # query = 'npd_q01c_filter.txt'
    # query = 'npd_q01d.txt'
    # query = 'npd_q01e.txt'
    # query = 'npd_q01e2.txt'
    # query = 'npd_q01e3.txt'
    # query = 'npd_q01e4.txt'
    # query = 'npd_q01e5.txt'
    # query = 'npd_q01e6.txt'
    # query = 'npd_q01.txt'
    # query = 'npd_q01_star.txt'
    # query = 'npd_q01_order.txt'

    # query = 'npd_q08a.txt'
    # query = 'npd_q08b.txt'
    # query = 'npd_q08c.txt'
    # query = 'npd_q08d.txt'
    # query = 'npd_q08e.txt'
    # query = 'npd_q08.txt'
    # query = 'npd_q08_order.txt'
    TimingClass.set_file_name('timing.csv', time_stamp=True)
    sparql_results = execute.execute_query(query)
    TimingClass.store_timing()
