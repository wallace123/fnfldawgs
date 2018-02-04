"""Helper functions"""

import urllib.request
import xml.etree.ElementTree
import json
from collections import Counter
from django.contrib import messages
from .models import Player, Lineup, Score


LINEUP_ORDER = ['Week 1', 'Week 2', 'Week 3',
                'Week 4', 'Week 5', 'Week 6',
                'Week 7', 'Week 8', 'Week 9',
                'Week 10', 'Week 11', 'Week 12',
                'Week 13', 'Week 14', 'Week 15',
                'Week 16', 'Week 17', 'Wild Card',
                'Divisional Round', 'Conference Championship',
                'Super Bowl']


POSITION_ORDER = ['QB', 'RB', 'WR', 'TE', 'K']


def is_lineup_taken(request, lineup):
    """Check if lineup week has already been used"""

    lineups = Lineup.objects.filter(author=request.user)
    lineup_weeks = [lw.week for lw in lineups]

    if lineup.week in lineup_weeks:
        messages.error(request, "You already have a lineup for that week. \
                                 Select another week!")
        return True
    else:
        return False


def is_playoffs(lineup):
    """Return True if lineup week is a playoff week"""

    return bool(lineup.week in LINEUP_ORDER[17:])


def order_lineups(lineups):
    """Order list of lineups in correct weekly order"""

    ordered_lineups = []

    for item in LINEUP_ORDER:
        for lineup in lineups:
            if item == lineup.week:
                ordered_lineups.append(lineup)

    return ordered_lineups


def order_positions(players):
    """Order list of players in correct position order"""

    ordered_players = []

    for item in POSITION_ORDER:
        for player in players:
            if item == player.position:
                ordered_players.append(player)

    return ordered_players


def is_lineup_full(request, lineup):
    """Prevent user from adding more than 7 players"""

    player_count = Player.objects.filter(lineup=lineup).count()

    if player_count == 7:
        messages.error(request, "You already have 7 players added to this lineup!")
        return True
    else:
        return False


def is_position_full(request, lineup, player, edit=False):
    """Prevent user from adding too many of one position"""

    players = Player.objects.filter(lineup=lineup)
    positions = [pos.position for pos in players]
    position_count = Counter(positions) # Counter returns a dictionary
    max_count = 1
    error_message = "You already have a %s in this lineup. \
                     Select another position!" % player.position

    if player.position in ['RB', 'WR']:
        # Completed lineup should have 2 RBs and WRs
        max_count = 2
        error_message = "You already have two %ss in this lineup. \
                         Select another position!" % player.position

    if player.position in position_count.keys():
        # Fix bug with edit. When user changes player's position.
        if edit:
            position_count[player.position] -= 1
        if position_count[player.position] == max_count:
            messages.error(request, error_message)
            return True

    return False


def is_prev_week_player(request, lineup, player):
    """Return True if player was used in previous week"""

    # Players can be repeated starting in the playoffs
    if is_playoffs(lineup):
        return False

    prev_week = LINEUP_ORDER[LINEUP_ORDER.index(lineup.week)-1]

    try:
        prev_lineup = Lineup.objects.get(week=prev_week, author=request.user)
        players = Player.objects.filter(lineup=prev_lineup)
        cur_player_tup = (player.position, player.name, player.team)
        for prev_player in players:
            prev_player_tup = (prev_player.position,
                               prev_player.name,
                               prev_player.team)
            if cur_player_tup == prev_player_tup:
                messages.error(request, "You used that player last week. \
                                         Select another player!")
                return True
    except Lineup.DoesNotExist:
        return False

    return False


def _get_all_players(request, reg_season):
    """Get all players by user and return list of (position, name, team)"""

    lineups = Lineup.objects.filter(author=request.user)
    p_list = []

    for lineup in lineups:
        # reg_season flag set = Don't get playoff players
        if reg_season:
            if is_playoffs(lineup):
                # Skip adding players that are used in playoffs
                continue

        players = Player.objects.filter(lineup=lineup)
        for player in players:
            p_list.append((player.position, player.name, player.team))

    return p_list


