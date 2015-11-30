__author__ = 'gj1292'

from selenium import webdriver

from utils import get_driver, get_soup_from_driver


class FixtureCrawler(object):
    def __init__(self, uri):
        self.driver = get_driver(uri)

    def crawl_monthly_pages(self):
        self.source = get_soup_from_driver(self.driver)
