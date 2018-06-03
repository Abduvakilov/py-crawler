import sys
sys.path.append(sys.path[0].replace('/list', ''))
sys.path.append(sys.path[0].replace('\\list', ''))
import crawl

crawler = crawl.Crawl('http://topmusic.uz', 'windows-1251')

def condition(t, req1, req2):
	if '/album-' in t.url:
		crawler.scrape = albumScrape
		return True
	else:
		crawler.scrape = artistScrape
		if t.lxml.find('.//div[@id="clips_section"]') is not None:
			return True
		elif t.lxml.find('.//div[@id="singls_section"]') is not None:
			return True
		else:
			return False

def artistScrape(t):
	t.lxml = t.lxml.find('.//div[@class="box-mid"]')
	t.get_data('title', './/h2[1]')
	t.get_data('genre', './div[1]//a[1]')
	t.get_atr_array('clip', './/div[@class="clip-box"]/a[3]/@title', 20) #cuts 20chars in the beginning
	t.get_atr_array('single', './/a[@class="play-track"]/@title')

def albumScrape(t):
	t.lxml = t.lxml.find('.//div[@class="box-mid"]')
	t.get_data('albumName', './div[1]/table/tbody/tr[1]/td[2]')
	t.get_atr('img', './div[1]/img/@src')
	t.get_data('artistName', './div[1]/table/tbody/tr[2]/td[2]')
	t.get_data('artistLink', './div[1]/table/tbody/tr[2]/td[2]/a/@href')
	t.get_data('genre', './div[1]/table/tbody/tr[3]/td[2]')
	t.get_data('year', './div[1]/table/tbody/tr[4]/td[2]')
	t.get_data_array('song', './/div[@class="block"]//table//span')


crawler.condition = condition
crawler.urlNotContains.extend(('/play/', '/get/', 'javascript:', '.pls', '/download/'))
crawler.crawl()
