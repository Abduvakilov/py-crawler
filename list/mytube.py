import sys
sys.path.append(sys.path[0].replace('/list', ''))

import crawl

crawler = crawl.Crawl('https://mover.uz/')


crawler.require1 = './/div[@id="aboutUser"]'

def scrape(t):
	t.set_main('title')

	t.get_data('description', './/div[@class="desc-text"]')
	t.data['description'] = t.data['description'][:-19]
	# print t.data['description']
	t.get_data('category', './/p[@class="cat-date"]/a')
	t.get_data_array('tags', './/p[@class="tags"]/a')
	t.get_data_int('views', './/span[@class="fr views"]/strong')
	t.get_data_int('likes', './/table[@class="r-desc"]/tr/td[@class="like"]')
	t.get_data_int('dislikes', './/table[@class="r-desc"]/tr/td[@class="dislike"]')



crawler.scrape   = scrape
# crawler.urlNotContains.extend()

crawler.crawl()