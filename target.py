import elastic as es
from urllib import parse
import lxml.html as lxml

class Domain:
	def __init__(self, url):
		short    = parse.urlparse(url)
		self.site     = short.netloc
		self.base_url = short.scheme + '://' + self.site
		self.enc      = 'utf8'
		es.nextPages.append(url)
		if not es.exists(url):
			es.update('crawled', self.base_url, {'doc':{'crawled': self.site, 'isTarget': False}, 'doc_as_upsert': True})
			print('First start of ' + self.site)
			import time
			time.sleep(2)
	def next_url(self, crawledBefore):
		return es.next(crawledBefore, self.site)

class Target:
	br_replacer = ' '
	data        = {}

	def __init__(self, req, domain):
		self.url    = req.url
		self.domain = domain
		source      = req.read()
		if self.domain.enc != 'utf8':
			source.decode(self.domain.enc).encode('utf8')
		self.lxml = lxml.fromstring(source)

	def required(self, xpath1, xpath2):
		self.required_element = self.lxml.find(xpath1)
		if self.required_element is not None:
			if xpath2 is not None:
				return self.required_element.find(xpath2) is not None
			else: return True
		else: return False

	def drop_from(self, name, xpath):
		for element in self.lxml.xpath(xpath):
			element.drop_tree()

	def drop_from_required(self, xpath):
		for element in self.required_element.xpath(xpath):
			element.drop_tree()

	def set_main(self, name):
		for br in self.required_element.xpath('//br'):
			br.text = self.br_replacer
		self.data[name] = self.required_element.text_content().replace('\t', '').replace('\n', '')
		self.data[name] = self.space(self.data[name])

	def get_data(self, name, xpath):
		for br in self.required_element.xpath('//br'):
			br.text = self.br_replacer
		self.data[name] = self.lxml.xpath(xpath)[0].text_content().replace('\t', '').replace('\n', '')
		self.data[name] = self.space(self.data[name])

	def space(self, data):
		import re
		return " ".join(re.split("\s+", data, flags=re.UNICODE)).strip()

	def get_data_int(self, name, xpath):
		num = self.lxml.xpath(xpath)
		if num:
			import re
			self.data[name] = int(re.search(r'\d+', num[0].text_content()).group())

	def get_data_date(self, name, xpath, format=['%d %B %Y']):
		date = dateparser.parse(self.lxml.xpath(xpath)[0].text_content(), date_formats=format, languages=['ru'])
		if date:
			import dateparser
			self.data[name] = date.strftime('%d.%m.%y')

	def get_data_array(self, name, xpath):
		self.data[name] = [e.text_content() for e in self.lxml.xpath(xpath)]

	def send_data(self, day):
		self.data['crawledDate'] = day
		es.update('targets', self.url, {'doc': self.data, 'doc_as_upsert': True})
		es.update('crawled', self.url, {'doc':{'crawledDate': day, 'isTarget':True}, 'doc_as_upsert': True})

	def not_found(self, day):
		res = es.update('crawled', self.url, {'doc':{'crawledDate': day, 'isTarget':False}, 'doc_as_upsert': True})
		# print res

	def links(self, notContains):
		unique_links = []
		out = []
		actions = []
		def noSubstring(a):
			for r in notContains:
				if r in a:
					return False
			return True
		for a in self.lxml.xpath('//a/@href'):
			if a not in unique_links and noSubstring(a):
				unique_links.append(a)
				url = parse.urlparse(a)
				if url.netloc == self.domain.site or url.netloc == '':
					try:
						quoted_path = parse.quote(url.path)
						if url.query:
							quoted_path+='?'+url.query
						absl = parse.urljoin(self.domain.base_url, quoted_path)	
					except ValueError:
						print('error____________________\n'+a)
					if parse.urlparse(absl).netloc == self.domain.site:
						actions.extend(({'create':{'_id': absl}}, {'crawled': self.domain.site, 'isTarget': False}))
		try:
			es.es.bulk(actions, index='crawled', doc_type='crawled')
		except es.elasticsearch.ElasticsearchException as err:
			print('error: ' + err)



