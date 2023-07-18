# create entity_linking.db
# 2023/6/1, Tadashi masuda

from src.DatabaseClass import DataBase
from src.PathClass import PathClass
from src.UriClass import Uri


if __name__ == '__main__':
    path = PathClass('dataset20230609')
    database = DataBase(path, 'landmark.db')

    uri = Uri(path)
    # tables = ['country', 'building']
    tables = ['country']
    # sqls = [
    #     'CREATE TABLE building (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));',
    #     'CREATE TABLE country (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));'
    # ]
    sqls = [
        'CREATE TABLE country (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));'
    ]
    uri.create_entity_linking_db(tables, sqls)

    uri.build_entity_linking(database, tables, True, False)
    uri.test_entity_linking(True)
