"""Helper functions"""

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
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
    """Get previous week players so user can't repeat use"""

    prev_week = LINEUP_ORDER[LINEUP_ORDER.index(lineup.week)-1]

    # Players can be repeated in the playoffs
    if prev_week in LINEUP_ORDER[16:]:
        return False

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
