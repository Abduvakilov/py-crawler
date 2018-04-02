import time
start = time.time()

from urllib.request import urlopen
import urllib.error
import datetime
import target
import os
class Crawl:
	EXPIRY_DAYS     = 5
	MAX_VISITS      = 1000
	numPagesVisited = 0
	urlNotContains  = ['#','.jpg','mailto:']
	if 'max' in os.environ:
		MAX_VISITS  = int(os.environ['max'])
	
	def __init__(self, startUrl, enc='utf8'):
		self.domain = target.Domain(startUrl, enc)

	day           = datetime.datetime.now().strftime('%d.%m.%y')
	crawledBefore = (datetime.datetime.now() - datetime.timedelta(days=EXPIRY_DAYS)).strftime('%d.%m.%y')

	require2 = None

	def crawl(self):
		while self.numPagesVisited <= self.MAX_VISITS:
			url   = self.domain.next_url(self.crawledBefore)
			self.numPagesVisited +=1
			print('->', self.numPagesVisited, ': ', url)

			urlParse  = target.parse.urlparse(url)
			encodedUrl = urlParse.scheme+'://'+urlParse.netloc+target.parse.quote(urlParse.path)
			if urlParse.query:
				encodedUrl+='?'+urlParse.query
			preUrl = None
			if 'preUrl' in os.environ:
				preUrl=os.environ['preUrl']+encodedUrl
			try:
				req = urlopen(preUrl or encodedUrl)
			except (UnicodeEncodeError, urllib.error.HTTPError) as e:
				target.es.update('crawled', url, {'doc':{'error': type(e).__name__, 'crawledDate': self.day}, 'doc_as_upsert': True})
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

			if req.geturl() != (preUrl or encodedUrl):
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
		if self.condition(t, self.require, self.require2):
			print('target found')

			self.scrape(t)

			for e in t.data:
				print(e + ': ' + str(t.data[e])) 
			t.send_data(self.day)
		else:
			t.not_found(self.day)

		t.links(self.urlNotContains)
		del t
		end = time.time()
		print('time: ' + str(int(down-start)) + ', ' + str(int((end-down)*1000)))

	def condition(self, t, xpath, xpath2):
		t.mainEl = t.lxml.find(xpath)
		return t.mainEl is not None



