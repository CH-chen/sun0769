# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
class Sun0769Pipeline(object):
    def process_item(self, item, spider):
        # print(item)
        item["content"] = self.process_content(item["content"]) #得到process_content里面content值
        print(item)
        return item

    def process_content(self,content):
        ##处理content里面的空白字符，\r\n,\t
        content = [re.sub(r"\xa0|\s|\r\n|\t","",i) for i in content] #把\xa0，空格，\r\n,\t替换成空字符串
        content = [i for i in content if len(i)>0]  #然后去除列表中的空字符串

        return content

