import time
import csv


class TimingClass:
    timing_list = []
    query_name = None
    start_time = None

    def __init__(self, query_name, keyword):
        self.query_name = query_name
        TimingClass.query_name = query_name
        self.keyword = keyword
        self.start_time = None
        self.end_time = None
        self.execution_time = None
        pass

    def record_start(self):
        self.start_time = time.time()
        TimingClass.start_time = self.start_time

    def record_end(self):
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time
        TimingClass.timing_list.append([self.query_name, self.keyword, self.execution_time])

    @staticmethod
    def store_timing():
        with open(f'timing.csv', 'a', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            for timing in TimingClass.timing_list:
                timing.insert(1, TimingClass.start_time)
                csv_writer.writerow(timing)
