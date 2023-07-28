# ExecuteQueryClass for execute sparql queries
# 2023/6/14, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import subprocess
from src.DatabaseClass import DataBase
from src.MappingClass import Mapping
from src.SparqlQueryClass import SparqlQuery
from src.UriClass import Uri
from src.OutputClass import Output
from src.TimingClass import TimingClass


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
        total_execution_timing = TimingClass(input_file, 'total_execution')
        # total_timing.record_start()
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

        sparql2sql_timing = TimingClass(input_file, 'sparql_to_sql')
        # sparql2sql_timing.record_start()
        sparql_query = SparqlQuery(query_json, uri)  # instance of SparqlQueryClass
        sparql_query.query_in_json = sparql_query.order_triples_in_query()  # order query to reduce the size of join in sql  # 2023/7/25
        exe_query = sparql_query.convert_to_sql(mapping_class)  # sparql to intermediate sql
        # exe_query = sparql_query.where_to_join_conversion(exe_query)  # convert where clause in SQL into Join  # 2023/7/27
        sparql2sql_timing.record_end()

        print(exe_query)  # for debug
        sql_execution_timing = TimingClass(input_file, 'sql_execution')
        # sql_timing.record_start()
        sql_results, headers = data_base.execute(exe_query)  # execute sql query
        sql_execution_timing.record_end()

        data_base.close()

        sql2sparql_timing = TimingClass(input_file, 'sql_to_sparql')
        # sql2sparql_timing.record_start()
        sparql_results = sparql_query.convert_to_rdf(uri, sql_results, headers)  # convert the sql results back to rdf
        sql2sparql_timing.record_end()

        Output.save_file(self.path.output_file_path, sparql_results, headers)  # save the results in a file
        print(len(sparql_results))  # debug info
        total_execution_timing.record_end()
        return sparql_results  # for pytests

    def execute_sql(self, exe_query):  # direct execution of sql  # for debug  # 2023/7/27
        data_base = DataBase(self.path, self.db_name, dbms=self.dbms, port=self.port)  # instance of DatabaseClass  # 2023/6/1

        sql_results, headers = data_base.execute(exe_query)  # execute sql query
        print(len(sql_results))
        data_base.close()
