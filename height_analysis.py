__author__ = 'gj1292'

from utils import load_as_json


def does_height_affect_results(match_reports):
    tall_team_wins = 0
    short_team_wins = 0
    same_height_wins = 0
    draws = 0
    for match_report in match_reports:
        home_goals = match_report['home_goals']
        away_goals = match_report['away_goals']
        home_team_height = match_report['home_team_height']
        away_team_height = match_report['away_team_height']

        if home_goals > away_goals:
            if home_team_height > away_team_height:
                tall_team_wins += 1
            elif home_team_height < away_team_height:
                short_team_wins += 1
            else:
                same_height_wins += 1

        elif home_goals < away_goals:
            if home_team_height < away_team_height:
                tall_team_wins += 1
            elif home_team_height > away_team_height:
                short_team_wins += 1
            else:
                same_height_wins += 1

        else:
            draws += 1

    print tall_team_wins, short_team_wins, same_height_wins, draws


def affects_of_opposition_height_on_team(team, match_reports):
    wins_against_taller_teams = {'home': 0, 'away': 0}
    wins_against_shorter_teams = {'home': 0, 'away': 0}
    draws_against_taller_teams = {'home': 0, 'away': 0}
    draws_against_shorter_teams = {'home': 0, 'away': 0}
    losses_against_taller_teams = {'home': 0, 'away': 0}
    losses_against_shorter_teams = {'home': 0, 'away': 0}

    for match_report in match_reports:
        if match_report['home_team'] == team:
            home_goals = match_report['home_goals']
            away_goals = match_report['away_goals']
            home_team_height = match_report['home_team_height']
            away_team_height = match_report['away_team_height']

            if home_goals > away_goals:
                if home_team_height < away_team_height:
                    wins_against_taller_teams['home'] += 1
                else:
                    wins_against_shorter_teams['home'] += 1

            elif home_goals < away_goals:
                if home_team_height < away_team_height:
                    losses_against_taller_teams['home'] += 1
                else:
                    losses_against_shorter_teams['home'] += 1

            else:
                if home_team_height < away_team_height:
                    draws_against_taller_teams['home'] += 1
                else:
                    draws_against_shorter_teams['home'] += 1

        elif match_report['away_team'] == team:
            home_goals = match_report['home_goals']
            away_goals = match_report['away_goals']
            home_team_height = match_report['home_team_height']
            away_team_height = match_report['away_team_height']

            if away_goals > home_goals:
                if away_team_height < home_team_height:
                    wins_against_taller_teams['away'] += 1
                else:
                    wins_against_shorter_teams['home'] += 1

            elif away_goals < home_goals:
                if away_team_height < home_team_height:
                    losses_against_taller_teams['away'] += 1
                else:
                    losses_against_shorter_teams['away'] += 1

            else:
                if away_team_height < home_team_height:
                    draws_against_taller_teams['away'] += 1
                else:
                    draws_against_shorter_teams['away'] += 1

    print wins_against_taller_teams, wins_against_shorter_teams
    print losses_against_taller_teams, losses_against_shorter_teams
    print draws_against_taller_teams, draws_against_shorter_teams


if __name__ == '__main__':
    reports = load_as_json('data.json')['reports']
    does_height_affect_results(reports)
    affects_of_opposition_height_on_team('Leicester', reports)
