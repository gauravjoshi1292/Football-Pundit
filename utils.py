__author__ = 'gj1292'

import json
import socket
import urllib2
import unicodedata
from sys import platform
from bson import json_util
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from urls import LEAGUE_TABLE_URL


def system_platform():
    """
    Returns system platform

    :rtype: str
    """
    if platform == "linux" or platform == "linux2":
        return "Linux"
    elif platform == "darwin":
        return "OS X"
    elif platform == "win32":
        return "Windows"


def get_control_key():
    """

    :return:
    """
    if system_platform() == "OS X":
        return Keys.COMMAND
    else:
        return Keys.CONTROL


def normalize(text):
    """
    Returns a NFKD normalized ASCII form of the text

    :type text: str

    :rtype: str
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')


def get_soup_from_url(url):
    """
    Given a url returns a soup of page source

    :param url: web url
    :type url: str

    :rtype: bs4.BeautifulSoup
    """
    try:
        response = urllib2.urlopen(url)
    except socket.error:
        proxy = urllib2.ProxyHandler({'http': 'http://bcproxy.ddu-india.com:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_chrome_driver():
    """
    Returns a selenium chrome driver

    :rtype: selenium.webdriver.chrome.webdriver.WebDriver
    """
    driver = webdriver.Chrome()
    return driver


def get_firefox_driver():
    """
    Returns a selenium firefox driver

    :rtype: selenium.webdriver.firefox.webdriver.WebDriver
    """
    driver = webdriver.Firefox()
    return driver


def get_safari_driver():
    """
    Returns a selenium safari driver

    :rtype: selenium.webdriver.safari.webdriver.WebDriver
    """
    driver = webdriver.Safari()
    return driver


def get_driver():
    """
    Return a selenium webdriver depending upon what's available on the system

    :rtype: selenium.webdriver.chrome.webdriver.WebDriver |
            selenium.webdriver.firefox.webdriver.WebDriver |
            selenium.webdriver.safari.webdriver.WebDriver
    """
    try:
        driver = get_firefox_driver()
    except WebDriverException:
        try:
            driver = get_chrome_driver()
        except WebDriverException:
            try:
                driver = get_safari_driver()
            except WebDriverException:
                print "Could not find selenium web driver on system! Quit!"
                return

    return driver


def get_table_from_url(url, table_class):
    """
    Given a url and table class, returns the table element with that class

    :param url: page url
    :type url: str

    :param table_class: table class
    :type table_class: str

    :rtype: bs4.element.ResultSet
    """
    soup = get_soup_from_url(url)
    table = soup.find('table', {'class': table_class})

    if not table:
        return []

    tds = table.find_all('td')
    return tds


def dump_as_json(data, json_file, mode):
    """
    Dumps the data into a json file

    :type data: dict

    :type mode: str

    :type json_file: str
    """
    with open(json_file, mode) as outfile:
        json.dump(data, outfile, indent=4, default=json_util.default)


def load_as_json(json_file):
    """
    Loads the json file and returns a json object

    :param json_file: input json file
    :type json_file: str

    :rtype: dict
    """
    with open(json_file, "r") as infile:
        data = json.load(infile, object_hook=json_util.object_hook)

    return data


def get_all_teams():
    return ['Arsenal', 'Aston Villa', 'Bournemouth', 'Chelsea', 'Crystal Palace',
            'Everton', 'Leicester', 'Liverpool', 'Manchester United', 'Manchester City',
            'Newcastle United', 'Norwich', 'Southampton', 'Stoke', 'Sunderland',
            'Swansea', 'Tottenham', 'Watford', 'West Bromwich Albion', 'West Ham']


def get_league_table():
    driver = get_driver()
    driver.get(LEAGUE_TABLE_URL)
    print driver.page_source


get_league_table()