from src.PathClass import PathClass
from src.UriClass import Uri
import sqlite3


path = PathClass('data_set2')


def test_entity_linking_db():
    uri = Uri(path)
    conn = sqlite3.connect(uri.entity_linking_file)
    cursor = conn.cursor()
    sql = 'SELECT * FROM hotel;'
    return_list = cursor.execute(sql).fetchall()
    headers = [col[0] for col in cursor.description]
    results = [list(i) for i in return_list]
    print(results)
    assert len(results) == 822

    sql = 'SELECT * FROM country;'
    return_list = cursor.execute(sql).fetchall()
    headers = [col[0] for col in cursor.description]
    results = [list(i) for i in return_list]
    print(results)
    assert len(results) == 188
    pass
