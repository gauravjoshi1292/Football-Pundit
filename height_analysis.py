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
            print team, away_team
            if home_team_height < away_team_height:
                matches_by_height['taller']['home'] += 1
                matches_by_height['taller']['at_home_against'].append(away_team)
            else:
                matches_by_height['shorter']['home'] += 1
                matches_by_height['shorter']['at_home_against'].append(away_team)

        elif away_team == team:
            print home_team, team
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


def get_home_away_info(data, league_table):
    info = {'home': {'top_five': 0, 'top_half': 0, 'bottom_half': 0, 'bottom_five': 0, 'teams': []},
            'away': {'top_five': 0, 'top_half': 0, 'bottom_half': 0, 'bottom_five': 0, 'teams': []}}

    for team in data['at_home_against']:
        pos = league_table[team]['pos']
        info['home']['teams'].append(team)
        if pos <= 5:
            info['home']['top_five'] += 1
            info['home']['top_half'] += 1
        elif pos > 5 and pos <= 10:
            info['home']['top_half'] += 1
        elif pos > 10 and pos <= 15:
            info['home']['top_half'] += 1
        elif pos > 15 and pos <= 20:
            info['home']['bottom_five'] += 1
            info['home']['bottom_half'] += 1

    for team in data['at_away_against']:
        pos = league_table[team]['pos']
        info['away']['teams'].append(team)
        if pos <= 5:
            info['away']['top_five'] += 1
            info['away']['top_half'] += 1
        elif pos > 5 and pos <= 10:
            info['away']['top_half'] += 1
        elif pos > 10 and pos <= 15:
            info['away']['top_half'] += 1
        elif pos > 15 and pos <= 20:
            info['away']['bottom_five'] += 1
            info['away']['bottom_half'] += 1

    return info


def bake_data(data, league_table):
    baked_data = {'taller': {}, 'shorter': {}}
    shorter_info = data['shorter']
    taller_info = data['taller']

    baked_data['shorter'] = get_home_away_info(shorter_info, league_table)
    baked_data['taller'] = get_home_away_info(taller_info, league_table)

    return baked_data


def bake_data_for_all_teams(match_reports, league_table):
    baked_data = {}

    teams = get_all_teams()
    for team in teams:
        team_data = {'matches': {}, 'wins': {}, 'draws': {}, 'losses': {}}

        matches_by_height = divide_matches_by_height(team, match_reports)
        print team, matches_by_height
        team_data['matches'] = bake_data(matches_by_height, league_table)

        wins_by_height = divide_wins_by_height(team, match_reports)
        team_data['wins'] = bake_data(wins_by_height, league_table)

        draws_by_height = divide_draws_by_height(team, match_reports)
        team_data['draws'] = bake_data(draws_by_height, league_table)

        losses_by_height = divide_losses_by_height(team, match_reports)
        team_data['losses'] = bake_data(losses_by_height, league_table)

        baked_data[team] = team_data

    return baked_data


def check_reports(reports):
    a = list()
    for r in reports:
        if (r['home_team'], r['away_team']) in a:
            print r['home_team'], r['away_team'], r['date']
        else:
            a.append((r['home_team'], r['away_team']))


if __name__ == '__main__':
    reports = load_as_json('data.json')['reports']
    check_reports(reports)
    # divide_matches_by_height('Arsenal', reports)
    # league_table = load_as_json('league_table.json')
    # baked_data = bake_data_for_all_teams(reports, league_table)
    # print baked_data['Arsenal']['matches']
    # print baked_data['Arsenal']['wins']
    # print baked_data['Arsenal']['draws']
    # print baked_data['Arsenal']['losses']
