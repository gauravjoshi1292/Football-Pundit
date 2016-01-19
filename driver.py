__author__ = 'gj1292'


from utils import load_as_json, dump_as_json
from fixture_crawler import FixtureCrawler
from exception import ForbiddenAccessError
from urls import FIXTURE_URL, LEAGUE_TABLE_URL
from league_table_crawler import LeagueTableCrawler


REQUIRED_ENTRIES = 220


class Driver(object):
    def __init__(self, required_entries=0, skip=0):
        self.required_entries = required_entries
        self.skip = skip

    def crawl_all_fixtures(self):
        try:
            entries = load_as_json('data.json')
        except ValueError:
            entries = {'reports': []}

        stored_entries = len(entries['reports'])
        print "stored entries:", stored_entries
        while stored_entries < self.required_entries:
            batch = 2
            try:
                print "stored:", stored_entries, "req:", self.required_entries, "skip:", self.skip
                crawler = FixtureCrawler(FIXTURE_URL, self.skip, batch)
                new_reports = crawler.browse_monthly_fixtures()
            except ForbiddenAccessError:
                continue

            self.persist_reports(new_reports)
            self.skip += 2
            stored_entries += 2

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
        valid_match_reports = []
        checklist = []
        for report in match_reports:
            home_team, away_team = report['home_team'], report['away_team']
            if (home_team, away_team) not in checklist:
                checklist.append((home_team, away_team))
                valid_match_reports.append(report)

        valid_reports = {'reports': valid_match_reports}

        return valid_reports

if __name__ == '__main__':
    driver = Driver(required_entries=REQUIRED_ENTRIES, skip=46)
    # driver.crawl_league_table()
    driver.crawl_all_fixtures()
    # f = FixtureCrawler(FIXTURE_URL, 0, 0)
    # driver.persist_reports({'reports': []})

    # data = load_as_json('data.json')
    # teams = {}
    # for i in data['reports']:
    #     try:
    #         teams[i['home_team']] += 1
    #     except KeyError:
    #         teams[i['home_team']] = 1
    #
    #     try:
    #         teams[i['away_team']] += 1
    #     except KeyError:
    #         teams[i['away_team']] = 1
    #
    # print teams
    # dump_as_json(new_data, 'data.json', 'w')
