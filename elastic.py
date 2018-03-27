import os
import elasticsearch
if 'es' in os.environ:
	es     = elasticsearch.Elasticsearch(os.environ['es'])
elif 'espr' in os.environ:
	es     = elasticsearch.Elasticsearch(os.environ['espr'],
    			http_auth=(os.environ['esu'], os.environ['esp']),
    			scheme="http",
    			port=int(os.environ['port'])
    		)
else:
	es     = elasticsearch.Elasticsearch()

nextPages = []
def exists(url):
	return es.exists(index="crawled", doc_type='crawled', id=url)

# def getSiteId(url):
	# Future plan to make sites filter by their id

def next(crawledBefore, site):
	global nextPages
	nextpage = ''
	def cont():
		global nextPages
		nextpage  = nextPages[0]
		nextPages = nextPages[1:]
		return nextpage

	if len(nextPages) != 0:
		return cont()
	else:
		try:
			res = es.search(index="crawled", doc_type="crawled",
			    body={
					'size' : 100,
					'_source': False,
					'query': {
						'bool': {
							'must': [
								{'term' : {'crawled.keyword' : site}},
								{'term' : {'isTarget'   : False}}
							],
							'filter': {
								'bool': {
									'should': [
										{'range': {'crawledDate': {'lt':crawledBefore}}},
										{'bool' : {'must_not'   : {'exists': {'field': 'crawledDate'}}}}
									]
								}
							}
						}
					}
				})
		except elasticsearch.ElasticsearchException as err:
			print(err)
		else:
			if res['hits']['total'] != 0:
				nextPages = [e['_id'] for e in res['hits']['hits']]
				return cont()
			else:
				print('no nextpage')
				import sys
				sys.exit(0)

def update(index, _id, body):
	try:
		return es.update(index=index, doc_type=index, id=_id, body=body, _source=False)
	except elasticsearch.ElasticsearchException as err:
		print(err)
	# else:
	# 	print res
