# create landmark.db in data_set2 folder
# 2023/6/1, Tadashi Masuda

from src.PathClass import PathClass
from src.DatabaseClass import DataBase


if __name__ == '__main__':
    path = PathClass('data_set2')
    db = DataBase(path, 'landmark.db')
    tables = [
        "building", "building_country",
        "hotel", "hotel_country",
        "museum", "museum_country",
        "heritage", "heritage_country",
        "country"
    ]
    db.create_database(tables)
    sqls = [
        "CREATE TABLE building (building_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        "CREATE TABLE building_country (building_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (building_id) REFERENCES building(building_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        "CREATE TABLE hotel (hotel_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        "CREATE TABLE hotel_country (hotel_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        "CREATE TABLE museum (museum_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        "CREATE TABLE museum_country (museum_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (museum_id) REFERENCES museum(museum_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        "CREATE TABLE heritage (heritage_id VARCHAR(255) PRIMARY KEY, name VARCHAR(255), description VARCHAR(255));",
        "CREATE TABLE heritage_country (heritage_id VARCHAR(255), country_id VARCHAR(255), FOREIGN KEY (heritage_id) REFERENCES heritage(heritage_id), FOREIGN KEY (country_id) REFERENCES country(country_id));",
        "CREATE TABLE country (country_id VARCHAR(255) PRIMARY KEY, country_name VARCHAR(255), country_description VARCHAR(255));"
    ]
    db.create_table(sqls)
    path_tables = [
        "Building/Building", "Building/Building_Country",
        "Hotel/Hotel", "Hotel/Hotel_Country",
        "Museum/Museum", "Museum/Museum_Country",
        "Heritage/Heritage", "Heritage/Heritage_Country",
        "Country/Country",
    ]
    sqls = [
        "INSERT INTO building (building_id, name, description) VALUES (?, ?, ?)",
        "INSERT INTO building_country (building_id, country_id) VALUES (?, ?)",
        "INSERT INTO hotel (hotel_id, name, description) VALUES (?, ?, ?)",
        "INSERT INTO hotel_country (hotel_id, country_id) VALUES (?, ?)",
        "INSERT INTO museum (museum_id, name, description) VALUES (?, ?, ?)",
        "INSERT INTO museum_country (museum_id, country_id) VALUES (?, ?)",
        "INSERT INTO heritage (heritage_id, name, description) VALUES (?, ?, ?)",
        "INSERT INTO heritage_country (heritage_id, country_id) VALUES (?, ?)",
        "INSERT INTO country (country_id, country_name, country_description) VALUES (?, ?, ?)"
    ]
    db.insert_data(path_tables, sqls)
