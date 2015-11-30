__author__ = 'gj1292'

from selenium import webdriver


class WebDriver(object):
    def __init__(self, url):
        self.driver

    def get_chrome_driver(self, url):
        """
        Returns a selenium chrome driver

        :param url: page url
        :type url: str


        :rtype: selenium.webdriver.chrome.webdriver.WebDriver
        """
        driver = webdriver.Chrome()
        driver.get(url)
        return driver

    def get_firefox_driver(url):
        """
        Returns a selenium firefox driver

        :param url: page ur;
        :type url: str

        :rtype: selenium.webdriver.firefox.webdriver.WebDriver
        """
        driver = webdriver.Firefox()
        driver.get(url)
        return driver

    def get_safari_driver(url):
        """
        Returns a selenium safari driver

        :param url: page url
        :type url: str

        :rtype: selenium.webdriver.safari.webdriver.WebDriver
        """
        driver = webdriver.Safari()
        driver.get(url)
        return driver

    def get_driver(url):
        """
        Return a selenium webdriver depending upon what's available on the system

        :param url: page url
        :type url: str

        :rtype: selenium.webdriver.chrome.webdriver.WebDriver |
                selenium.webdriver.firefox.webdriver.WebDriver |
                selenium.webdriver.safari.webdriver.WebDriver
        """
        try:
            driver = get_chrome_driver(url)
        except WebDriverException:
            try:
                driver = get_firefox_driver(url)
            except WebDriverException:
                try:
                    driver = get_safari_driver(url)
                except WebDriverException:
                    print "Could not find selenium web driver on system! Quit!"
                    return

        return driver

    def scroll_to_bottom(driver):
        """
        Scrolls to the bottom of web page

        :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                      selenium.webdriver.firefox.webdriver.WebDriver |
                      selenium.webdriver.safari.webdriver.WebDriver
        """
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_till_page_is_loaded(driver):
        """
        Scrolls down until the complete web page is loaded

        :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                      selenium.webdriver.firefox.webdriver.WebDriver |
                      selenium.webdriver.safari.webdriver.WebDriver
        """
        old_source = ''
        source = driver.page_source

        while source != old_source:
            scroll_to_bottom(driver)
            time.sleep(1)
            old_source = source
            source = driver.page_source

    def get_soup_from_driver(driver):
        """
        Given a selenium web driver return the soup

        :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                      selenium.webdriver.firefox.webdriver.WebDriver|
                      selenium.webdriver.safari.webdriver.WebDriver

        :rtype: bs4.BeautifulSoup
        """
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        return soup

    def get_table_from_driver(url, table_id):
        """
        Returns the table element with the given id from the web page

        :param url: page url
        :type url: str

        :param table_id: table id
        :type table_id: str

        :rtype: bs4.element.Tag
        """
        driver = get_driver(url)
        scroll_till_page_is_loaded(driver)
        soup = get_soup_from_driver(driver)
        table = soup.find('table', table_id)
        driver.quit()
        return table
