# create entity_linking.db
# 2023/6/1, Tadashi masuda

from src.DatabaseClass import DataBase
from src.PathClass import PathClass
from src.UriClass import Uri


if __name__ == '__main__':
    path = PathClass('data_set2')
    database = DataBase(path, 'landmark.db')

    uri = Uri(path)
    tables = ['country', 'hotel', 'building', 'museum', 'heritage']
    sqls = [
        'CREATE TABLE hotel (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));',
        'CREATE TABLE building (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));',
        'CREATE TABLE museum (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));',
        'CREATE TABLE heritage (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));',
        'CREATE TABLE country (id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), status VARCHAR(255));'
    ]
    uri.create_entity_linking_db(tables, sqls)

    uri.build_entity_linking(database, tables)
    uri.test_entity_linking()
