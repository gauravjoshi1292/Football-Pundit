__author__ = 'gj1292'


from utils import load_as_json
from fixture_crawler import FixtureCrawler
from exception import ForbiddenAccessError
from urls import FIXTURE_URL, LEAGUE_TABLE_URL
from league_table_crawler import LeagueTableCrawler


REQUIRED_ENTRIES = 150


class Driver(object):
    def __init__(self, required_entries):
        self.required_entries = required_entries

    def crawl_all_fixtures(self):
        try:
            entries = load_as_json('data.json')
        except ValueError:
            entries = {'reports': []}

        stored_entries = len(entries['reports'])
        while stored_entries < self.required_entries:
            skip = stored_entries
            batch = 10
            for i in range(16):
                try:
                    f = FixtureCrawler(FIXTURE_URL, skip, batch)
                    f.browse_monthly_fixtures()
                except ForbiddenAccessError:
                    continue

                f.persist_reports()
                skip += 10
                stored_entries += 10

    def crawl_league_table(self):
        crawler = LeagueTableCrawler(LEAGUE_TABLE_URL)
        try:
            crawler.create_league_table()
        except:
            crawler.quit()

        crawler.persist_table()


if __name__ == '__main__':
    driver = Driver(REQUIRED_ENTRIES)
    # driver.crawl_league_table()
    driver.crawl_all_fixtures()
