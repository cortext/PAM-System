from elasticsearch import Elasticsearch

es = Elasticsearch()
res = es.search(index="test", doc_type="articles", body={"query": {"match": {"content": "fox"}}})
print("%d documents found" % res['hits']['total'])
for doc in res['hits']['hits']:
    print("%s) %s" % (doc['_id'], doc['_source']['content'])) 
