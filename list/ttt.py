import sys
sys.path.append(sys.path[0].replace('/list', ''))
sys.path.append(sys.path[0].replace('\\list', ''))

import crawl

crawler = crawl.Crawl('http://www.ttt.uz')

dictionary = {
    'year': ['Год выпуска', 'Год', 'Chiqarilgan yili'],
    'country': ['Страна', 'Davlat'],
    'genre': ['Жанр','Janr'],
    'time': ['Время','Davomiyligi'],
    'director': ['Режиссер','Rejisyor'],
    'actors': ['В главных ролях','Bosh ro’lda'],
    'version': ['Версия'],
    'dev': ['Разработчик'],
    'lang': ['Язык'],
    'tbd': ['Перевод','Tarjima']
  }
crawler.require = './/div[@class="entry-content"]'

def scrape(t):
	t.br_replacer=' ‧ '
	t.drop_from_required('.//script')

	t.set_main('description')

	t.get_data('title', './/h1[@class="entry-title"]')
	t.get_atr('img', './/img[@class="aligncenter wp-post-image"]/@src')
	t.get_data('publishDate', './/time[contains(concat(" ", @class, " "), " updated ")]')
	t.get_data_array('tags', './/span[@class="cat-links"]')

	t.data['publishDate'] = t.data['publishDate'][:6]+t.data['publishDate'][8:]
	arr = [x.strip() for x in t.data['description'].split('‧') if x.strip() != '']
	# print(t.data['description'])
	# print(arr)

	tbr=[]

	def key_found(el):
		for key in dictionary:
			for x in dictionary[key]:
				if el.startswith(x):
					t.data[key] = el.replace(x,'',1).replace(': ','',1)
					return True
		return False

	for i, e in enumerate(arr):
		if key_found(e):
			tbr.append(i)

	
	for e in sorted(tbr, reverse=True):
		del arr[e]
	if 'tbd' in t.data:
		del t.data['tbd']
	arr = [x.strip() for x in arr if x.strip() != '']
	t.data['description'] = t.br_replacer.join(arr).replace('Про фильм:','').replace(t.br_replacer[:-1]+t.br_replacer,'')

	




crawler.scrape   = scrape

crawler.crawl()
