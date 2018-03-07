# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup

username = "deisaack@gmail.com"
password = "Jacktone1"


class FormreqSpider(scrapy.Spider):
    name = 'formreq'
    start_urls = ["http://bitbucket.org/account/signin/?next=/",]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        form = soup.find('form', {"class": "aui aid-form errors-below-inputs"})

        csrf = form.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//form[@class="aui aid-form errors-below-inputs"]',
            formdata={
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrf
            },
            callback=self.after_login)

    def after_login(self, response):
        print('='*1000)
        print(response.body.decode())
        print('\n'*10)
        # base_url = BASE_URL + '/public/'
        # for page in PAGES:
        #     yield Request(
        #         url=base_url + page + "?id=1",
        #         callback=self.action)
