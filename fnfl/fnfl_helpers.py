"""Helper functions"""

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
    lineup_weeks = []

    # Get already created lineups so user can't create duplicates
    for used_lineup in lineups:
        lineup_weeks.append(used_lineup.week)

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


def _get_position_count(lineup):
    """Get a count of all positions in lineup"""

    qb_count = 0
    rb_count = 0
    wr_count = 0
    te_count = 0
    k_count = 0
    players = Player.objects.filter(lineup=lineup)

    for player in players:
        if player.position == "QB":
            qb_count += 1
        if player.position == "RB":
            rb_count += 1
        if player.position == "WR":
            wr_count += 1
        if player.position == "TE":
            te_count += 1
        if player.position == "K":
            k_count += 1

    return qb_count, rb_count, wr_count, te_count, k_count


def is_position_full(request, lineup, player, edit=False):
    """Prevent user from adding too many of one position"""

    qb_count, rb_count, wr_count, te_count, k_count = _get_position_count(lineup)

    if player.position == "QB":
        if edit:
            qb_count -= 1
        if qb_count == 1:
            messages.error(request, "You already have a QB in this lineup. \
                                     Select another position!")
            return True

    if player.position == "RB":
        if edit:
            rb_count -= 1
        if rb_count == 2:
            messages.error(request, "You already have two RBs in this lineup. \
                                     Select another position!")
            return True

    if player.position == "WR":
        if edit:
            wr_count -= 1
        if wr_count == 2:
            messages.error(request, "You already have two WRs in this lineup. \
                                     Select another position!")
            return True

    if player.position == "TE":
        if edit:
            te_count -= 1
        if te_count == 1:
            messages.error(request, "You already have a TE in this lineup. \
                                     Select another position!")
            return True

    if player.position == "K":
        if edit:
            k_count -= 1
        if k_count == 1:
            messages.error(request, "You already have a K in this lineup. \
                                     Select another position!")
            return True

    return False


def is_prev_week_player(request, lineup, player):
    """Return True if player was used in previous week"""

    # Players can be repeated starting in the playoffs
    if is_playoffs(lineup):
        return False

    prev_week = LINEUP_ORDER[LINEUP_ORDER.index(lineup.week)-1]

    try:
        prev_lineup = Lineup.objects.get(week=prev_week)
        players = Player.objects.filter(lineup=prev_lineup)
        player_tup = (player.position, player.name, player.team)
        for prev_player in players:
            prev_player_tup = (prev_player.position,
                               prev_player.name,
                               prev_player.team)
            if player_tup == prev_player_tup:
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
