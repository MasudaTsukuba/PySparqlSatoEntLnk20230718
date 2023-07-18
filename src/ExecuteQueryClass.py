# ExecuteQueryClass for execute sparql queries
# 2023/6/14, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import subprocess
from src.DatabaseClass import DataBase
from src.MappingClass import Mapping
from src.SparqlQueryClass import SparqlQuery
from src.UriClass import Uri
from src.OutputClass import Output


class ExecuteQueryClass:
    def __init__(self, path, db_name='landmark.db', dbms='sqlite3', port=8080):
        self.path = path
        self.db_name = db_name
        self.dbms = dbms
        self.port = port

    def query2json(self):  # convert sparql query string into json format
        json_file = self.path.input_query_file.replace('.txt', '.json')  # output json file name
        command = self.path.working_path + '/action_folder/node_modules/sparqljs/bin/sparql-to-json'
        cp = subprocess.run([command, '--strict', self.path.common_query_path + self.path.input_query_file],
                            capture_output=True, text=True)  # , '>', 'query_parse.json'])  # クエリをjson形式に構造化
        if cp.returncode != 0:
            print('Error: sparql-to-json: ', cp.stderr)
            return -1
        with open(self.path.common_query_path + json_file, mode='w') as f:
            f.write(cp.stdout)
        return self.path.common_query_path + json_file

    def execute_query(self, input_file):  # , tables):  # execute a sparql query
        # path = PathClass('data_set2')
        self.path.set_input_query(input_file)
        data_base = DataBase(self.path, self.db_name, dbms=self.dbms, port=self.port)  # instance of DatabaseClass  # 2023/6/1
        # ------ マッピングデータを使ってSPARQL -> SQL に変換する ----------
        # self.path.set_mapping_file('mapping_revised.json')
        mapping_class = Mapping(self.path.mapping_file_path)  # instance of MappingClass
        # ------ ユーザから得て, JSON形式に変換したSPARQLを取り込む --------
        uri = Uri(self.path)  # instance of UriClass
        # uri.read_entity_linking(tables)  # 2023/6/5
        uri.read_entity_linking_from_csv()  # 2023/6/14
        query_json = self.query2json()  # convert the sparql query into json format
        sparql_query = SparqlQuery(query_json, uri)  # instance of SparqlQueryClass
        exe_query = sparql_query.convert_to_sql(mapping_class)  # sparql to intermediate sql
        print(exe_query)  # for debug
        # exe_query = 'SELECT s, name, country_id FROM (SELECT museum_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var501, name AS name FROM museum UNION SELECT hotel_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var701, name AS name FROM hotel UNION SELECT building_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var901, name AS name FROM building UNION SELECT heritage_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var1101, name AS name FROM heritage) NATURAL JOIN (SELECT heritage.heritage_id AS s, "http://example.com/predicate/country" AS Var1301, country.country_id AS country_id FROM heritage_country, heritage, country WHERE heritage.heritage_id = heritage_country.heritage_id AND heritage_country.country_id = country.country_id AND country.country_id != "<http://example.com/country/id/237>");'  # debug
        # exe_query = 'SELECT * FROM "apaAreaNet";'  # "licence";'
        # exe_query = 'SELECT var0 FROM(SELECT "prlNpdidLicence" AS var0 FROM "licence" ) AS FOO ';
#         exe_query = '''
#         SELECT * FROM
# (SELECT hotel_id AS s, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" AS Var201, "http://example.com/ontology/Hotel" AS Var202 FROM hotel)
# NATURAL JOIN
# (
# SELECT museum_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var501, name AS hotel_name FROM museum
# UNION
# SELECT hotel_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var701, name AS hotel_name FROM hotel
# )
#  ;
#
#         '''
#         exe_query = '''
#         SELECT DISTINCT var0, var1 FROM ((SELECT "fclNpdidFacility" AS var0 FROM "facility_moveable" ) AS FOO NATURAL JOIN (SELECT "fclNpdidFacility" AS var0, "fclName" AS var1 FROM "facility_moveable" ) AS FOO10200 );
# '''
#         exe_query = '''
# SELECT var1, var2 FROM ((SELECT CONCAT('npd:licence/', "prlNpdidLicence") AS var0  FROM "licence" ) AS FOO0
# NATURAL JOIN (SELECT CONCAT('npd:licence/', "prlNpdidLicence") AS var0, "prlName" AS var1 FROM "licence" ) AS FOO1
# NATURAL JOIN (SELECT CONCAT('npd:licence/', "prlNpdidLicence") AS var0, "prlDateGranted" AS var2 FROM "licence" WHERE "prlDateGranted" <> '9999-12-31' ) AS FOO2
# NATURAL JOIN (
# SELECT CONCAT('npd:licence/', "prlNpdidLicence") AS var0 FROM "licence" WHERE "prlDateValidTo" <> '9999-12-31'
# ) AS FOO3);
#          '''
        sql_results, headers = data_base.execute(exe_query)  # execute sql query
        data_base.close()
        sparql_results = sparql_query.convert_to_rdf(uri, sql_results, headers)  # convert the sql results back to rdf
        Output.save_file(self.path.output_file_path, sparql_results, headers)  # save the results in a file
        print(len(sparql_results))  # debug info
        return sparql_results  # for pytests
