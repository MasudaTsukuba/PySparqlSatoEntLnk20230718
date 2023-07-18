import sqlite3
import os

working_dir = os.getcwd()
if working_dir.endswith('src'):
    working_dir = os.path.dirname(working_dir)


def test_sql():
    conn = sqlite3.connect(working_dir+'/data/data_set2/csv/landmark.db')
    cursor = conn.cursor()
    sql = 'SELECT * FROM hotel;'
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    assert len(results) == 822

    sql = 'SELECT * FROM building;'
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    assert len(results) == 18556

    sql = 'SELECT * FROM museum;'
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    assert len(results) == 19958

    sql = 'SELECT * FROM heritage;'
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)
    assert len(results) == 5154


if __name__ == '__main__':
    test_sql()
