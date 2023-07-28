from SPARQLWrapper import SPARQLWrapper, JSON
import csv

sparql_endpoint = SPARQLWrapper('https://query.wikidata.org/sparql')

sparql_query = '''
SELECT ?s ?author ?author_label
WHERE {
    ?s wdt:P31 wd:Q7725634;
        wdt:P50 ?author.
    ?author rdfs:label ?author_label .
    FILTER (lang(?author_label) = "en")    
} LIMIT 100000
'''
sparql_endpoint.setQuery(sparql_query)
sparql_endpoint.setReturnFormat(JSON)
query_results = sparql_endpoint.query().convert()
rows = []
for result in query_results["results"]["bindings"]:
    rows.append([result['s']['value'], result['author']['value'], result['author_label']['value']])

with open('../../data/book20230728/csv/book_author.csv', 'w', encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["uri", "author", "author_label"])
    csv_writer.writerows(rows)
