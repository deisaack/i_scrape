# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging as log
import json
import os
from safi.items import PostItem
import datetime


class FotiSpider(scrapy.Spider):
    name = 'foti'
    nex_page = 'https://www.instagram.com/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&variables=%7B%22tag_name%22%3A%22{tag}%22%2C%22first%22%3A{first}%2C%22after%22%3A%22{cursor}%22%7D'
    first = 200

    def __init__(self, tag='pawabridge', *args, **kwargs):
        super(FotiSpider, self).__init__(*args, **kwargs)
        self.tag = tag

    def start_requests(self):
        urls = [
            'https://www.instagram.com/explore/tags/{0}/?__a=1'.format(self.tag),
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print('\n'*20)
        body = json.loads(response.body)
        has_next_page = body['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        end_cursor = body['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        edges = body['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        edges += body['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']
        for edge in edges:
            yield self.parse_node(edge['node'])

        if has_next_page:
            next_page_url = self.nex_page.format(tag=self.tag, first=self.first, cursor=end_cursor)
            yield scrapy.Request(next_page_url, callback=self.parse_next)

    def parse_next(self, response):
        body = json.loads(response.body)
        has_next_page = body['data']['hashtag']['edge_hashtag_to_media']['page_info']['has_next_page']
        end_cursor = body['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
        edges = body['data']['hashtag']['edge_hashtag_to_media']['edges']
        edges += body['data']['hashtag']['edge_hashtag_to_top_posts']['edges']
        for edge in edges:
            yield self.parse_node(edge['node'])

        if has_next_page:
            next_page_url = self.nex_page.format(tag=self.tag, first=self.first, cursor=end_cursor)
            yield scrapy.Request(next_page_url, callback=self.parse_next)

    def parse_node(self, node):
        item = PostItem()
        item['id'] = int(node['id'])
        item['shortcode'] = node['shortcode']
        item['comments'] = int(node['edge_media_to_comment']['count'])
        item['likes'] = int(node['edge_liked_by']['count'])
        time_stamp = node['taken_at_timestamp']
        item['timestamp'] = datetime.datetime.fromtimestamp(time_stamp).isoformat()
        item['owner_id'] = int(node['owner']['id'])
        item['image'] = node['display_url']
        item['tag'] = self.tag
        try: item['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
        except: item['caption'] = None
        # item['tags'] = Todo
        item.save()
        return item

    #
    # def parse(self, response):
    #     # follow links to author pages
    #     for href in response.css('.author + a::attr(href)'):
    #         yield response.follow(href, self.parse_author)
    #
    #     # follow pagination links
    #     for href in response.css('li.next a::attr(href)'):
    #         yield response.follow(href, self.parse)
    #
    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()
    #
    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }