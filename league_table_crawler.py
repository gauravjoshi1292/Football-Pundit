__author__ = 'gj1292'

from web_browser import WebBrowser
from utils import dump_as_json, normalize
from exception import ForbiddenAccessError


class LeagueTableCrawler(object):
    def __init__(self, url):
        self.browser = WebBrowser()
        self.browser.get(url)

        # Check for forbidden access
        server_response = normalize(self.browser.find_element_by_css_selector("div[id='header']").text)
        if server_response == "Server Error":
            self.browser.quit()
            raise ForbiddenAccessError

        self.table = {}
        self.timeout = 300

    def create_league_table(self):
        self.browser.wait_till_element_is_loaded("tbody[class='standings']", self.timeout)
        table = self.browser.find_element_by_css_selector("tbody[class='standings']")
        rows = table.find_elements_by_tag_name("tr")

        for row in rows:
            columns = row.find_elements_by_tag_name("td")
            counter = 0
            pos, team, matches, wins, draws, losses, gf, ga, gd, points = 0, '', 0, 0, 0, 0, 0, 0, 0, 0
            for column in columns:
                text = normalize(column.text)

                if counter == 0:
                    pos = int(text)
                elif counter == 1:
                    team = text
                elif counter == 2:
                    matches = int(text)
                elif counter == 3:
                    wins = int(text)
                elif counter == 4:
                    draws = int(text)
                elif counter == 5:
                    losses = int(text)
                elif counter == 6:
                    gf = int(text)
                elif counter == 7:
                    ga = int(text)
                elif counter == 8:
                    gd = int(text)
                elif counter == 9:
                    points = int(text)
                elif counter == 10:
                    counter = 0
                    self.table[team] = {'pos': pos, 'matches': matches, 'wins': wins,
                                        'draws': draws, 'losses': losses, 'gf': gf,
                                        'ga': ga, 'gd': gd, 'points': points}

                counter += 1

        self.quit()

    def persist_table(self):
        dump_as_json(self.table, 'league_table.json', 'w')

    def quit(self):
        self.browser.quit()
