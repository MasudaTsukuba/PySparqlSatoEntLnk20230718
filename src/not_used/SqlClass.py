# import re  # regular expression
#
#
# class Sql:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def convert(sparql_query):  # sparql to sql
#         select_var = ''
#         for var in sparql_query.var_list:  # list of variables in sparql query
#             select_var += var + ', '  # change them to a comma-separated string
#         select_var = re.sub(', $', '', select_var)  # remove the comma at the end
#         exe_query = 'SELECT ' + select_var + ' FROM '
#         for item in sparql_query.sql_query:
#             exe_query += ' (' + item + ') NATURAL JOIN '  # combine with NATURAL JOIN
#         exe_query = re.sub('NATURAL JOIN $', '', exe_query)  # remove the "NATURAL JOIN" at the end
#         exe_query = exe_query.replace(';', '') + ';'  # end up with a semicolon while suppressing a duplicate
#         # print(exe_query)
#         return exe_query  # return the built sql query
