import sys
sys.path.append(sys.path[0].replace('/list', ''))
import crawl

crawler           = crawl.Crawl('http://tas-ix.me/')


crawler.require  = './/table[@id="topic_main"]//div[@class="post_wrap"]'
crawler.require2 =  './/fieldset[@class="attach"]'

def scrape(t):
		t.drop_from_required('.//fieldset[@class="attach"]')
		t.drop_from_required('//div[@class="sp-body" and @title="MediaInfo"]')
		t.drop_from_required('//script')
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