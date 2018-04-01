import sys
sys.path.append(sys.path[0].replace('/list', ''))
sys.path.append(sys.path[0].replace('\\list', ''))
import crawl

crawler           = crawl.Crawl('http://tas-ix.me/')


crawler.require  = './/table[@id="topic_main"]//div[@class="post_wrap"]'
crawler.require2 =  './/fieldset[@class="attach"]'
def condition(self, xpath1, xpath2):
	self.mainEl = self.lxml.find(xpath1)
	if self.mainEl is not None:
		return self.mainEl.find(xpath2) is not None
	else: return False

crawler.condition = condition

def scrape(t):
		t.dropFromMain('.//fieldset[@class="attach"]')
		t.dropFromMain('//div[@class="sp-body" and @title="MediaInfo"]')
		t.dropFromMain('//script')
		t.set_main('description')

		t.get_data('title', './/h1[@class="maintitle"]')
		t.get_data_array('category', '(.//td[@class="nav w100"])[1]/a[not(position()=1)]')


crawler.scrape    = scrape
crawler.urlNotContains.extend(('privmsg.php'
								,'info.php'
								,'profile.php'
								,'posting.php'
								,'search.php'
								,'download.php'
								,'dl.php'
								,'magnet:?'
								,'&view='))

crawler.crawl()