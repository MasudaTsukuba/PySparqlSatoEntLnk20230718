import json
import re

with open('/media/masuda/HDS2-UT/PycharmProjects/PyForBackBench20230629/scenarios/StockExchange/ontop-files/gav-mapping.obda', 'r') as input_file:
    mode = None
    prefixes = {}
    json_list = []
    json_element = {}
    var_number = 10000
    gav_data = input_file.readlines()
    for line in gav_data:
        if line.find('PrefixDeclaration') >= 0:
            mode = 'PrefixDeclaration'
            continue
        elif line.find('MappingDeclaration') >= 0:
            mode = 'MappingDeclaration'
            continue
        else:
            if mode == 'PrefixDeclaration':
                input_line = line.replace('\n', '').replace(' ', '').replace('\t', '').replace('http:', 'http$').replace('https:', 'https$')
                if input_line:
                    input_split = input_line.split(':')
                    prefixes[input_split[0]] = input_split[1].replace('http$', 'http:').replace('https$', 'https:')
                pass
            if mode == 'MappingDeclaration':
                input_line = line.replace('\t', ' ').replace('\n', '').replace('  ', ' ')
                if input_line:
                    for prefix_key, prefix_value in prefixes.items():
                        input_line = input_line.replace(prefix_key+':', prefix_value)
                    if input_line.find('mappingId ') >= 0:
                        json_element = {}
                        json_element['mappingId'] = input_line.replace('mappingId ', '')
                    if input_line.find('target ') >= 0:
                        target_line = input_line.replace('target ', '')
                        target_split = target_line.split(' ')
                        subject_term = target_split[0]
                        predicate_term = target_split[1]
                        object_term = target_split[2]

                        json_term = {}
                        subject_replaced_name = 'VAR'+str(var_number)
                        if subject_term.find('{') >= 0:
                            matches_subject = re.findall(r'[{]var\d+[}]', subject_term)
                            subject_var_name = matches_subject[0].replace('{', '').replace('}', '')
                            json_term['type'] = 'Variable'
                            json_term['uri'] = 'plain'
                            json_term['content'] = ''
                            json_term['variable'] = subject_replaced_name
                            json_element['subject'] = json_term
                        else:
                            print('Invalid subject term: ', subject_term)

                        json_term = {}
                        predicate_var_name = 'VAR'+str(var_number+1)
                        json_term['type'] = 'NamedNode'
                        if predicate_term == 'a':
                            predicate_term = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
                        json_term['content'] = predicate_term
                        json_term['variable'] = predicate_var_name
                        json_element['predicate'] = json_term

                        json_term = {}
                        object_replaced_name = 'VAR'+str(var_number+2)
                        object_is_variable = False
                        if object_term.find('{') >= 0:
                            matches_subject = re.findall(r'[{]var\d+[}]', object_term)
                            object_var_name = matches_subject[0].replace('{', '').replace('}', '')
                            json_term['type'] = 'Variable'
                            json_term['uri'] = 'plain'
                            json_term['content'] = ''
                            object_is_variable = True
                        else:
                            json_term['type'] = 'NamedNode'
                            json_term['uri'] = '-'
                            json_term['content'] = object_term
                        json_term['variable'] = object_replaced_name
                        json_element['object'] = json_term

                        var_number += 100

                        pass
                    if input_line.find('source ') >= 0:
                        matches_subject = re.findall(r'(A\.\"c0\" as var\d+)|(\"c0\" as var\d+)', input_line)
                        sql = input_line.replace('source ', '')
                        matched_string = str(matches_subject[0][0]).replace(' as ', ') as ')
                        sql = sql.replace(str(matches_subject[0][0]),
                                          f"CONCAT('http://www.owl-ontologies.com/Ontology1207768242.owl#ns/', {matched_string}")\
                            .replace(subject_var_name, subject_replaced_name)

                        if object_is_variable:
                            matches_object = re.findall(r'([A-Z]\.\"c\d\" as var\d+)', sql)
                            matched_string = str(matches_object[0]).replace(' as ', ') as ')
                            sql = sql.replace(str(matches_object[0]),
                                              f"CONCAT('http://www.owl-ontologies.com/Ontology1207768242.owl#ns/', {matched_string}")\
                                .replace(object_var_name, object_replaced_name)
                        else:
                            sql = sql.replace(' FROM ', f", CONCAT('{object_term}') AS {object_replaced_name} FROM ")

                        sql = sql.replace('"', '\"')
                        json_element['SQL'] = sql
                        json_list.append(json_element)
                        pass

    with open('../../data/stock_exchange_20230705/mapping/mapping.json', 'w') as output_file:
        json.dump(json_list, output_file, indent=2)
