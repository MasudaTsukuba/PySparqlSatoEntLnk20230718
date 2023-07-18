# import os
# import subprocess
from src.ExecuteQueryClass import ExecuteQueryClass
# from src.MappingClass import Mapping
# from src.DatabaseClass import DataBase
# from src.SparqlQueryClass import SparqlQuery
# from src.UriClass import Uri
# from src.OutputClass import Output
from src.PathClass import PathClass


# def query2json(path):  # convert sparql query string into json format
#     json_file = path.input_query_file.replace('.txt', '.json')  # output json file name
#     command = path.working_path + '/action_folder/node_modules/sparqljs/bin/sparql-to-json'
#     cp = subprocess.run([command, '--strict', path.common_query_path + path.input_query_file],
#                         capture_output=True, text=True)  # , '>', 'query_parse.json'])  # クエリをjson形式に構造化
#     if cp.returncode != 0:
#         print('Error: sparql-to-json: ', cp.stderr)
#         return -1
#     with open(path.working_path+'/'+json_file, mode='w') as f:
#         f.write(cp.stdout)
#     return path.working_path+'/'+json_file
#
#
# def execute_query(input_file):
#     path = PathClass('data_set2')
#     path.set_input_query(input_file)
#     data_base = DataBase(path, 'landmark.db')  # 2023/6/1
#     # ------ マッピングデータを使ってSPARQL -> SQL に変換する ----------
#     path.set_mapping_file('mapping_revised.json')
#     mapping_class = Mapping(path.mapping_file_path)
#     # ------ ユーザから得て, JSON形式に変換したSPARQLを取り込む --------
#     uri = Uri(path)
#     uri.read_entity_linking()  # 2023/6/5
#     sparql_query = SparqlQuery(query2json(path), uri)
#     exe_query = sparql_query.convert_to_sql(mapping_class)  # sparql to intermediate sql
#     print(exe_query)  # for debug
#     # exe_query = 'SELECT s, name, country_id FROM (SELECT museum_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var501, name AS name FROM museum UNION SELECT hotel_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var701, name AS name FROM hotel UNION SELECT building_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var901, name AS name FROM building UNION SELECT heritage_id AS s, "http://www.w3.org/2000/01/rdf-schema#label" AS Var1101, name AS name FROM heritage) NATURAL JOIN (SELECT heritage.heritage_id AS s, "http://example.com/predicate/country" AS Var1301, country.country_id AS country_id FROM heritage_country, heritage, country WHERE heritage.heritage_id = heritage_country.heritage_id AND heritage_country.country_id = country.country_id AND country.country_id != "<http://example.com/country/id/237>");'  # debug
#     sql_results, headers = data_base.execute(exe_query)  # execute sql query
#     data_base.close()
#     sparql_results = sparql_query.convert_to_rdf(uri, sql_results)  # back to rdf
#     Output.save_file(path.output_file_path, sparql_results, headers)  # save in a file
#     print(len(sparql_results))  # debug info
#     return sparql_results  # for tests


if __name__ == '__main__':
    path = PathClass('data_set2')
    path.set_mapping_file('mapping_revised.json')
    execute = ExecuteQueryClass(path)
    query = 'q1.txt'
    # query = 'q2_MoveableFacility.txt'
    # query = 'q3a.txt'
    # query = 'q3b.txt'
    # query = 'q4.txt'
    # query = 'q5.txt'
    # query = 'q6.txt'
    # query = 'q7.txt'
    # query = 'q7b.txt'
    # query = 'q1_pred_hotel.txt'
    # query = 'q1_pred_building.txt'
    # query = 'q1_pred_museum.txt'
    # query = 'q1_pred_heritage.txt'
    # query = 'query_type_object20230518.txt'
    # query = 'query_extract_hotels20230519.txt'
    # query = 'query_extract_hotels_with_name20230519.txt'
    # query = 'query_extract_buildings20230519.txt'
    # query = 'query_extract_museums20230519.txt'
    # query = 'query_extract_heritages20230519.txt'
    # query = 'query_extract_labels20230519.txt'
    # query = 'q5b.txt'
    # query = 'q5c.txt'
    # query = 'q1_hotel_name_only.txt'  # q1 without country, only hotel id and name
    # query = 'q1_hotel_country_id.txt'  # q1 wit country_id, but without country name
    # query = 'q1_pred_hotel_get.txt'  # predicate for rdf:type is variable
    # query = 'q1_pred_get_hotel.txt'  # return predicate value
    # query = 'query_description.txt'
    execute.execute_query(query)
