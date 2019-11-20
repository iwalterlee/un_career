# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashMiddleware
import time
from bs4 import BeautifulSoup
from ..items import Scrapy4Item
import datetime
import time

now_page = 1
last_page_on = True
last_page = {}
category = 0
class UnSpider(scrapy.Spider):
    name = 'un'

    def __init__(self):
        self.pagelist = []
        self.url = 'https://careers.un.org/lbw/home.aspx?viewtype=SJ&exp=All&level=0&location=All&occup=0&department=All&bydate=0&occnet=0&lang=en-US/'

    def start_requests(self):
        for i in range(5):
            script = self.lua_script(i,"Last")
            yield SplashRequest(url=self.url, callback=self.parse_final, dont_filter=True,endpoint='execute', args={
                            'wait': 10, 'images': 0, 'lua_source': script})

    def parse_final(self, response):
        global last_page
        pages = response.xpath('.//tr[@class="pager"]/td/table/tbody/tr/td/a/text()').extract()
        category = response.xpath('.//input[@id="ctl00_ContentPlaceHolder1_UNCareersLoader1_ctl00_RadtabStrip_Grid1_RadTabStrip1_ClientState"]/@value').extract()
        category = int(category[0].split('"')[3])
        if len(pages) > 0:
            last_page = int(pages[-1])+1
        else:
            last_page = 1
        print(f"pages :{pages}")
        print(f"category :{category}")
        print(f"last page :{last_page}")
        print("******"*20)
        for i in range(last_page):
            script = self.lua_script(category,i+1)
            yield SplashRequest(url=self.url, callback=self.parese_pos, dont_filter=True,endpoint='execute', args={
                            'wait': 10, 'images': 0, 'lua_source': script})
        # call function run for each categories

    def parese_pos(self,response):
        si = Scrapy4Item()
        bs4 = BeautifulSoup(response.text)
        raw = bs4.select(".sch-grid-standard")[0].select("tr")
        for ele in raw:
            if ele.get("align", True) == True and ele.td.text.strip() != "1" and ele.td.text.strip() != "<<":
                td_list = ele.select("td")
                si["title"] = td_list[0].text.strip()
                si["link"] = "https://careers.un.org/lbw/"+td_list[0].a["onclick"].split("'")[1]
                si["level"] = td_list[1].text.strip()
                si["job_network"] = td_list[3].text.strip()
                si["job_family"] = td_list[4].text.strip()
                si["department"] = td_list[5].text.strip()
                si["location"] = td_list[6].text.strip()
                si["deadline"] = datetime.datetime.strptime(td_list[7].text.strip(),"%d/%m/%Y").date()
                yield si

        print("&&&&&&&&"*20)

    def lua_script(self,category,page):
        script = f"""
        function main(splash, args)
          splash.images_enabled = true
          assert(splash:go(args.url))
          assert(splash:wait(2))
          js_1 = string.format("document.getElementById('ctl00_ContentPlaceHolder1_UNCareersLoader1_ctl00_RadtabStrip_Grid1_RadTabStrip1_ClientState').value = `{{'selectedIndexes':['{category}'],'logEntries':[],'scrollState':{{}}}}`",args.page)
          js_2 = string.format("__doPostBack('ctl00$ContentPlaceHolder1$UNCareersLoader1$ctl00$RadtabStrip_Grid1$RadTabStrip1','{category}')", args.page)
          js = string.format("__doPostBack('ctl00$ContentPlaceHolder1$UNCareersLoader1$ctl00$RadtabStrip_Grid1$gvSearchGrid','Page${page}')", args.page)
          splash:runjs(js_1)
          splash:runjs(js_2)
          assert(splash:wait(4))
          splash:runjs(js)
          assert(splash:wait(4))
          return splash:html()
        end
        """
        return script
