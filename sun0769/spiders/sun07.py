# -*- coding: utf-8 -*-
import scrapy
from sun0769.items import Sun0769Item

class Sun07Spider(scrapy.Spider):
    name = 'sun07'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):

        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")   #获取所有tr列表
        print(tr_list)

        for tr in tr_list:
            item = Sun0769Item()
            item["title"] = tr.xpath("./td[2]/a[@class='news14']/@title").extract_first()
            item["href"] = tr.xpath("./td[2]/a[@class='news14']/@href").extract_first()  #详情页网址
            item["publish_date"] = tr.xpath("./td[last()]/text()").extract_first()
            yield scrapy.Request(
                item["href"],  #详情页网址
                callback=self.parse_detail,
                meta = {"item":item}

            )
        #<a href="http://wz.sun0769.com/index.php/question/questionType?type=4&amp;page=100500">></a>
        # 尖括号href有值代表有下一页，没有代表最后一页
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    #处理详情页
    def parse_detail(self,response):
        item = response.meta["item"]
        item["content"] = response.xpath("//td[@class='txt16_3']//text()").extract()
        item["content_img"] = response.xpath("//td[@class='txt16_3']//img/@src").extract() #路径不完整，要拼接
        item["content_img"] =['http://wz.sun0769.com'+i for i in item["content_img"]] #拼接路径
        # print(item)
        yield item
