import sys
sys.path.append(sys.path[0].replace('/list', ''))
sys.path.append(sys.path[0].replace('\\list', ''))
import crawl

crawler = crawl.Crawl('http://megasoft.uz', 'windows-1251')

crawler.require = './/a[starts-with(@href, "/get/")]'

def condition(t, xpath, xpath2):
	t.mainEl = t.lxml.xpath(xpath)
	return len(t.mainEl) != 0
crawler.condition = condition

stringSel = {
	"os"   : "Система:",
	"size" : "Размер файла: ",
	"lang" : "Язык интерфейса: "
}
other = {
	"publishDate"  : "Добавлено:",
	"downloadCount": "Количество загрузок: "
}
xpathstr = {}
xpath = {}
template = './/table[@width="300"]//td[text()="{0}"]/following-sibling::td'
for x in stringSel:
	xpathstr[x] = template.format(stringSel[x])
for x in other:
	xpath[x] = template.format(other[x])

def scrape(t):
	t.get_data('title', './/span[@class="title"]')
	t.get_data('category', './/span[@class="cat"]')
	for x in xpathstr:
	    t.get_data(x, xpathstr[x])
	t.get_data_date('publishDate', xpath['publishDate'])
	t.get_data_int('downloadCount', xpath['downloadCount'])

crawler.scrape = scrape
crawler.urlNotContains.extend(('?sort', '/get/'))
crawler.crawl()