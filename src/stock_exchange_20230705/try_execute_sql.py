from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass

path = PathClass('stock_exchange_20230705')
execute = ExecuteQueryClass(path, 'stock_exchange_20230629', dbms='postgres')
exe_query = '''
SELECT DISTINCT "c0" FROM (
SELECT DISTINCT "c0" FROM "src_Thing" 
) AS FOO0
NATURAL JOIN (
SELECT DISTINCT "c0" FROM "src_Person" 
) AS FOO1
NATURAL JOIN (
SELECT DISTINCT "c0" FROM "src_involvesInstrument" 
) AS FOO2
NATURAL JOIN (
SELECT DISTINCT "c0" FROM "src_FinantialInstrument" 
) AS FOO3
NATURAL JOIN (
SELECT DISTINCT "c0" FROM "src_Stock" 
) AS FOO4
;
'''
# exe_query = '''
# SELECT DISTINCT var0 FROM (SELECT CONCAT('http://www.owl-ontologies.com/Ontology1207768242.owl#ns/', A."c0") as var0
# FROM "src_Thing" as A, "src_Person" as B, "src_involvesInstrument" as C, "src_FinantialInstrument" as D, "src_Stock" as E
# WHERE A."c0" = B."c0" AND B."c0" = C."c0" AND C."c0" = D."c0" AND D."c0" = E."c0") AS FOO0;
# '''
execute.execute_sql(exe_query)
