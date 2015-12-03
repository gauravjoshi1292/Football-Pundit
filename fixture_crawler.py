__author__ = 'gj1292'

from urls import FIXTURE_URL
from web_browser import WebBrowser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from utils import normalize, get_control_key, dump_as_json


class FixtureCrawler(object):
    def __init__(self, uri):
        self.browser = WebBrowser(uri)
        self.match_reports = {'reports': []}
        self.timeout = 180

    def browse_monthly_fixtures(self):
        try:
            self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", 5)
            elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
            self.analyze_match_report()

        except TimeoutException:
            f.browse_previous_fixtures()

        finally:
            self.browser.quit()

    def browse_previous_fixtures(self):
        self.browser.wait_till_element_is_loaded("span.ui-icon.ui-icon-triangle-1-w", self.timeout)

        elem = self.browser.find_element_by_css_selector("span.ui-icon.ui-icon-triangle-1-w")
        self.browser.click_element(elem)

        self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", self.timeout)

        elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
        self.browse_match_reports(elements)

        month = normalize(self.browser.find_element_by_css_selector("a[id='date-config-toggle-button']").text)
        print month
        if month != "Aug 2015":
            self.browse_previous_fixtures()

    def browse_match_reports(self, elements):
        CONTROL_KEY = get_control_key()
        for elem in elements:
            # Save the window opener (current window, do not mistaken with tab... not the same)
            main_window = self.browser.current_window_handle()

            # Open the link in a new tab by sending key strokes on the element
            # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
            # first_link.send_keys(Keys.CONTROL + Keys.RETURN)
            self.browser.open_link_in_new_tab(elem)

            # Switch tab to the new tab, which we will assume is the next one on the right
            self.browser.find_element_by_tag_name('body').send_keys(CONTROL_KEY + Keys.TAB)

            # Put focus on current window which will, in fact, put focus on the current visible tab
            self.browser.switch_to_window(main_window)

            # do whatever you have to do on this page, we will just got to sleep for now
            self.analyze_match_report()

            # Close current tab
            self.browser.find_element_by_tag_name('body').send_keys(CONTROL_KEY + 'w')

            # Put focus on current window which will be the window opener
            self.browser.switch_to_window(main_window)

    def analyze_match_report(self):
        self.browser.wait_till_element_is_loaded("div[id='match-header']", self.timeout)
        match_header_elem = self.browser.find_element_by_css_selector("div[id='match-header']")
        team_elements = match_header_elem.find_elements_by_css_selector("td[class='team']")
        home_team, away_team = normalize(team_elements[0].text), normalize(team_elements[1].text)
        result_elem = match_header_elem.find_element_by_css_selector("td[class='result']")
        home_goals, away_goals = map(int, normalize(result_elem.text).split(':'))
        kickoff_elements = match_header_elem.find_elements_by_css_selector("dd")
        date = normalize(kickoff_elements[-1].text)
        kickoff = normalize(kickoff_elements[-2].text)
        print '\n\n', home_team, away_team, home_goals, away_goals, kickoff, date

        self.browser.wait_till_element_is_loaded("div[id='sub-navigation']", self.timeout)
        div_elem = self.browser.find_element_by_css_selector("div[id='sub-navigation']")
        li_elem = div_elem.find_element_by_css_selector("li")
        preview_elem = li_elem.find_element_by_css_selector("a")
        self.browser.click_element(preview_elem)

        self.browser.wait_till_element_is_loaded("div[class='stat-group']", self.timeout)
        # print self.browser.get_soup()
        # print '\n\n\n'

        stat_group_elements = self.browser.find_elements_by_css_selector("div[class='stat-group']")
        print stat_group_elements
        stat_group_elem = stat_group_elements[1]
        stat_elements = stat_group_elem.find_elements_by_css_selector("div[class='stat']")
        print stat_elements
        height_elem = stat_elements[-1]
        height_val_elements = height_elem.find_elements_by_css_selector("span[class='stat-value']")
        print height_val_elements
        print '\n\n', height_val_elements[0].text, height_val_elements[-1].text
        home_team_height = float(normalize(height_val_elements[0].text))
        away_team_height = float(normalize(height_val_elements[-1].text))

        match_report = dict()
        match_report['date'] = date
        match_report['kickoff'] = kickoff
        match_report['home_team'] = home_team
        match_report['away_team'] = away_team
        match_report['home_goals'] = home_goals
        match_report['away_goals'] = away_goals
        match_report['home_team_height'] = home_team_height
        match_report['away_team_height'] = away_team_height

        self.match_reports['reports'].append(match_report)
    
    def persist_reports(self):
        dump_as_json(self.match_reports, 'data.json')


f = FixtureCrawler(FIXTURE_URL)
f.browse_monthly_fixtures()
