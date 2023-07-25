from src.ExecuteQueryClass import ExecuteQueryClass
from src.PathClass import PathClass
from src.SparqlQueryClass import SparqlQuery
from src.UriClass import Uri

path = PathClass('stock_exchange_20230705')
path.set_mapping_file('mapping.json')
execute = ExecuteQueryClass(path, 'stock_exchange_20230629', dbms='postgres')
uri = Uri(path)
query = path.common_query_path + 'Q3.json'  # uncomment to select a query

sparql_query = SparqlQuery(query, uri)
# sparql_query.check_triples_cycle()
# sparql_query.set_ranks_for_triples()
sparql_query.order_triples_in_query()
pass
