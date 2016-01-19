__author__ = 'gj1292'

import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from web_browser import WebBrowser
from exception import ForbiddenAccessError
from utils import normalize, get_control_key, dump_as_json, load_as_json


class FixtureCrawler(object):
    def __init__(self, url, skip, batch):
        self.browser = WebBrowser()
        self.browser.get(url)

        # Check for forbidden access
        server_response = normalize(self.browser.find_element_by_css_selector("div[id='header']").text)
        if server_response == "Server Error":
            self.browser.quit()
            raise ForbiddenAccessError

        self.match_reports = {'reports': []}
        self.timeout = 300  # Wait for 300s for elements to load on the page
        self.skip = skip  # Number of fixtures to skip
        self.batch_size = batch  # Number of fixtures to crawl in one go

    def skip_elements(self, elements):
        """
        Cull the elements list based on skip attribute

        :param elements: list of elements to be culled
        :type elements:

        :rtype:
        """
        size = len(elements)
        skip = self.skip

        if size < self.skip:
            self.skip -= size
        else:
            self.skip = 0

        culled_elements = elements[skip:]
        return culled_elements

    def browse_monthly_fixtures(self):
        """
        Browses monthly fixture pages one by one
        """
        try:
            # Wait till links to match reports are active
            self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", self.timeout)

            # Find all links to match reports, cull them and browse them
            elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
            elements.reverse()
            culled_elements = self.skip_elements(elements)
            self.browse_match_reports(culled_elements)

        except TimeoutException:
            pass

        finally:
            # Browse previous months and then quit
            self.browse_previous_fixtures()
            self.browser.quit()

        return self.match_reports

    def browse_previous_fixtures(self):
        """
        Browses fixtures from previous months recursively
        """
        # If batch size is zero that means all fixtures have been browsed, so return
        if self.batch_size == 0:
            return

        # Wait till links to previous months are active
        self.browser.wait_till_element_is_loaded("span.ui-icon.ui-icon-triangle-1-w", self.timeout)

        # Navigate to previous month
        elem = self.browser.find_element_by_css_selector("span.ui-icon.ui-icon-triangle-1-w")
        self.browser.click_element(elem)

        # Wait till match report links are active
        self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", self.timeout)

        # Sleep for 5s
        time.sleep(5)

        # Find all links to match reports, cull them and browse them
        elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
        elements.reverse()
        culled_elements = self.skip_elements(elements)
        self.browse_match_reports(culled_elements)

        # Check if month is August, if not browse previous month
        month = normalize(self.browser.find_element_by_css_selector("a[id='date-config-toggle-button']").text)
        if month != "Aug 2015":
            self.browse_previous_fixtures()

    def browse_match_reports(self, elements):
        """
        Browses match reports one by one

        :param elements: list of elements which are links to match reports
        :type elements:
        """
        # Get control key based on system platform
        CONTROL_KEY = get_control_key()

        for elem in elements:
            # If batch size is zero that means all fixtures have been browsed, so return
            if self.batch_size == 0:
                break

            # Skip if required
            if self.skip != 0:
                self.skip -= 1
                continue

            # Save the window opener (current window, do not mistaken with tab... not the same)
            main_window = self.browser.current_window_handle()

            # Open match report in new tab
            self.browser.open_link_in_new_tab(elem)

            # Sleep for 5s
            time.sleep(5)

            # Switch tab to the new tab, which we will assume is the next one on the right
            self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

            # Put focus on current window which will, in fact, put focus on the current visible tab
            self.browser.switch_to_window(main_window)

            # Check for forbidden access
            server_response = normalize(self.browser.find_element_by_css_selector("div[id='header']").text)
            if server_response == "Server Error":
                self.browser.quit()
                raise ForbiddenAccessError

            # Analyze the match report
            self.analyze_match_report()

            # Close current tab
            self.browser.find_element_by_tag_name('body').send_keys(CONTROL_KEY + 'w')

            # Put focus on current window which will be the window opener
            self.browser.switch_to_window(main_window)

            # Decrement batch size
            self.batch_size -= 1

    def get_match_result(self):
        """
        Returns a dict containing information on match result

        :rtype:
        """
        # Wait till match header is loaded
        self.browser.wait_till_element_is_loaded("div[id='match-header']", self.timeout)

        # Extract match result from html source
        match_header_elem = self.browser.find_element_by_css_selector("div[id='match-header']")
        team_elements = match_header_elem.find_elements_by_css_selector("td[class='team']")
        home_team, away_team = normalize(team_elements[0].text), normalize(team_elements[1].text)
        result_elem = match_header_elem.find_element_by_css_selector("td[class='result']")
        home_goals, away_goals = map(int, normalize(result_elem.text).split(':'))
        kickoff_elements = match_header_elem.find_elements_by_css_selector("dd")
        date = normalize(kickoff_elements[-1].text)
        kickoff = normalize(kickoff_elements[-2].text)
        return {'home_team': home_team, 'away_team': away_team, 'home_goals': home_goals,
                'away_goals': away_goals, 'kickoff': kickoff, 'date': date}

    def go_to_match_preview(self):
        """
        Navigates to match preview
        """
        # Wait till navigation menu is active on page
        self.browser.wait_till_element_is_loaded("div[id='sub-navigation']", self.timeout)

        # Extract preview element from match source
        div_elem = self.browser.find_element_by_css_selector("div[id='sub-navigation']")
        li_elem = div_elem.find_element_by_css_selector("li")
        preview_elem = li_elem.find_element_by_css_selector("a")

        # Click on preview element
        self.browser.click_element(preview_elem)

        # Sleep for 3s
        time.sleep(3)

    def get_height_stats(self):
        """
        Returns height info for both teams

        :rtype:
        """
        # Wait till element is active
        self.browser.wait_till_element_is_loaded("div[class='stat-group']", self.timeout)

        # Extract height info from html source
        stat_group_elements = self.browser.find_elements_by_css_selector("div[class='stat-group']")
        stat_group_elem = stat_group_elements[1]
        stat_elements = stat_group_elem.find_elements_by_css_selector("div[class='stat']")
        height_elem = stat_elements[-1]
        height_val_elements = height_elem.find_elements_by_css_selector("span[class='stat-value']")
        home_team_height = float(normalize(height_val_elements[0].text))
        away_team_height = float(normalize(height_val_elements[-1].text))

        return {'home_team_height': home_team_height,
                'away_team_height': away_team_height}

    def analyze_match_report(self):
        """

        :return:
        """
        self.go_to_match_preview()
        match_result = self.get_match_result()
        height_stats = self.get_height_stats()

        match_report = dict()
        match_report.update(match_result)
        match_report.update(height_stats)

        self.match_reports['reports'].append(match_report)
