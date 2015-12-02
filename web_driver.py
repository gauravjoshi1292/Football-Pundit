__author__ = 'gj1292'

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

from utils import get_driver


class WebDriver(object):
    def __init__(self, url):
        self.driver = get_driver(url)

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of web page
        """
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_till_page_is_loaded(self):
        """
        Scrolls down until the complete web page is loaded
        """
        old_source = ''
        source = self.driver.page_source

        while source != old_source:
            self.scroll_to_bottom()
            time.sleep(1)
            old_source = source
            source = self.driver.page_source

    def get_soup(self):
        """
        Given a selenium web driver return the soup

        :rtype: bs4.BeautifulSoup
        """
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        return soup

    def get_table(self, table_id):
        """
        Returns the table element with the given id from the web page

        :param table_id: table id
        :type table_id: str

        :rtype: bs4.element.Tag
        """
        self.scroll_till_page_is_loaded()
        soup = self.get_soup()
        table = soup.find('table', table_id)
        self.driver.quit()
        return table

    def find_element_by_css_selector(self, selector):
        """

        :param selector:
        :return:
        """
        return self.driver.find_element_by_css_selector(selector)

    def find_elements_by_css_selector(self, selector):
        """

        :param selector:
        :return:
        """
        return self.driver.find_elements_by_css_selector(selector)

    def click_element(self, elem):
        actions = ActionChains(self.driver)
        actions.move_to_element(elem)
        actions.click(elem)
        actions.perform()

    def quit(self):
        self.driver.quit()
