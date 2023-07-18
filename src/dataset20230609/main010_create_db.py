# create landmark.db in dataset20230609 folder
# 2023/6/1, Tadashi Masuda

from src.PathClass import PathClass
from src.DatabaseClass import DataBase


if __name__ == '__main__':
    path = PathClass('dataset20230609')
    db = DataBase(path, 'landmark.db')
    tables = [
        "building", "building_country",
        "country"
    ]
    db.create_database(tables)
    sqls = [
        "CREATE TABLE building (building_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        "CREATE TABLE building_country (building_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (building_id) REFERENCES building(building_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        "CREATE TABLE country (country_id VARCHAR(255) PRIMARY KEY, country_name VARCHAR(255), country_description VARCHAR(255));"
    ]
    db.create_table(sqls)
    path_tables = [
        "Building/Building", "Building/Building_Country",
        "Country/Country",
    ]
    sqls = [
        "INSERT INTO building (building_id, name, description) VALUES (?, ?, ?)",
        "INSERT INTO building_country (building_id, country_id) VALUES (?, ?)",
        "INSERT INTO country (country_id, country_name, country_description) VALUES (?, ?, ?)"
    ]
    db.insert_data(path_tables, sqls)
