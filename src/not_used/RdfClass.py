# import json
# import re
# import sqlite3
# # import csv
# # import rewriter
#
# URI_directory = '/data_set2/uri/'
#
#
# class Rdf:
#     def __init__(self):
#         pass
#
#     def convert_to_rdf(self, sparql_query, uri_database, results):
#         # --------- SQLクエリ結果をSPARQLクエリ結果に合わせるため、必要に応じて文字列->URIに変換する ----------------------------------
#         def create_trans_uri_list(sparql_query):
#             tmp = []
#             for i in sparql_query.trans_uri_list:
#                 if i[1] != 'plain':
#                     tmp.append(i)
#             return tmp
#         trans_uri_list = create_trans_uri_list(sparql_query)
#
#         def open_mapping():
#             uri_mapping = './data_set2/uri/URI_mapping.json'
#             json_open = open(uri_mapping, 'r')
#             uri_mapping_dict = json.load(json_open)
#             json_open.close()
#             return uri_mapping_dict
#         uri_mapping_dict = open_mapping()
#
#         def prepare_sql_tquery(sparql_query):
#             sql_tquery = []
#             # print(transURI_list)
#             r_list = []
#             for s in sparql_query.var_list:
#                 r_list.append(s)
#             # print(r_list)
#             for y in range(len(r_list)):
#                 or_query = []
#                 insert_sql = ''
#                 i0 = ''
#                 sql = ''
#                 for j in trans_uri_list:
#                     if j[0] == r_list[y]:
#                         for k in uri_mapping_dict:
#                             if k['name'] == j[1]:
#                                 i0 = r_list[y] + 'trans'
#                                 sql = self.g(k, r_list[y], i0)
#                         or_query.append(sql)
#                 if len(or_query) != 0:
#                     for or_q in or_query:
#                         insert_sql += or_q + ' UNION '
#                     insert_sql = re.sub('UNION $', '', insert_sql)
#                     insert_sql = insert_sql.replace(';', '') + ';'
#
#                 if insert_sql != '':
#                     sql_tquery.append(insert_sql)
#                     r_list[y] = i0
#             return sql_tquery, r_list
#         sql_tquery, r_list = prepare_sql_tquery(sparql_query)
#
#         def uri_db(uri_database, sparql_query):
#             c = sqlite3.connect(uri_database)
#             c.execute('DROP TABLE Result;')  # ####################2023/3/20
#             select_var = ''
#             for i in range(len(sparql_query.var_list)):
#                 if i != len(sparql_query.var_list) - 1:
#                     select_var = select_var + sparql_query.var_list[i] + ', '
#                 else:
#                     select_var = select_var + sparql_query.var_list[i]
#             c.execute('CREATE TABLE Result(' + select_var + ')')
#             v = ''
#             for b in range(len(sparql_query.var_list) - 1):
#                 v = v + '?,'
#                 if b == len(sparql_query.var_list) - 2:
#                     v = v + '?'
#             c.executemany('INSERT INTO Result (' + select_var + ') values (' + v + ')', results)
#             cur = c.cursor()
#             return cur
#         cu = uri_db(uri_database, sparql_query)
#
#         # test_query = 'SELECT * FROM Result;'  # debug 20230323
#         # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
#
#         def build_query(cursor, r_list, sql_tquery):
#             select_var2 = ''
#             for r_l in r_list:
#                 select_var2 += r_l + ', '
#             select_var2 = re.sub(', $', '', select_var2)
#
#             # exe_query = 'SELECT ' + select_var2 + ' FROM (Result) '
#             exe_query = 'SELECT DISTINCT ' + select_var2 + ' FROM (Result) '  # 20230323
#             for sql_tq in sql_tquery:
#                 # exe_query = exe_query + ' NATURAL JOIN (' + SQL_tquery[i] + ')'
#                 exe_query = exe_query + ' NATURAL LEFT JOIN (' + sql_tq + ')'  # 20230323
#             exe_query = exe_query.replace(';', '') + ';'
#             print(exe_query)
#             sql_results = cursor.execute(exe_query).fetchall()
#             return sql_results
#         results2 = build_query(cu, r_list, sql_tquery)
#
#         # test_query = 'SELECT s, name, cname FROM Result;'
#         # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
#         # test_query = 'SELECT * FROM PREFIX_hotel WHERE ID = "15923583h";'
#         # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
#         # test_query = 'SELECT s, strans, name, cname FROM (Result)  NATURAL LEFT JOIN (SELECT ID AS s, URI_hotel AS strans FROM PREFIX_hotel);'
#         # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
#         # test_query = 'SELECT DISTINCT s, strans, name, cname FROM (Result)  NATURAL LEFT JOIN (SELECT ID AS s, URI_hotel AS strans FROM PREFIX_hotel);'
#         # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
#         results2 = [list(pp) for pp in results2]
#         return results2
#
#     # def f(self, sql: str, sparql, mapping, filter_list):
#     #     # subject
#     #
#     #     # print(triple)
#     #     # print(mapping)
#     #
#     #     trans_URI = []
#     #     if (sparql['subject']['termType'] == 'Variable'):
#     #         value = sparql['subject']['value']
#     #         sql = sql.replace(mapping['subject'], value)
#     #         trans_URI.append([value, mapping['subject_uri']])
#     #
#     #     elif (sparql['subject']['termType'] == 'NamedNode'):
#     #         value = sparql['subject']['value']
#     #         uri_function = mapping['subject_uri']
#     #         with open(URI_directory + uri_function + '.csv') as g:
#     #             reader = csv.reader(g)
#     #             for row in reader:
#     #                 if (value == row[1]):
#     #                     sql_value = row[0]
#     #                     break
#     #             sql = rewriter.rewrite_where_sql(sql, sql_value, mapping['subject'])
#     #
#     #     # object
#     #     if (sparql['object']['termType'] == 'Variable'):
#     #         value = sparql['object']['value']
#     #         sql = sql.replace(mapping['object'], value)
#     #         trans_URI.append([value, mapping['object_uri']])
#     #
#     #         for filter in filter_list:
#     #             if (filter[0] == value):
#     #                 sql = rewriter.rewrite_where_sql_filter(sql, filter[1])
#     #
#     #
#     #     elif (sparql['object']['termType'] == 'NamedNode'):
#     #         value = sparql['object']['value']
#     #         if (mapping['object_uri'] == '-'):
#     #             if (value != mapping['object']):
#     #                 return ['No', []]
#     #
#     #         else:
#     #             value = sparql['object']['value']
#     #             uri_function = mapping['object_uri']
#     #             with open(URI_directory + uri_function + '.csv') as g:
#     #                 reader = csv.reader(g)
#     #                 for row in reader:
#     #                     if (value == row[1]):
#     #                         sql_value = '"' + row[0] + '"'
#     #                         break
#     #             sql = rewriter.rewrite_where_sql(sql, sql_value, mapping['object'])
#     #             # sql = sql.replace(mapping['object'], value)
#     #
#     #     else:  # termTypeが'Literalのとき'
#     #         value = sparql['object']['value']
#     #         uri_function = mapping['object_uri']
#     #         if uri_function == 'plain':
#     #             sql = rewriter.rewrite_where_sql(sql, value, mapping['object'])
#     #             sql = sql.replace(mapping['object'], value)
#     #
#     #     return [sql, trans_URI]
#
#     @staticmethod
#     def g(uri_mapping, b_trans, a_trans):
#         sql = str(uri_mapping['SQL'])
#         sql = sql.replace(uri_mapping['x'], b_trans)
#         sql = sql.replace(uri_mapping['y'], a_trans)
#         return sql
