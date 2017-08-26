"""Views for fnfldawgs site"""

import json
from collections import OrderedDict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Player, Lineup, Score
from .forms import PlayerForm, LineupForm, ScoreForm
from .fnfl_helpers import is_lineup_taken, order_lineups, \
      order_positions, is_lineup_full, is_position_full, \
      is_prev_week_player, get_player_count, is_player_count_max, \
      total_week_score, is_playoffs, get_gid, get_json, get_stats, \
      nflcom_week


# Start Page
def welcome(request):
    """Display welcome page"""

    return render(request, 'fnfl/welcome.html', {})


# Lineup Views
@login_required
def lineup_new(request):
    """Display form to create new lineup"""

    if request.method == "POST":
        form = LineupForm(request.POST)
        if form.is_valid():
            lineup = form.save(commit=False)

            if is_lineup_taken(request, lineup):
                return render(request, 'fnfl/lineup_new.html', {'form': form})

            lineup.author = request.user
            lineup.save()
            messages.success(request, "New Lineup created!")
            return redirect('lineup_detail', lineup_pk=lineup.pk)
    else:
        form = LineupForm()

    return render(request, 'fnfl/lineup_new.html', {'form': form})


@login_required
def lineup_list(request):
    """Display lineups"""

    lineups_players_score = OrderedDict()
    lineups = Lineup.objects.filter(created_date__lte=timezone.now(),
                                    author=request.user)
    ordered_lineups = order_lineups(lineups)
    p_count = get_player_count(request)

    for lineup in ordered_lineups:
        ordered_players = order_positions(Player.objects.filter(lineup=lineup))

        player_count = []
        for player in ordered_players:
            item = (player, p_count[(player.position, player.name, player.team)])
            player_count.append(item)

        week_score = total_week_score(lineup)

        # lineups_players_score is a dictionary
        # Dictionary key = lineup
        # Dictionary values are a list.
        # list[0] = the ordered players list with count of times used
        # list[1] = the weekly score
        lineups_players_score[lineup] = [player_count, week_score]

    return render(request, 'fnfl/lineup_list.html',
                  {'lineups_players_score': lineups_players_score}
                 )


@login_required
def lineup_edit(request, lineup_pk):
    """Edit lineup"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    if request.method == "POST":
        form = LineupForm(request.POST, instance=lineup)
        if form.is_valid():
            lineup = form.save(commit=False)

            if is_lineup_taken(request, lineup):
                return render(request, 'fnfl/lineup_new.html', {'form': form})

            lineup.author = request.user
            lineup.save()
            messages.success(request, "Lineup changed!")
            return redirect('lineup_detail', lineup_pk=lineup.pk)
    else:
        form = LineupForm(instance=lineup)

    return render(request, 'fnfl/lineup_edit.html', {'form': form})


@login_required
def lineup_detail(request, lineup_pk):
    """Display lineup positions and score for each player and the week total"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    ordered_players = order_positions(Player.objects.filter(lineup=lineup))
    players_scores = []
    no_score = 0

    for player in ordered_players:
        try:
            score = Score.objects.get(lineup_to_score=lineup,
                                      player_to_score=player)
            # List of tuples (player, score)
            players_scores.append((player, score.week_score))
        except Score.DoesNotExist:
            players_scores.append((player, no_score))

    week_score = total_week_score(lineup)

    return render(request, 'fnfl/lineup_detail.html',
                  {'lineup': lineup,
                   'week_score': week_score,
                   'players_scores': players_scores}
                 )


