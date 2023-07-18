# class for handling paths
# 2023/6/1, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import os


class PathClass:
    def __init__(self, dataset_name):
        # root of working path
        self.working_path = os.getcwd()
        if self.working_path.find('data') >= 0 or self.working_path.find('npd') >= 0 or self.working_path.find('stock') >= 0:
            self.working_path = os.path.dirname(self.working_path)
        if self.working_path.endswith('src'):
            self.working_path = os.path.dirname(self.working_path)

        # path storing queries
        self.dataset_path = f'{self.working_path}/data/{dataset_name}/'  # 2023/6/15
        self.common_query_path = self.dataset_path + '/query/'

        # name of input query file
        self.input_query_file = ''  # 2023/6/14  # input_query_file

        # path to output file
        self.output_file_path = ''  # 2023/6/14

        # path to mapping file
        self.mapping_file_path = ''  # 2023/6/14  # self.dataset_path + '/mapping/mapping_revised.json'
        pass

    def set_input_query(self, input_query_file):
        self.input_query_file = input_query_file
        # path to output file
        output_file = self.input_query_file.replace('.txt', '.csv')
        self.output_file_path = f'{self.dataset_path}/output/{output_file}'

    def set_mapping_file(self, mapping_file):
        # path to mapping file
        self.mapping_file_path = self.dataset_path + 'mapping/' + mapping_file
