# SparqlQueryClass for handling sparql queries
# 2023/6/14, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import json
import re
# import sqlite3
# from UriClass import Uri


class SparqlQuery:
    def __init__(self, query_uri, uri):
        # ------ ユーザから得て, JSON形式に変換したSPARQLを取り込む --------
        # self.var_list = None  # list of variables
        self.filter_list = None  # list of filters
        # self.trans_uri_list = None  # not used? 2023/5/23
        # self.sql_query = None
        # self.exe_query = None
        self.uri = uri  # instance of Uri class
        # json_open = open(query_uri, 'r')
        # self.query_in_json = json.load(json_open)  # read query in json format
        # json_open.close()
        with open(query_uri, 'r') as json_open:
            self.query_in_json = json.load(json_open)  # read query in json format

        # def open_mapping():
        #     uri_mapping = './data_set2/uri/URI_mapping.json'
        #     json_open = open(uri_mapping, 'r')
        #     uri_mapping_dict = json.load(json_open)
        #     json_open.close()
        #     return uri_mapping_dict
        # self.uri_mapping_dict = open_mapping()

        # ------------------------------------------------------------
        self.variables_translation_list = {}  # dictionary for indicating the translation of variables to the corresponding variables in the mapping file
        # self.variables_uri_list = {}  # dictionary for indicating the correspondence of variables and their uri transformations

    def convert_to_sql(self, mapping_class):  # sparql to intermediate sql
        def create_var_list(query_dict):  # create a list of variables in sparql query
            # 出力する変数リストを作成
            var_list = []
            for var in query_dict['variables']:  # extract variables from json
                var_list.append(var['value'])  # append to a variable list
            return var_list
        var_list = create_var_list(self.query_in_json)  # create a list of variables in sparql query: ['s', 'name, 'cname']

        def create_sql_query(query_json, filter_list, uri):  # create a list of individual sql queries
            # SPARQLクエリの各トリプルパターンから候補のSQLクエリを検索
            sql_queries = []  # sqls to be returned
            # trans_uri_list = []  # return value
            # check = []
            # checked = []
            foo_count = 0
            for triple in query_json['where'][0]['triples']:  # process each triple in sparql query
                sql_subquery = []  # a list of individual sql queries
                q_predicate = triple['predicate']['value']  # 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
                q_type = triple['predicate']['termType']  # 'NamedNode'
                if q_type == 'NamedNode':  # in case the predicate in the query triple is not a variable
                    for mapping in mapping_class.mapping_dict:  # search mapping rules
                        predicate = mapping["predicate"]["content"]
                        if q_predicate == predicate:  # predicates matched
                            sql = mapping["SQL"]  # sql statement in the mapping file
                            # answer = uri.translate_sql(sql, triple, mapping, filter_list)
                            answer = uri.translate_sql(sql, triple, mapping)  # 2023/6/16
                            re_sql = answer[0]  # uri translated sql
                            if answer[1]:
                                for key, value in answer[1].items():
                                    self.variables_translation_list[key] = value
                                    # if ans[0] not in checked:
                                        # trans_uri_list.append(ans)
                                #         check.append(ans[0])
                            if re_sql != 'No':
                                sql_subquery.append(re_sql)
                    insert_sql = ''
                    if sql_subquery:  # matches are found
                        # for sub_q in sql_subquery:
                        #     insert_sql += sub_q + ' UNION '  # connect sqls with union
                        # insert_sql = re.sub(r' UNION $', '', insert_sql)  # remove the last 'UNION'
                        if len(sql_subquery) == 1:
                            if sql_subquery[0].find('FOO') < 0:
                                insert_sql = f'({sql_subquery[0]}) AS FOO{foo_count}'
                            else:
                                insert_sql = f'({sql_subquery[0]}) AS FOO{foo_count}'
                        else:
                            insert_sql = ' UNION '.join(sql_subquery)  # connect with UNION  # 2023/5/23
                            insert_sql = f'({insert_sql}) AS FOO{foo_count}'
                        foo_count += 1
                        insert_sql = insert_sql.replace(';', '') + ';'  # add a semicolon at the end
                    # checked = checked + check
                    sql_queries.append(insert_sql)  # append into a list
                elif q_type == 'Variable':  # in the case the predicate of the query triple is a variable
                    predicate_variable = triple['predicate']['value']
                    for mapping in mapping_class.mapping_dict:  # pick up applicable mapping rules
                        # predicate = mapping_class.mapping_dict[j]["predicate"]
                        sql = mapping["SQL"]
                        # query = triple
                        # mapping = mapping_class.mapping_dict[j]
                        # answer = uri.translate_sql(sql, triple, mapping, filter_list)  # create a uri translated sql and variables list
                        answer = uri.translate_sql(sql, triple, mapping)  # 2023/6/16  # create a uri translated sql and variables list
                        re_sql = answer[0]  # answer[0] contains the sql statement
                        if answer[1]:  # answer[1] contains a dict of uri transformation
                            for key, value in answer[1].items():
                                self.variables_translation_list[key] = value
                        # if answer[1]:  # answer[1] contains the list of variables
                        #     for ans in answer[1]:
                        #         if ans[0] not in checked:
                        #             trans_uri_list.append(ans)
                        #             check.append(ans[0])
                        if re_sql != 'No':
                            sql_subquery.append(re_sql)
                    insert_sql = ''
                    if sql_subquery:
                        # for sub_q in sql_subquery:
                        #     insert_sql += sub_q + ' UNION '
                        # insert_sql = re.sub(r' UNION $', '', insert_sql)
                        if len(sql_subquery) == 1:
                            if sql_subquery[0].find('FOO') < 0:
                                insert_sql = f'({sql_subquery[0]}) AS FOO{foo_count}'
                            else:
                                insert_sql = f'({sql_subquery[0]}) AS FOO{foo_count}'
                        else:
                            insert_sql = ' UNION '.join(sql_subquery)  # connect with UNION  # 2023/5/23
                            insert_sql = f'({insert_sql}) AS FOO{foo_count}'
                        foo_count += 1
                        insert_sql = insert_sql.replace(';', '') + ';'  # add a semicolon at the end while avoiding the duplicate
                    # checked = checked + check  # concatenate the list
                    sql_queries.append(insert_sql)  # add to the sql list
            # trans_uri_list = list(set(tuple(i) for i in trans_uri_list))
            # trans_uri_list = [list(i) for i in trans_uri_list]
            # return sql_query, trans_uri_list
            return sql_queries
        # self.sql_query, self.trans_uri_list = create_sql_query(self.query_in_json, self.filter_list, self.uri)  # create a list of individual sql queries
        sql_queries = create_sql_query(self.query_in_json, self.filter_list, self.uri)  # create a list of individual sql queries

        def create_filter_list(query_json, uri):  # process filters in sparql query
            def uri_transform(var_list_in, sql_filter_in, uri_in):
                sql_filter_out = sql_filter_in
                pattern = r'"(https?://.*)"'
                matches = re.findall(pattern, sql_filter_in)
                if matches:
                    for match in matches:
                        replacement = match
                        for var in var_list_in:
                            try:
                                # replacement = self.inv_dict_all[match]
                                uri_table = self.variables_translation_list[var]  # choose the uri transformation table
                                temp_inv_dict = uri_in.inv_dict[uri_table]  # use individual uri table  # 2023/6/14
                                try:
                                    replacement = temp_inv_dict[match]
                                except KeyError:
                                    pass
                                sql_filter_out = re.sub(match, replacement, sql_filter_in)
                            except KeyError:
                                pass
                return sql_filter_out

            def analyze_filter(filter_expression_in, var_list_in, uri_in):  # parse filter clause recursively
                try:
                    expression_type = filter_expression_in['type']  # check the type of the filter element
                    if expression_type == 'operation':  # expression type is operation, then it has an attribute 'operator'
                        filter_operator = filter_expression_in['operator']  # &&, ||, !, =, >, <, etc
                        filter_args = filter_expression_in['args']  # args of operation
                        var_list1, filter_element1 = analyze_filter(filter_args[0], var_list_in, self.uri)  # analyze the first arg
                        var_list_in = var_list_in.union(var_list1)
                        if filter_operator == '!':  # in case of logical not operator
                            return var_list_in, f'NOT {filter_element1}'  # analyze only the first arg
                        else:  # filter_operator == '&&' or filter_operator == '||':
                            var_list2, filter_element2 = analyze_filter(filter_args[1], var_list_in, self.uri)  # analyze the second arg
                            var_list_in = var_list_in.union(var_list2)
                            if filter_operator == '&&':  # logical and
                                sql_filter = f'({filter_element1} AND {filter_element2})'  # convert to sql format
                            elif filter_operator == '||':  # logical or
                                sql_filter = f'({filter_element1} OR {filter_element2})'  # convert to sql format
                            else:  # =, >, <, etc.
                                sql_filter = f'({filter_element1} {filter_operator} {filter_element2})'

                                match_float = re.match(r'[-+]?\d+(\.\d+)', filter_element1)  # cast string column to float or integer  # 2023/7/20
                                match_integer = re.match(r'[-+]?\d+', filter_element1)
                                if match_float:
                                    sql_filter = f'({filter_element1} {filter_operator} CAST({filter_element2} AS FLOAT))'
                                elif match_integer:
                                    sql_filter = f'({filter_element1} {filter_operator} CAST({filter_element2} AS INTEGER))'
                                match_float = re.match(r'[-+]?\d+(\.\d+)', filter_element2)
                                match_integer = re.match(r'[-+]?\d+', filter_element2)
                                if match_float:
                                    sql_filter = f'(CAST({filter_element1} AS FLOAT) {filter_operator} {filter_element2})'
                                elif match_integer:
                                    sql_filter = f'(CAST({filter_element1} AS INTEGER) {filter_operator} {filter_element2})'

                            sql_filter = uri_transform(var_list_in, sql_filter, uri_in)
                            return var_list_in, sql_filter
                except KeyError:  # filter_expression does not have an attribute 'type'
                    try:
                        expression_term_type = filter_expression_in['termType']  # check the term type: Variable or NamedNode
                        if expression_term_type == 'Variable':  # in case of Variable
                            var = filter_expression_in['value']
                            var_list_in.add(var)  # add to a set of variables
                            return {var}, var  # returned filter expression is the variable itself
                        elif expression_term_type == 'NamedNode':  # in case of NamedNode
                            val = filter_expression_in['value']
                            val = f'"{val}"'  # enclose the value with double quotes
                            return set(), val
                        elif expression_term_type == 'Literal':  # in case of Literal
                            val = filter_expression_in['value']
                            match = re.match(r'[-+]?\d+(\.\d+)?', val)
                            if match:  # number
                                pass
                            else:  # string
                                val = f"'{val}'"  # enclose the value with single quotes  # 2023/7/14
                            return set(), val
                    except KeyError:  # something unexpected happened
                        pass
                pass
                return var_list_in, ''  # this is also an exceptional return

            # FILTERの条件リストを作成
            filter_list = []  # element is a list of a set of variables and an sql formatted filter clause
            var_list = set()  # a set of variables contained in a filter clause
            for element in query_json['where']:
                if element['type'] == 'filter':
                    filter_expression = element['expression']
                    var_list_out, filter_element = analyze_filter(filter_expression, var_list, uri)
                    filter_list.append([var_list_out, filter_element])
                        # [filter_args[0]['value'],
                        #  filter_args[0]['value'] + ' '  # cname
                        #  + element['expression']['operator'] + ' "'  # =
                        #  + filter_args[1]['value'] + '"'])  # 'United Kingdom'
            return filter_list
        self.filter_list = create_filter_list(self.query_in_json, self.uri)  # create a list of filters: []

        def create_final_sql(var_list_in, filter_list_in, sql_queries_in):  # final build of sql query
            select_var = ''  # comma separated list string of variables
            # for var in var_list:  # list of variables in sparql query
            #     select_var += var + ', '  # change them to a comma-separated string
            # select_var = re.sub(', $', '', select_var)  # remove the comma at the end
            select_var = ', '.join(var_list_in)  # var_list to a string# 2023/5/23
            exe_query_out = 'SELECT ' + select_var + ' FROM '  # starting sql query build
            try:  # in the case SELECT has the option distinct
                if self.query_in_json['distinct']:
                    exe_query_out = 'SELECT DISTINCT ' + select_var + ' FROM '
            except KeyError:  # no DISTINCT
                pass
            filters = ''
            filter_sqls = [element[1] for element in filter_list_in]
            if filter_list_in:
                filters = ' AND '.join(filter_sqls)
            # sql_queries_local = []
            # for sql in sql_queries_in:
            #     if filters == '':
            #         sql_queries_local.append(sql)
            #     elif sql.find('WHERE') >= 0:
            #         sql_queries_local.append(sql + ' AND ' + filters)
            #     else:
            #         sql_queries_local.append(sql + ' WHERE ' + filters)
            if len(sql_queries_in) == 1:
                exe_query_out_append = sql_queries_in[0]
            else:
                # exe_query_out += '(' + ') NATURAL JOIN ('.join(sql_queries_in) + ')'  # connect with NATURAL JOIN
                exe_query_out_append = '' + ' NATURAL JOIN '.join(sql_queries_in) + ''  # connect with NATURAL JOIN
                exe_query_out_append = f'({exe_query_out_append})'
            exe_query_out += exe_query_out_append
            if filters:
                exe_query_out += ' WHERE ' + filters
            exe_query_out = exe_query_out.replace(';', '') + ';'  # end up with a semicolon while suppressing a duplicate
            # print(exe_query)  # for debug
            return exe_query_out  # return the built sql query

        exe_query = create_final_sql(var_list, self.filter_list, sql_queries)  # final build of sql query
        return exe_query  # return the built sql query

    def convert_to_rdf(self, uri, results, headers):  # convert the sql results into sparql results using uri_dict_all table
        # --------- SQLクエリ結果をSPARQLクエリ結果に合わせるため、必要に応じて文字列->URIに変換する ----------------------------------
        # def create_trans_uri_list(trans_uri_list):
        #     tmp = []
        #     for i in trans_uri_list:
        #         if i[1] != 'plain':
        #             tmp.append(i)
        #     return tmp
        # trans_uri_list = create_trans_uri_list(self.trans_uri_list)
        #
        # def prepare_sql_tquery(uri):
        #     def g(uri_mapping, b_trans, a_trans):
        #         sql = str(uri_mapping['SQL'])  # "SQL":"SELECT ID AS A0, URI_Build AS A1 FROM PREFIX_Build"
        #         sql = sql.replace(uri_mapping['x'], b_trans)  # "x":"A0"
        #         sql = sql.replace(uri_mapping['y'], a_trans)  # "y":"A1"
        #         return sql
        #
        #     sql_tquery = []
        #     # print(transURI_list)
        #     r_list = []
        #     for s in self.var_list:
        #         r_list.append(s)
        #     # print(r_list)  # ['s', 'name', 'cname']
        #     for y in range(len(r_list)):
        #         or_query = []
        #         insert_sql = ''
        #         i0 = ''
        #         sql = ''
        #         for j in trans_uri_list:  # [['s', 'PREFIX_museum'],...]
        #             if j[0] == r_list[y]:  # name of a variable
        #                 for k in uri:
        #                     if k['name'] == j[1]:  # mapping table/function
        #                         i0 = r_list[y] + 'trans'  # s -> strans
        #                         sql = g(k, r_list[y], i0)  # query for search PREFIX*
        #                 or_query.append(sql)
        #         if len(or_query) != 0:
        #             for or_q in or_query:
        #                 insert_sql += or_q + ' UNION '  # combine with 'UNION
        #             insert_sql = re.sub('UNION $', '', insert_sql)  # remove the last 'UNION'
        #             insert_sql = insert_sql.replace(';', '') + ';'  # add semicolon at the end while suppressing the duplicate
        #
        #         if insert_sql != '':
        #             sql_tquery.append(insert_sql)  # list of sql's
        #             r_list[y] = i0  # replace the list of variables
        #     return sql_tquery, r_list
        # sql_tquery, r_list = prepare_sql_tquery(self.uri)
        #
        # def uri_db(uri_database, var_list):
        #     c = sqlite3.connect(uri_database)
        #     c.execute('DROP TABLE Result;')  # ####################2023/3/20
        #     select_var = ''
        #     for i in range(len(var_list)):
        #         if i != len(var_list) - 1:
        #             select_var = select_var + var_list[i] + ', '
        #         else:
        #             select_var = select_var + var_list[i]
        #     c.execute('CREATE TABLE Result(' + select_var + ')')  # empty table
        #     v = ''
        #     # for b in range(len(var_list) - 1):
        #     for b in range(len(var_list)):
        #         v = v + '?,'
        #         # if b == len(var_list) - 2:
        #         # if b == len(var_list) - 1:
        #         #     v = v + '?'
        #     v = re.sub(',$', '', v)
        #     c.executemany('INSERT INTO Result (' + select_var + ') values (' + v + ')', results)
        #     # save the results of SQL query into a RD table
        #     # for result in results:
        #     #     v = ''
        #     #     for element in result:
        #     #         v += element + ', '
        #     #     v = re.sub(', $', '', v)
        #     #     c.execute('INSERT INTO Result (' + select_var + ') values (' + v + ')')
        #     cur = c.cursor()
        #     return cur
        # cu = uri_db(uri_database, self.var_list)
        #
        # # test_query = 'SELECT * FROM Result;'  # debug 20230323
        # # test_results = cursor.execute(test_query).fetchall()  # debug 20230323
        #
        # def build_query(cursor, r_list, sql_tquery):
        #     # by searching ID with ID->uri conversion table, convert ID to uri
        #     select_var2 = ''
        #     for r_l, var in zip(r_list, self.var_list):
        #         if r_l:
        #             select_var2 += r_l + ', '
        #         else:
        #             select_var2 += var + ', '  # 2023/5/18
        #     select_var2 = re.sub(', $', '', select_var2)
        #
        #     # exe_query = 'SELECT ' + select_var2 + ' FROM (Result) '
        #     exe_query = 'SELECT DISTINCT ' + select_var2 + ' FROM (Result) '  # 20230323
        #     # match 's' against Results and at the same time 's' and uri against PREFIX***
        #     for sql_tq in sql_tquery:
        #         if sql_tq != ' ;':  # 2023/5/18
        #             # exe_query = exe_query + ' NATURAL JOIN (' + SQL_tquery[i] + ')'
        #             exe_query = exe_query + ' NATURAL LEFT JOIN (' + sql_tq + ')'  # 20230323
        #     exe_query = exe_query.replace(';', '') + ';'
        #     print(exe_query)
        #     sql_results = cursor.execute(exe_query).fetchall()
        #     return sql_results
        # sparql_results = build_query(cu, r_list, sql_tquery)
        #
        # sparql_results = [list(pp) for pp in sparql_results]  # convert to a list
        sparql_results = []
        for result in results:
            row = []
            for element, header in zip(result, headers):
                converted_element = str(element)
                try:
                    # converted_element = uri.uri_dict_all[element]  # use unified table
                    uri_dict = self.variables_translation_list[header]  # use individual tables
                    try:
                        converted_element = uri.uri_dict[uri_dict][element]
                    except KeyError:
                        pass
                except KeyError:
                    pass
                row.append(converted_element)
            sparql_results.append(row)
        return sparql_results
