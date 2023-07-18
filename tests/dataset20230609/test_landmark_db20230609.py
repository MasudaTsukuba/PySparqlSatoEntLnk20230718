import sqlite3
import os
from src.PathClass import PathClass

working_dir = os.getcwd()
if working_dir.endswith('src'):
    working_dir = os.path.dirname(working_dir)
conn = sqlite3.connect(working_dir+'/data/dataset20230609/csv/landmark.db')
cursor = conn.cursor()


def test_sql():
    sql = 'SELECT * FROM building;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    assert len(results) == 4

    sql = 'SELECT * FROM country;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    assert len(results) == 4

    sql = 'SELECT * FROM building_country;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    assert len(results) == 4


if __name__ == '__main__':
    test_sql()
