# class for handling the output of sparql queries into a file
# 2023/6/1, Tadashi Masuda
# Amagasa Laboratory, University of Tsukuba

import csv


# write the sparql query results into a file
class Output:
    def __init__(self):
        pass

    # 結果の表示, output.csvに出力される
    @staticmethod
    def save_file(output, results, headers):
        output = output.replace('.txt', '.csv')
        sorted_results = results
        index = 0
        results2 = []
        for item in results:
            if not isinstance(item[0], str):
                print(index, item)
                results2.append(['None']+item[1:])
            else:
                results2.append(item)
            index += 1
        if results2:
            dimension = len(results2[0])
            sorted_results = results2
            for i in range(dimension):
                sorted_results = sorted(sorted_results, key=lambda x: x[dimension-i-1])  # sort
            # try:
            #     sorted_results = sorted(results, key=lambda x: x[0])  # sort
            # except:
            #     pass
            with open(output, mode='w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(headers)
                writer.writerows(sorted_results)
        else:
            print('Query results empty.')
