# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import uuid
import logging as log
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

log.basicConfig(level=log.DEBUG)


class GramSpider(scrapy.Spider):
    name = 'gram'
    script = '''
            function main(splash)
                local num_scrolls = 2
                local scroll_delay = 1.0
            
                local scroll_to = splash:jsfunc("window.scrollTo")
                local get_body_height = splash:jsfunc(
                    "function() {return document.body.scrollHeight;}"
                )
                assert(splash:go(splash.args.url))
                splash:wait(splash.args.wait)
            
                for _ = 1, num_scrolls do
                    scroll_to(0, get_body_height())
                    splash:wait(scroll_delay)
                end        
                return splash:html()
            end
        '''

    def __init__(self, tag='fashionnairobi', *args, **kwargs):
        super(GramSpider, self).__init__(*args, **kwargs)
        self.tag=tag

    def start_requests(self):
        urls = [
            'https://www.instagram.com/explore/tags/{0}/'.format(self.tag),
        ]
        for url in urls:
            yield SplashRequest(url, self.parse,
                                        endpoint='execute',
                                        args={'wait': 2, 'lua_source': self.script})
            # yield SplashRequest(url, self.parse,
            #     endpoint='render.html',
            #     args={'wait': 0.5},
            # )
    def parse(self, response):
        filename = 'lua2.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        soup = BeautifulSoup(open(filename), 'html.parser')
        posts= soup.select('._mck9w')
        for post in posts:
            imgs=[ img for img in post.find('img').get('srcset', '').split(',')]
            imgurl = imgs[-1].split(' ')[0]
            # imgname= 'images/'+str(uuid.uuid4())+'.png'
            # r = requests.get(imgurl, stream=True)
            # with open(imgname, 'wb') as f:
            #     for chunk in r.iter_content(chunk_size=1024):
            #         if chunk:  # filter out keep-alive new chunks
            #             f.write(chunk)
            yield {
                'url': response.urljoin(post.find('a').get('href', '')),
                'tags': post.find('img').get('alt', ''),
                'imageset': imgs,
                # 'imagename': imgname
            }
            # imgurl = imgs[-1].split(' ')[0]
            # imgname= 'images/'+str(uuid.uuid4())+'.png'
            # r = requests.get(imgurl, stream=True)
            # with open(imgname, 'wb') as f:
            #     for chunk in r.iter_content(chunk_size=1024):
            #         if chunk:  # filter out keep-alive new chunks
            #             f.write(chunk)

        os.remove(filename)

if __name__ == '__main__':
    log.info('Nothing Happened')
    process = CrawlerProcess(get_project_settings())

    process.crawl(GramSpider)
    process.start()