__author__ = 'gj1292'


from urls import FIXTURE_URL
from utils import load_as_json
from fixture_crawler import FixtureCrawler
from exception import ForbiddenAccessError


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
            for i in range(15):
                try:
                    f = FixtureCrawler(FIXTURE_URL, skip, batch)
                    f.browse_monthly_fixtures()
                except ForbiddenAccessError:
                    continue

                f.persist_reports()
                skip += 10
                stored_entries += 10


if __name__ == '__main__':
    driver = Driver(REQUIRED_ENTRIES)
    driver.crawl_all_fixtures()
