__author__ = 'gj1292'

from urls import FIXTURE_URL
from web_browser import WebBrowser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class FixtureCrawler(object):
    def __init__(self, uri):
        self.browser = WebBrowser(uri)

    def browse_monthly_fixtures(self):
        try:
            self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", 3)
            elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
            self.analyze_match_report()

        except TimeoutException:
            f.browse_previous_fixtures()

        finally:
            self.browser.quit()

    def browse_previous_fixtures(self):
        self.browser.wait_till_element_is_loaded("span.ui-icon.ui-icon-triangle-1-w", 3)

        elem = self.browser.find_element_by_css_selector("span.ui-icon.ui-icon-triangle-1-w")
        self.browser.click_element(elem)

        self.browser.wait_till_element_is_loaded("a[class='match-link match-report rc']", 3)

        elements = self.browser.find_elements_by_css_selector("a[class='match-link match-report rc']")
        self.browse_match_reports(elements)

        month = self.browser.find_element_by_css_selector("a[id='date-config-toggle-button']").text
        print month
        if month != "Aug 2015":
            self.browse_previous_fixtures()

    def browse_match_reports(self, elements):
        for elem in elements:
            # Save the window opener (current window, do not mistaken with tab... not the same)
            main_window = self.browser.current_window_handle()

            # Open the link in a new tab by sending key strokes on the element
            # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
            # first_link.send_keys(Keys.CONTROL + Keys.RETURN)
            self.browser.open_link_in_new_tab(elem)

            # Switch tab to the new tab, which we will assume is the next one on the right
            self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

            # Put focus on current window which will, in fact, put focus on the current visible tab
            self.browser.switch_to_window(main_window)

            # do whatever you have to do on this page, we will just got to sleep for now
            self.analyze_match_report()

            # Close current tab
            self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

            # Put focus on current window which will be the window opener
            self.browser.switch_to_window(main_window)

            break

    def analyze_match_report(self):
        source = self.browser.get_soup()
        div_elem = self.browser.find_element_by_css_selector("div[id='sub-navigation]")
        li_elem = div_elem.find_element_by_css_selector("li")
        preview_elem = li_elem.find_element_by_css_selector("a")
        self.browser.click_element(preview_elem)

f = FixtureCrawler(FIXTURE_URL)
f.browse_monthly_fixtures()
