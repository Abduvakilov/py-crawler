import time
start = time.time()

from urllib2 import urlopen
import datetime
import target
class Crawl:
	expiry_days        = 5
	max_pages_to_visit = 1000
	numPagesVisited    = 0
	urlNotContains     = ['#','.jpg']
	require2 = None

	
	def __init__(self, start_url):
		self.domain = target.Domain(start_url)

	day           = datetime.datetime.now().strftime('%d.%m.%y')
	crawledBefore = (datetime.datetime.now() - datetime.timedelta(days=expiry_days)).strftime('%d.%m.%y')


	def crawl(self):
		while self.numPagesVisited <= self.max_pages_to_visit:
			url   = self.domain.next_url(self.crawledBefore)
			self.numPagesVisited +=1
			print 'Visiting page ', self.numPagesVisited, ': ', url
			try:
				req = urlopen(url)
			except Exception as e:
				print 'error getting url ' + str(self.numPagesVisited) + ' ' + url
				print e
				continue
			else:
				code  = req.getcode()
				if req.geturl() != url:
						target.es.update('crawled', url, {'doc':{'error': 'redirected', 'crawledDate': self.day}, 'doc_as_upsert' : True})
						print 'redirected'
				elif code < 300:
					if 'html' in req.info().type.lower():
						self.visit(req)
					else:
						print 'not html on ' + url
						target.es.update('crawled', url, {'doc':{'error': 'not html', 'crawledDate': self.day}, 'doc_as_upsert' : True})
						continue
				else:
					print 'code>=300'
					target.es.update('crawled', url, {'doc':{'error': 'code>299', 'crawledDate': self.day}, 'doc_as_upsert': True})
					continue
		print 'Reached the limit'

	def visit(self, req):
		down = time.time()
		t    = target.Target(req, self.domain)
		
		# Main Part
		if t.required(self.require1, self.require2):
			print 'target found'

			self.scrape(t)

			for e in t.data:
				print('%s: %s' % (e, t.data[e])) 
			t.send_data(self.day)
		else:
			t.not_found(self.day)

		t.links(self.urlNotContains)

		end = time.time()
		print 'Total and individual Scrape time: ' + str(down-start) + ', ' + str(end-down)