def get_player_count(request, reg_season=False):
    """Get number of times a player has been used in a lineup"""

    p_list = _get_all_players(request, reg_season)
    p_count = Counter(p_list)
    return p_count


def is_player_count_max(request, player):
    """Check if player has reached maximum use for season (4 times)"""

    # Get only regular season players
    # See Issue #6
    p_count = get_player_count(request, True)
    player_tup = (player.position, player.name, player.team)

    if p_count[player_tup] >= 4:
        messages.error(request, "You used that player the max times already. \
                                 Select another player!")
        return True
    else:
        return False


def total_week_score(lineup):
    """Get all player scores for a lineup and total for a week score"""

    player_scores = Score.objects.filter(lineup_to_score=lineup)
    total_score = 0

    for score in player_scores:
        total_score += score.week_score

    return total_score


def get_gid(season, stype, week, team):
    """Gets the GID for getting statsu from nfl.com"""
    req = "http://www.nfl.com/ajax/scorestrip?season=%s&seasonType=%s&week=%s" % (season, stype, week)
    resp = urllib.request.urlopen(req).read()
    resp = str(resp, 'utf-8')

    e = xml.etree.ElementTree.fromstring(resp)
    for games in e.iter('g'):
        if games.attrib['h'] == team or games.attrib['v'] == team:
            return games.attrib['eid']

    return None


def get_json(gid):
    """Gets the json formatted states from nfl.com"""
    req = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (gid, gid)
    resp = urllib.request.urlopen(req).read()
    resp = str(resp, 'utf-8')

    return resp


def get_stats(gid, stats, player):
    """Parses the json stats to populate a player's stats"""
    tds = 0
    pass_yds = 0
    ints = 0
    rush_yds = 0
    rec_yds = 0
    two_pts = 0
    fgs = 0
    xps = 0

    if stats[gid]['away']['abbr'] == player.team:
        field = 'away'
    else:
        field = 'home'

    for key in stats[gid][field]['stats']['kicking'].keys():
        if stats[gid][field]['stats']['kicking'][key]['name'] == player.name:
            fgs = stats[gid][field]['stats']['kicking'][key]['fgm']
            xps = stats[gid][field]['stats']['kicking'][key]['xpmade']

    for key in stats[gid][field]['stats']['passing'].keys():
        if stats[gid][field]['stats']['passing'][key]['name'] == player.name:
            pass_yds += stats[gid][field]['stats']['passing'][key]['yds']
            tds += stats[gid][field]['stats']['passing'][key]['tds']
            ints += stats[gid][field]['stats']['passing'][key]['ints']
            two_pts += stats[gid][field]['stats']['passing'][key]['twoptm']

    for key in stats[gid][field]['stats']['rushing'].keys():
        if stats[gid][field]['stats']['rushing'][key]['name'] == player.name:
            rush_yds += stats[gid][field]['stats']['rushing'][key]['yds']
            tds += stats[gid][field]['stats']['rushing'][key]['tds']
            two_pts += stats[gid][field]['stats']['rushing'][key]['twoptm']

    for key in stats[gid][field]['stats']['receiving'].keys():
        if stats[gid][field]['stats']['receiving'][key]['name'] == player.name:
            rec_yds += stats[gid][field]['stats']['receiving'][key]['yds']
            tds += stats[gid][field]['stats']['receiving'][key]['tds']
            two_pts += stats[gid][field]['stats']['receiving'][key]['twoptm']

    #return stats[gid][field]['stats']
    return tds, pass_yds, ints, rush_yds, rec_yds, two_pts, fgs, xps


def nflcom_week(week):
    """Modifies the week from the DB to an nfl.com week"""
    if week == "Wild Card":
        print("in Wild Card")
        return "18"
    elif week == "Divisional Round":
        return "19"
    elif week == "Conference Championship":
        return "20"
    elif week == "Super Bowl":
        return "21"
    else:
        return week.split()[1]
