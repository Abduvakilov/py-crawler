import sys
sys.path.append(sys.path[0].replace('/list', ''))
sys.path.append(sys.path[0].replace('\\list', ''))
import crawl

crawler = crawl.Crawl('http://mediabox.uz/ru')

crawler.require = './/p[@class="col-lg-12 inner_title"]'
selector = {
  "release" : "Год:",
  "country" : "Страна:",
  "genre"   : "Жанр:",
  "subtitle": "Слоган:",
  "budget"  : "Бюджет:",
  "producer": "Продюсер:",
  "director": "Режиссёр:",
  "actor"   : "Актеры:",
  "lang"    : "Язык:",
  "time"    : "Время:"
}
xpath = {}
for x in selector:
  xpath[x] = './/div[@id="info"]//td[text()="'+selector[x]+'")]/following-sibling::td'

def scrape(t):
  t.set_main('title')
  t.get_atr('img', './/div[@class="cover"]/img/@src')
  for x in xpath:
    t.get_data(x, xpath[x])

  t.get_data('forAge', './/div[@id="info"]/td[contains(., "Возраст:")]/following-sibling::td/b')
  t.get_data('description', './/div[@id="descripton"]')

crawler.urlNotContains.extend(('/uz/','/en/'))

crawler.scrape = scrape
crawler.crawl()
