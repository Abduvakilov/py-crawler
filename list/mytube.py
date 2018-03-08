import sys
sys.path.append(sys.path[0].replace('/list', ''))

import crawl

crawler = crawl.Crawl('http://mytube.uz')


crawler.require = './/div[@class="WhiteBlock CommentsBlock"]'

def scrape(t):
	t.get_data('description', './/div[@id="aboutUser"]/pre')
	t.get_data('category', './/span[@class="userinfobox-categories-tags-container"]/a[1]')
	t.get_data_array('tags', './/span[@class="userinfobox-categories-tags-container"]/a[not(position()=1)]')
	t.get_data_int('views', './/div[@class="Views-Container"]')
	t.get_data_date('publishDate', './/div[@class="Date"]/text()[last()]')



crawler.scrape   = scrape
# crawler.urlNotContains.extend()

crawler.crawl()