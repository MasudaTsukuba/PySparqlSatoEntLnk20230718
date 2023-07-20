# UriClass for handling uri transformation
# 2023/6/14, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import os
import pandas as pd
import re
import sqlite3
import spacy
import csv
# import json
# import csv
# from spacy.pipeline import EntityLinker
# from src.DatabaseClass import DataBase
# from src.PathClass import PathClass


class Uri:
    def __init__(self, path):
        self.path = path
        self.uri_path = self.path.dataset_path + '/uri/'  # ./data_set2/uri
        self.uri_dict = {}  # str->uri dictionary
        self.inv_dict = {}  # uri->str dictionary
        # self.uri_dict_all = {}
        # self.inv_dict_all = {}
        # for file in os.listdir(self.uri_path):  # read PREFIX*.csv
        #     if file.endswith(".csv"):
        #         df = pd.read_csv(self.uri_path + file, header=None)
        #         key = file.replace('.csv', '')  # key = PREFIX_Build, etc.
        #         self.uri_dict[key] = dict(zip(df[0], df[1]))  # str->uri dictionary
        #         self.inv_dict[key] = dict(zip(df[1], df[0]))  # uri->str dictionary
        #         self.uri_dict_all.update(zip(df[0], df[1]))  # all the files in one dictionary
        #         self.inv_dict_all.update(zip(df[1], df[0]))

        # def open_mapping(): not used. replaced by uri_dict, etc.
        #     uri_mapping = './data_set2/uri/URI_mapping.json'
        #     json_open = open(uri_mapping, 'r')
        #     uri_mapping_dict = json.load(json_open)
        #     json_open.close()
        #     return uri_mapping_dict
        # self.uri_mapping_dict = open_mapping()
        # self.entity_linking_file = None
        self.entity_linking_file = self.uri_path+'entity_linking.db'
        pass

    # def translate_sql(self, sql: str, triple, mapping, filter_list):  # uri translation: return [sql, trans_uri]
    def translate_sql(self, sql: str, triple, mapping):  # 2023/6/16  # uri translation: return [sql, trans_uri]

        def rewrite_where_sql(sql: str, where_value, var):
            if 'WHERE' in sql:  # if WHERE key word is already in the sql statement
                index = sql.find(';')  # find the last
                re_sql = sql[:index] + ' AND ' + var + ' = "' + where_value + '";'  # append the WHERE clause at the end
            else:  # first time 'WHERE' is inserted
                index = sql.find(';')
                re_sql = sql[:index] + ' WHERE ' + var + ' = "' + where_value + '";'  # first WHERE
            return re_sql

        def rewrite_where_sql_filter(sql: str, sql_filter, uri_table):
            pattern = r'"(https?://.*)"'
            matches = re.findall(pattern, sql_filter)
            if matches:
                for match in matches:
                    replacement = match
                    try:
                        # replacement = self.inv_dict_all[match]
                        temp_inv_dict = self.inv_dict[uri_table]  # use individual uri table  # 2023/6/14
                        try:
                            replacement = temp_inv_dict[match]
                        except KeyError:
                            pass
                        sql_filter = re.sub(match, replacement, sql_filter)
                    except KeyError:
                        pass
            if 'WHERE' in sql:  # The WHERE key word is already in the sql statement
                index = sql.find(';')
                re_sql = sql[:index] + ' AND ' + sql_filter + ';'  # join with AND
            else:
                index = sql.find(';')
                re_sql = sql[:index] + ' WHERE ' + sql_filter + ';'  # start of new WHERE term
            return re_sql

        def create_trans_uri(triple, sql, key):
            value = triple[key]['value']  # get the name of the variable
            sql_replace = sql.replace(mapping[key]['variable'], value)  # replace the variable in sql statement
            try:
                # trans_uri.append([value, mapping[key]['uri']])
                trans_uri[value] = mapping[key]['uri']  # 2023/6/14
            except KeyError:
                pass
            return trans_uri, sql_replace, value

        trans_uri = {}  # translation uri; will be returned
        # subject
        if triple['subject']['termType'] == 'Variable':  # in the case the subject is a variable
            trans_uri, sql, value = create_trans_uri(triple, sql, 'subject')
            # for filter_item in filter_list:
            #     if filter_item[0] == value:
            #         uri_table = ''
            #         try:
            #             uri_table = trans_uri[value]
            #         except KeyError:
            #             pass
            #         sql = rewrite_where_sql_filter(sql, filter_item[1], uri_table)

        elif triple['subject']['termType'] == 'NamedNode':  # in the case the subject is a constant
            value = triple['subject']['value']
            if mapping['subject']['uri'] == '-':
                if value != mapping['subject']['content']:
                    return ['No', []]
            elif mapping['subject']['uri'] == 'plain':  # 2023/5/8
                sql_value = value  # 2023/5/8
                sql = rewrite_where_sql(sql, sql_value, mapping['subject']['variable'])  # 2023/5/8
            else:
                uri_function = mapping['subject']['uri']
                # with open(self.uri_directory + uri_function + '.csv') as g:
                #     reader = csv.reader(g)
                #     for row in reader:
                #         if value == row[1]:
                #             sql_value = row[0]
                #             break
                # sql_value = self.inv_dict[uri_function][value]
                # sql_value = self.inv_dict[uri_function][value]
                sql_value = value
                # try:
                #     sql_value = self.inv_dict_all[value]
                # except KeyError:
                #     pass
                try:  # 2023/6/14  # use individual PREFIX files
                    inv_dict = self.inv_dict[uri_function]
                    try:
                        sql_value = inv_dict[value]
                    except KeyError:
                        pass
                except KeyError:
                    pass
                sql = rewrite_where_sql(sql, sql_value, mapping['subject']['variable'])

        elif triple['subject']['termType'] == 'BlankNode':
            trans_uri, sql, value = create_trans_uri(triple, sql, 'subject')
            pass

        # predicate  # 2023/5/23
        if triple['predicate']['termType'] == 'Variable':
            trans_uri, sql, value = create_trans_uri(triple, sql, 'predicate')

        # object
        if triple['object']['termType'] == 'Variable':
            # value = triple['object']['value']
            # sql = sql.replace(mapping['object'], value)
            # trans_uri.append([value, mapping['object_uri']])
            trans_uri, sql, value = create_trans_uri(triple, sql, 'object')

            # for filter_item in filter_list:
            #     if filter_item[0] == value:
            #         uri_table = ''
            #         try:
            #             uri_table = trans_uri[value]
            #         except KeyError:
            #             pass
            #         sql = rewrite_where_sql_filter(sql, filter_item[1], uri_table)

        elif triple['object']['termType'] == 'NamedNode':
            value = triple['object']['value']
            if mapping['object']['uri'] == '-':
                if value != mapping['object']['content']:
                    return ['No', []]
            elif mapping['object']['uri'] == 'plain':  # 2023/5/8
                sql_value = value  # 2023/5/8
                sql = rewrite_where_sql(sql, sql_value, mapping['object']['variable'])  # 2023/5/8
            else:
                value = triple['object']['value']
                uri_function = mapping['object']['uri']
                # with open(self.uri_directory + uri_function + '.csv') as g:
                #     reader = csv.reader(g)
                #     for row in reader:
                #         if value == row[1]:
                #             sql_value = '"' + row[0] + '"'
                #             break
                # try:  # 2023/5/8
                #     # sql_value = self.inv_dict[uri_function][value]
                #     sql_value = self.inv_dict_all[value]  # 2023/6/5
                #     sql = rewrite_where_sql(sql, sql_value, mapping['object'])
                #     # sql = sql.replace(mapping['object'], value)
                # except KeyError:  # 2023/5/8
                #     return ['No', []]  # 2023/5/8
                try:  # 2023/6/14  # use individual PREFIX files
                    inv_dict = self.inv_dict[uri_function]
                    try:
                        sql_value = inv_dict[value]
                        sql = rewrite_where_sql(sql, sql_value, mapping['object'])
                    except KeyError:
                        return ['No', []]
                except KeyError:
                    return ['No', []]

        elif triple['object']['termType'] == 'BlankNode':
            trans_uri, sql, value = create_trans_uri(triple, sql, 'object')
            pass

        else:  # termTypeが'Literalのとき'
            value = triple['object']['value']
            uri_function = mapping['object']['uri']
            if uri_function == 'plain':
                sql = rewrite_where_sql(sql, value, mapping['object'])
                sql = sql.replace(mapping['object'], value)

        return [sql, trans_uri]

    # create tables in entity_linking.db database
    def create_entity_linking_db(self, tables, sqls):
        conn = sqlite3.connect(self.entity_linking_file)
        cursor = conn.cursor()

        # tables = ['country', 'hotel', 'building', 'museum', 'heritage']
        # sqls = [
        #     'CREATE TABLE hotel (id VARCHAR(255) PRIMARY KEY, uri VARCHAR(255), status VARCHAR(255));',
        #     'CREATE TABLE building (id VARCHAR(255) PRIMARY KEY, uri VARCHAR(255), status VARCHAR(255));',
        #     'CREATE TABLE museum (id VARCHAR(255) PRIMARY KEY, uri VARCHAR(255), status VARCHAR(255));',
        #     'CREATE TABLE heritage (id VARCHAR(255) PRIMARY KEY, uri VARCHAR(255), status VARCHAR(255));',
        #     'CREATE TABLE country (id VARCHAR(255) PRIMARY KEY, uri VARCHAR(255), status VARCHAR(255));'
        # ]

        for table in tables:
            sql = f'DROP TABLE {table};'
            try:
                cursor.execute(sql)
                print('DROP TABLE SUCCEEDED: ' + sql)
                pass
            except:
                print('DROP TABLE FAILED: ' + sql)
                pass

        for sql in sqls:
            try:
                cursor.execute(sql)
                print('CREATE TABLE SUCCEEDED: ' + sql)
                pass
            except:
                print('CREATE TABLE FAILED: ' + sql)
                pass

        cursor.close()
        conn.commit()
        conn.close()
        pass

    # for test entity_linking.db
    def test_entity_linking(self, print_results=True):
        conn = sqlite3.connect(self.entity_linking_file)
        cursor = conn.cursor()
        # sql = 'INSERT INTO hotel (id, uri, status) VALUES ("aaa", "bbb", "ccc");'
        # cursor.execute(sql)

        # sql = 'SELECT * FROM building;'
        sql = 'SELECT * FROM country;'
        return_list = cursor.execute(sql).fetchall()
        headers = [col[0] for col in cursor.description]
        results = [list(i) for i in return_list]
        if print_results:
            print(results)
        cursor.close()
        conn.close()

    # build entity linking
    def build_entity_linking(self, database, tables, id_label=True, replace=True):
        conn = sqlite3.connect(self.entity_linking_file)
        cursor = conn.cursor()

        nlp = spacy.load('en_core_web_md')
        # nlp = spacy.load('en_core_web_lg')
        nlp.add_pipe('entityLinker', last=True)

        def spacy_entity_linking(text):
            if text == 'United States of America':  # debug
                pass
            entity = nlp(text)
            result_uri = ''
            result_label = ''
            result_description = ''
            result_status = 'NoFound'
            xxx = entity._.linkedEntities
            my_ents = entity.ents
            found = False
            try:
                yyy = xxx[0]
                result_uri = yyy.get_url()
                result_label = yyy.label
                result_description = yyy.description
                found = True
            except TypeError:
                pass
            except IndexError:
                pass
            mark = '  '
            try:
                if len(xxx) == 1 and result_label == text and found:
                    result_status = 'Succeeded'
                    pass
                else:
                    result_uri = ''
            except IndexError:
                result_uri = ''
                pass
            pass
            return result_status, result_uri, result_label, result_description, xxx

        # path = PathClass('data_set2')
        # database = DataBase(path, 'landmark.db')
        # tables = ['country', 'hotel', 'building', 'museum', 'heritage']
        # tables = ['hotel']  # debug
        conn.execute("BEGIN")
        for table in tables:
            print(table)  # debug
            sql = f'SELECT * FROM {table};'
            results, headers = database.execute(sql)
            for result in results:
                table_id = result[0]
                name = result[1]
                status, uri, label, description, xxx = spacy_entity_linking(name)
                if status == 'Succeeded':
                    if replace:
                        uri = uri.replace('https://www.wikidata.org/wiki/', 'http://www.wikidata.org/entity/')
                else:
                    uri = f'http://example.com/id/{table_id}'
                sql = f'INSERT INTO {table} (id, name, uri, status) VALUES ("{table_id}", "{name}", "{uri}", "{status}");'
                if status == 'Succeeded' and table_id.replace('h', '') != uri.split('/')[-1].replace('Q', ''):
                    # print(sql)  # debug
                    pass
                cursor.execute(sql)
                pass
            conn.commit()
            query = f'SELECT * FROM {table} WHERE status = "Succeeded" ;'
            results = cursor.execute(query).fetchall()
            for row in results:
                if row[0].replace('h', '') != row[1].split('/')[-1]:
                    pass  # debug
            with open(f'{self.uri_path}EntityLinking_{table}.csv', 'w') as f:  # debug
                writer = csv.writer(f)
                for result in results:
                    row = [result[0], result[2]]  # table_id, uri
                    if not id_label:
                        row = [result[1], result[2]]  # name, uri
                    writer.writerow(row)
            pass
        cursor.close()
        conn.close()
        pass

    def read_entity_linking(self, tables):
        conn = sqlite3.connect(self.entity_linking_file)
        cursor = conn.cursor()

        # tables = ['country', 'hotel', 'building', 'museum', 'heritage']
        for table in tables:  # read from tables in entity_linking.db
            sql = f'SELECT id, uri, status from {table};'
            results = cursor.execute(sql).fetchall()
            for row in results:
                if True:  # row[2] == 'Succeeded':
                    record_id = row[0]
                    record_uri = row[1]
                    # self.uri_dict_all[record_id] = record_uri  # all the files in one dictionary
                    # self.inv_dict_all[record_uri] = record_id
                    # xxx = self.uri_dict_all['Q30']  # debug
        cursor.close()
        conn.close()
        pass

    def read_entity_linking_from_csv(self):  # in case the entity linking info and user supplied conversion info is stored in csv files
        for file in os.listdir(self.uri_path):  # read PREFIX*.csv
            if file.endswith(".csv"):
                df = pd.read_csv(self.uri_path + file, header=None)
                key = file.replace('.csv', '')  # key = PREFIX_Build, etc.
                uri_dict_element = {}
                inv_dict_element = {}
                for value0, value1 in zip(df[0], df[1]):
                    uri_dict_element[str(value0)] = str(value1)
                    inv_dict_element[str(value1)] = str(value0)
                self.uri_dict[key] = uri_dict_element  # 2023/6/14  # dict(zip(df[0], df[1]))  # str->uri dictionary
                self.inv_dict[key] = inv_dict_element  # 2023/6/14  # dict(zip(df[1], df[0]))  # uri->str dictionary

                # self.uri_dict_all.update(zip(df[0], df[1]))  # all the files in one dictionary
                # self.inv_dict_all.update(zip(df[1], df[0]))

                # for value0, value1 in zip(df[0], df[1]):
                #     self.uri_dict_all[str(value0)] = str(value1)
                #     self.inv_dict_all[str(value1)] = str(value0)
