"""Views for fnfldawgs site"""

from collections import Counter, OrderedDict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Player, Lineup, Score
from .forms import PlayerForm, LineupForm, ScoreForm
from .fnfl_helpers import *


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
def lineup_publish(request, lineup_pk):
    """Publish lineup"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    lineup.publish()
    messages.success(request, "Lineup published!")
    return redirect('lineup_detail', lineup_pk=lineup.pk)


@login_required
def lineup_draft_list(request):
    """Display draft lineups"""

    lineups = Lineup.objects.filter(published_date__isnull=True,
                                    author=request.user)
    ordered_lineups = order_lineups(lineups)
    return render(request, 'fnfl/lineup_draft_list.html', {'lineups': ordered_lineups})


@login_required
def lineup_list(request):
    """Display lineups"""

    lineups_players_score = OrderedDict()
    lineups = Lineup.objects.filter(published_date__lte=timezone.now(),
                                    author=request.user)
    ordered_lineups = order_lineups(lineups)

    for lineup in ordered_lineups:
        players = Player.objects.filter(lineup=lineup)
        ordered_players = order_positions(players)
        week_score = total_week_score(request, lineup)

        # for lineups_players_score dictionary
        # Dictionary key = lineup
        # Dictionary values are a list. 
        # list[0] = the ordered players list
        # list[1] = the weekly score
        lineups_players_score[lineup] = [ordered_players, week_score]

    return render(request, 'fnfl/lineup_list.html', {'lineups_players_score': lineups_players_score})


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
    players = Player.objects.filter(lineup=lineup)

    qb_player = ""
    rb1_player = ""
    rb2_player = ""
    wr1_player = ""
    wr2_player = ""
    te_player = ""
    k_player = ""

    qb_score = 0
    rb1_score = 0
    rb2_score = 0
    wr1_score = 0
    wr2_score = 0
    te_score = 0
    k_score = 0

    for player in players:
        if player.position == 'QB':
            qb_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                qb_score = score.week_score
            except Score.DoesNotExist:
                pass

        if player.position == 'RB' and rb1_player == '':
            rb1_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                rb1_score = score.week_score
            except Score.DoesNotExist:
                pass
            continue # Continue here so RB is not displayed twice

        if player.position == 'RB' and rb1_player != '':
            rb2_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                rb2_score = score.week_score
            except Score.DoesNotExist:
                pass

        if player.position == 'WR' and wr1_player == '':
            wr1_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                wr1_score = score.week_score
            except Score.DoesNotExist:
                pass
            continue # Continue here so WR is not displayed twice

        if player.position == 'WR' and wr1_player != '':
            wr2_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                wr2_score = score.week_score
            except Score.DoesNotExist:
                pass

        if player.position == 'TE':
            te_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                te_score = score.week_score
            except Score.DoesNotExist:
                pass

        if player.position == 'K':
            k_player = player
            try:
                score = Score.objects.get(lineup_to_score=lineup,
                                          player_to_score=player)
                k_score = score.week_score
            except Score.DoesNotExist:
                pass

    week_score = total_week_score(request, lineup)

    return render(request, 'fnfl/lineup_detail.html',
                  {'lineup': lineup,
                   'week_score': week_score,
                   'qb': qb_player,
                   'rb1': rb1_player,
                   'rb2': rb2_player,
                   'wr1': wr1_player,
                   'wr2': wr2_player,
                   'te': te_player,
                   'k': k_player,
                   'qb_score': qb_score,
                   'rb1_score': rb1_score,
                   'rb2_score': rb2_score,
                   'wr1_score': wr1_score,
                   'wr2_score': wr2_score,
                   'te_score': te_score,
                   'k_score': k_score,}
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

            if is_player_count_max(request, lineup, player):
                return render(request, 'fnfl/add_player.html', {'form': form})

            player.lineup = lineup
            player.save()
            messages.success(request, "Player added!")
            return redirect('lineup_detail', lineup_pk=lineup.pk)
    else:
        form = PlayerForm()
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

            if is_player_count_max(request, lineup, player):
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
    player.delete()
    messages.success(request, "Player removed from lineup!")
    return redirect('lineup_list')


# Score Views

@login_required
def add_score(request, lineup_pk, player_pk):
    """Add stats to player to calculate score"""

    lineup = get_object_or_404(Lineup, pk=lineup_pk)
    player = get_object_or_404(Player, pk=player_pk)

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
            form = ScoreForm()

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