@login_required
def lineup_remove(request, lineup_pk):
    """Remove lineup"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    lineup.delete()
    messages.success(request, "Lineup deleted!")
    return redirect('lineup_list')


# Player Views
@login_required
def add_player(request, lineup_pk):
    """Add new player"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)

    if is_lineup_full(request, lineup):
        return redirect('lineup_detail', lineup_pk=lineup.pk)

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)

            if is_position_full(request, lineup, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            if is_prev_week_player(request, lineup, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            if is_player_count_max(request, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            player.lineup = lineup
            player.save()
            messages.success(request, "Player added!")
            return redirect('lineup_detail', lineup_pk=lineup.pk)
    else:
        form = PlayerForm(initial={"name": "C.Palmer"})

    return render(request, 'fnfl/add_player.html', {'form': form})


@login_required
def edit_player(request, lineup_pk, player_pk):
    """Edit created player"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    player = get_object_or_404(Player, pk=player_pk)

    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save(commit=False)

            if is_position_full(request, lineup, player, edit=True):
                return render(request, 'fnfl/edit_player.html', {'form': form})

            if is_prev_week_player(request, lineup, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            if is_player_count_max(request, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            player.lineup = lineup
            player.save()
            messages.success(request, "Player modified!")
            return redirect('lineup_detail', lineup_pk=lineup.pk)
    else:
        form = PlayerForm(instance=player)

    return render(request, 'fnfl/edit_player.html', {'form': form})


@login_required
def remove_player(request, player_pk):
    """Remove created player"""

    player = get_object_or_404(Player, pk=player_pk)
    lineup = player.lineup
    player.delete()
    messages.success(request, "Player removed from lineup!")
    return redirect('lineup_detail', lineup_pk=lineup.pk)


# Score Views
@login_required
def add_score(request, lineup_pk, player_pk):
    """Add stats to player to calculate score"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    player = get_object_or_404(Player, pk=player_pk)

    try:
        week = nflcom_week(lineup.week)
        gid = get_gid("2017", "REG", week, player.team)
        #print(gid)
        stats = json.loads(get_json(gid))
        tds, pass_yds, ints, rush_yds, rec_yds, two_pts, fgs, xps = get_stats(gid, stats, player)
        #print(tds, pass_yds, ints, rush_yds, rec_yds, two_pts, fgs, xps)
    except:
        tds, pass_yds, ints, rush_yds, rec_yds, two_pts, fgs, xps = 0, 0, 0, 0, 0, 0, 0, 0

    try:
        score = Score.objects.get(lineup_to_score=lineup, player_to_score=player)

        # If we're here then a score already exists for this player
        messages.warning(request, "Score already added. Choose Edit Score!")
        return redirect('lineup_detail', lineup_pk=lineup.pk)
    except Score.DoesNotExist:
        if request.method == "POST":
            form = ScoreForm(request.POST)
            if form.is_valid():
                score = form.save(commit=False)
                score.lineup_to_score = lineup
                score.player_to_score = player
                score.save()
                messages.success(request, "Added score to player!")
                return redirect('lineup_detail', lineup_pk=lineup.pk)
        else:
            form = ScoreForm(initial={"tds": tds,
                                      "pass_yds": pass_yds,
                                      "ints": ints,
                                      "rush_yds": rush_yds,
                                      "rec_yds": rec_yds,
                                      "two_pts": two_pts,
                                      "fgs": fgs,
                                      "xps": xps,
                                      }) 

    return render(request, 'fnfl/add_score.html', {'form': form})


@login_required
def edit_score(request, lineup_pk, player_pk):
    """Edit stats of player to recalculate score"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    player = get_object_or_404(Player, pk=player_pk)

    try:
        score = Score.objects.get(lineup_to_score=lineup, player_to_score=player)

        # If we're here then a score is available to edit
        if request.method == "POST":
            form = ScoreForm(request.POST, instance=score)
            if form.is_valid():
                score = form.save(commit=False)
                score.lineup_to_score = lineup
                score.player_to_score = player
                score.save()
                messages.success(request, "Edited score of player!")
                return redirect('lineup_detail', lineup_pk=lineup.pk)
        else:
            form = ScoreForm(instance=score)

        return render(request, 'fnfl/edit_score.html', {'form': form})
    except Score.DoesNotExist:
        messages.warning(request, "No score available to edit. Choose Add Score!")
        return redirect('lineup_detail', lineup_pk=lineup.pk)


@login_required
def raw_scores(request):
    """Cumulative score for all positions"""

    lineups = Lineup.objects.filter(created_date__lte=timezone.now(),
                                    author=request.user)
    raw_score_dict = {'QB': 0, 'RB': 0, 'WR': 0, 'TE': 0, 'K': 0, 'RAW_POINTS': 0}

    for lineup in lineups:
        if is_playoffs(lineup):
            # Only score regular season
            continue

        players = Player.objects.filter(lineup=lineup)

        for player in players:
            try:
                score = Score.objects.get(lineup_to_score=lineup, player_to_score=player)
                if player.position == 'QB':
                    raw_score_dict['QB'] += score.week_score
                elif player.position == 'RB':
                    raw_score_dict['RB'] += score.week_score
                elif player.position == 'WR':
                    raw_score_dict['WR'] += score.week_score
                elif player.position == 'TE':
                    raw_score_dict['TE'] += score.week_score
                elif player.position == 'K':
                    raw_score_dict['K'] += score.week_score
            except Score.DoesNotExist:
                pass

        raw_score_dict['RAW_POINTS'] += total_week_score(lineup)

    return render(request, 'fnfl/raw_scores.html',
                  {'raw_score_dict': raw_score_dict}
                 )

# Count Views
@login_required
def player_usage(request):
    """Show how many times a player has been used"""

    p_count = get_player_count(request)
    player_count_list = []

    for player in p_count:
        player_count_list.append((p_count[player], ' '.join(player)))

    player_count_list.sort(key=lambda tup: tup[0], reverse=True)

    return render(request, 'fnfl/player_count.html', {'player_count_list': player_count_list})