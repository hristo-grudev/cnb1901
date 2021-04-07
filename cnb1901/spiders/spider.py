import scrapy

from scrapy.loader import ItemLoader

from ..items import Cnb1901Item
from itemloaders.processors import TakeFirst


class Cnb1901Spider(scrapy.Spider):
	name = 'cnb1901'
	start_urls = ['https://www.cnb1901.com/blog-cnb']

	def parse(self, response):
		post_links = response.xpath('//p//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagenation", " " ))]/text()[normalize-space()][last()]').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "blog_postcontent", " " ))]//p//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=Cnb1901Item(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
