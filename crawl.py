import time
start = time.time()

from urllib.request import urlopen
import urllib.error
import datetime
import target
import os
class Crawl:
	expiry_days        = 5
	max_pages_to_visit = 1000
	numPagesVisited    = 0
	urlNotContains     = ['#','.jpg']
	require2 = None
	try:
		max_pages_to_visit = int(os.environ['max'])
	except:
		pass
	
	def __init__(self, start_url):
		self.domain = target.Domain(start_url)

	day           = datetime.datetime.now().strftime('%d.%m.%y')
	crawledBefore = (datetime.datetime.now() - datetime.timedelta(days=expiry_days)).strftime('%d.%m.%y')


	def crawl(self):
		while self.numPagesVisited <= self.max_pages_to_visit:
			url   = self.domain.next_url(self.crawledBefore)
			self.numPagesVisited +=1
			print('Visiting page ', self.numPagesVisited, ': ', url)
			quoted_url = ''
			try:
				req = urlopen(url)
			except UnicodeEncodeError:
				url_parse  = target.parse.urlparse(url)
				quoted_url = url_parse.scheme+'://'+url_parse.netloc+target.parse.quote(url_parse.path)
				if url_parse.query:
					quoted_url+='?'+url_parse.query
				target.es.update('crawled', quoted_url, {'doc':{'crawled': self.domain.site, 'isTarget': False}, 'doc_as_upsert': True})
				target.es.update('crawled', url, {'doc':{'error': 'EncodeError', 'crawledDate': self.day}, 'doc_as_upsert': True})
				continue
			except urllib.error.HTTPError:
				target.es.update('crawled', url, {'doc':{'error': 'HTTPError', 'crawledDate': self.day}, 'doc_as_upsert': True})
				continue
			except Exception as e:
				template = "An exception of type {0} occurred. Arguments:\n{1!r}"
				message = template.format(type(e).__name__, e.args)
				print(message)
				continue

			code  = req.getcode()
			def visit_if_html(req):
				if 'html' in req.info().get_content_subtype().lower():
					self.visit(req)
				else:
					print('not html on ' + url)
					target.es.update('crawled', url, {'doc':{'error': 'not html', 'crawledDate': self.day}, 'doc_as_upsert' : True})


			if (req.geturl() != url) and (req.geturl() != quoted_url):
					target.es.update('crawled', url, {'doc':{'error': 'redirected', 'crawledDate': self.day}, 'doc_as_upsert' : True})
					print('redirected to '+req.geturl())
					if target.parse.urlparse(req.geturl()).netloc == self.domain.site:
						visit_if_html(req)
			elif code < 300:
				visit_if_html(req)

			else:
				print('code>=300')
				target.es.update('crawled', url, {'doc':{'error': 'code>299', 'crawledDate': self.day}, 'doc_as_upsert': True})

		print('Reached the limit')

	def visit(self, req):
		down = time.time()
		t    = target.Target(req, self.domain)
		
		# Main Part
		if t.required(self.require1, self.require2):
			print('target found')

			self.scrape(t)

			for e in t.data:
				print(e + ' ' + str(t.data[e])) 
			t.send_data(self.day)
		else:
			t.not_found(self.day)

		t.links(self.urlNotContains)

		end = time.time()
		print('Total and individual Scrape time: ' + str(down-start) + ', ' + str(end-down))




