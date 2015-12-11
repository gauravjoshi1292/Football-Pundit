__author__ = 'gj1292'

from utils import load_as_json, get_all_teams


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


def divide_matches_by_height(team, match_reports):
    matches_by_height = {'taller': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []},
                         'shorter': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []}}

    for match_report in match_reports:
        home_team = match_report['home_team']
        away_team = match_report['away_team']
        home_team_height = match_report['home_team_height']
        away_team_height = match_report['away_team_height']

        if home_team == team:
            if home_team_height < away_team_height:
                matches_by_height['taller']['home'] += 1
                matches_by_height['taller']['at_home_against'].append(away_team)
            else:
                matches_by_height['shorter']['home'] += 1
                matches_by_height['shorter']['at_home_against'].append(away_team)

        elif away_team == team:
            if away_team_height < home_team_height:
                matches_by_height['taller']['away'] += 1
                matches_by_height['taller']['at_away_against'].append(home_team)
            else:
                matches_by_height['shorter']['away'] += 1
                matches_by_height['shorter']['at_away_against'].append(home_team)

    return matches_by_height


def divide_wins_by_height(team, match_reports):
    wins_by_height = {'taller': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []},
                      'shorter': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []}}

    for match_report in match_reports:
        home_team = match_report['home_team']
        away_team = match_report['away_team']
        home_goals = match_report['home_goals']
        away_goals = match_report['away_goals']
        home_team_height = match_report['home_team_height']
        away_team_height = match_report['away_team_height']

        if home_team == team:
            if home_goals > away_goals:
                if home_team_height < away_team_height:
                    wins_by_height['taller']['home'] += 1
                    wins_by_height['taller']['at_home_against'].append(away_team)
                else:
                    wins_by_height['shorter']['home'] += 1
                    wins_by_height['shorter']['at_home_against'].append(away_team)

        elif away_team == team:
            if away_goals > home_goals:
                if away_team_height < home_team_height:
                    wins_by_height['taller']['away'] += 1
                    wins_by_height['taller']['at_away_against'].append(home_team)
                else:
                    wins_by_height['shorter']['away'] += 1
                    wins_by_height['shorter']['at_away_against'].append(home_team)

    return wins_by_height


def divide_draws_by_height(team, match_reports):
    draws_by_height = {'taller': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []},
                       'shorter': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []}}

    for match_report in match_reports:
        home_team = match_report['home_team']
        away_team = match_report['away_team']
        home_goals = match_report['home_goals']
        away_goals = match_report['away_goals']
        home_team_height = match_report['home_team_height']
        away_team_height = match_report['away_team_height']

        if home_team == team:
            if home_goals == away_goals:
                if home_team_height < away_team_height:
                    draws_by_height['taller']['home'] += 1
                    draws_by_height['taller']['at_home_against'].append(away_team)
                else:
                    draws_by_height['shorter']['home'] += 1
                    draws_by_height['shorter']['at_home_against'].append(away_team)

        elif away_team == team:
            if away_goals == home_goals:
                if away_team_height < home_team_height:
                    draws_by_height['taller']['away'] += 1
                    draws_by_height['taller']['at_away_against'].append(home_team)
                else:
                    draws_by_height['shorter']['away'] += 1
                    draws_by_height['shorter']['at_away_against'].append(home_team)

    return draws_by_height


def divide_losses_by_height(team, match_reports):
    losses_by_height = {'taller': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []},
                        'shorter': {'home': 0, 'at_home_against': [], 'away': 0, 'at_away_against': []}}

    for match_report in match_reports:
        home_team = match_report['home_team']
        away_team = match_report['away_team']
        home_goals = match_report['home_goals']
        away_goals = match_report['away_goals']
        home_team_height = match_report['home_team_height']
        away_team_height = match_report['away_team_height']

        if home_team == team:
            if home_goals < away_goals:
                if home_team_height < away_team_height:
                    losses_by_height['taller']['home'] += 1
                    losses_by_height['taller']['at_home_against'].append(away_team)
                else:
                    losses_by_height['shorter']['home'] += 1
                    losses_by_height['shorter']['at_home_against'].append(away_team)

        elif away_team == team:
            if away_goals < home_goals:
                if away_team_height < home_team_height:
                    losses_by_height['taller']['away'] += 1
                    losses_by_height['taller']['at_away_against'].append(home_team)
                else:
                    losses_by_height['shorter']['away'] += 1
                    losses_by_height['shorter']['at_away_against'].append(home_team)

    return losses_by_height


def bake_home_games_data(data):
    baked_data = {'against_taller_teams': {'top_five': 0, 'top_half': 0, 'bottom_half': 0, 'bottom_five': 0, 'teams': []},
                  'against_shorter_teams': {'top_five': 0, 'top_half': 0, 'bottom_half': 0, 'bottom_five': 0, 'teams': []}}

    for item in data:



def bake_data_for_each_team(match_reports):
    teams = get_all_teams()
    for team in teams:
        matches_by_height = divide_matches_by_height(team, match_reports)
        wins_by_height = divide_wins_by_height(team, match_reports)
        draws_by_height = divide_draws_by_height(team, match_reports)
        losses_by_height = divide_losses_by_height(team, match_reports)



if __name__ == '__main__':
    reports = load_as_json('data.json')['reports']
    does_height_affect_results(reports)
    print divide_matches_by_height("Arsenal", reports)
    print divide_wins_by_height('Arsenal', reports)
    print divide_draws_by_height('Arsenal', reports)
    print divide_losses_by_height('Arsenal', reports)
