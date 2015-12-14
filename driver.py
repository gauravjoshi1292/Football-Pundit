__author__ = 'gj1292'


from utils import load_as_json, dump_as_json
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
                    crawler = FixtureCrawler(FIXTURE_URL, skip, batch)
                    new_reports = crawler.browse_monthly_fixtures()
                except ForbiddenAccessError:
                    continue

                self.persist_reports(new_reports)
                skip += 10
                stored_entries += 10

    def crawl_league_table(self):
        crawler = LeagueTableCrawler(LEAGUE_TABLE_URL)
        try:
            crawler.create_league_table()
        except:
            crawler.quit()

        crawler.persist_table()

    def persist_reports(self, new_reports):
        """

        :return:
        """
        print new_reports
        try:
            reports = load_as_json('data.json')
        except ValueError:
            reports = {'reports': []}

        reports['reports'].extend(new_reports['reports'])
        valid_reports = self.validate(reports['reports'])
        dump_as_json(valid_reports, 'data.json', 'w')

    def validate(self, match_reports):
        """

        :param reports:
        :return:
        """
        print match_reports, len(match_reports)
        valid_match_reports = [dict(t) for t in set([tuple(r.items()) for r in match_reports])]
        print valid_match_reports, len(valid_match_reports)
        valid_reports = {'reports': valid_match_reports}

        return valid_reports

if __name__ == '__main__':
    driver = Driver(REQUIRED_ENTRIES)
    # driver.crawl_league_table()
    driver.crawl_all_fixtures()
    # f = FixtureCrawler(FIXTURE_URL, 0, 0)
    # driver.persist_reports({'reports': []})
