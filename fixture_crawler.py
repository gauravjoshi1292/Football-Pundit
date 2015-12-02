__author__ = 'gj1292'

import time

from urls import FIXTURE_URL
from web_driver import WebDriver


class FixtureCrawler(object):
    def __init__(self, uri):
        self.driver = WebDriver(uri)

    def crawl_monthly_pages(self):
        source = self.driver.get_soup()
        # print source
        f.previous_page()
        self.driver.quit()

    def previous_page(self):
        elem = self.driver.find_element_by_css_selector("span.ui-icon.ui-icon-triangle-1-w")
        self.driver.click_element(elem)
        time.sleep(1)
        source = self.driver.get_soup()
        # print source
        elems = self.driver.find_elements_by_css_selector("a[class='match-link match-report rc']")
        print elems


f = FixtureCrawler(FIXTURE_URL)
f.crawl_monthly_pages()
