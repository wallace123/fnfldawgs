from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Player, Lineup, Score
from .forms import PlayerForm, LineupForm, ScoreForm
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.contrib import messages

# Start Page
def welcome(request):
    return render(request, 'fnfl/welcome.html', {})


# Lineup Views

@login_required
def lineup_new(request):
    if request.method == "POST":
        form = LineupForm(request.POST)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm()
    return render(request, 'fnfl/lineup_edit.html', {'form': form})


@login_required
def lineup_publish(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.publish()
    return redirect('lineup_detail', pk=pk)


@login_required
def lineup_draft_list(request):
    lineups = Lineup.objects.filter(published_date__isnull=True, author=request.user).order_by('created_date')
    return render(request, 'fnfl/lineup_draft_list.html', {'lineups': lineups})


@login_required
def lineup_list(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now(), author=request.user).order_by('published_date')
    return render(request, 'fnfl/lineup_list.html', {'lineups': lineups})


@login_required
def lineup_edit(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    if request.method == "POST":
        form = LineupForm(request.POST, instance=lineup)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm(instance=lineup)
    return render(request, 'fnfl/lineup_edit.html', {'form': form})


@login_required
def lineup_remove(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.delete()
    return redirect('lineup_list')


@login_required
def lineup_detail(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = Player.objects.filter(lineup=lineup)
    score = Score.objects.filter(lineup_to_score=lineup)

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

    for p in player:
        if p.position == 'QB':
            qb_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                qb_score = s.week_score
            except:
                pass
        if p.position == 'RB' and rb1_player == '':
            rb1_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                rb1_score = s.week_score
            except:
                pass
            continue
        if p.position == 'RB' and rb1_player != '':
            rb2_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                rb2_score = s.week_score
            except:
                pass
        if p.position == 'WR' and wr1_player == '':
            wr1_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                wr1_score = s.week_score
            except:
                pass
            continue
        if p.position == 'WR' and wr1_player != '':
            wr2_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                wr2_score = s.week_score
            except:
                pass
        if p.position == 'TE':
            te_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                te_score = s.week_score
            except:
                pass
        if p.position == 'K':
            k_player = p
            try:
                s = Score.objects.get(lineup_to_score=lineup,
                    player_to_score=p)
                k_score = s.week_score
            except:
                pass

    total_week_score = 0

    for s in score:
        total_week_score += s.week_score

    return render(request, 'fnfl/lineup_detail.html', 
        {'lineup': lineup,
         'total_week_score': total_week_score,
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
def lineup_remove(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.delete()
    return redirect('lineup_list')


# Player Views

@login_required
def add_player(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player_count = Player.objects.filter(lineup=lineup).count()
    if player_count == 7:
        messages.warning(request, "You already have 7 players added to this lineup!")
        return redirect('lineup_detail', pk=lineup.pk)

    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.lineup = lineup
            player.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = PlayerForm()
    return render(request, 'fnfl/add_player.html', {'form': form})


@login_required
def edit_player(request, pk, player_pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = get_object_or_404(Player, pk=player_pk)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            player = form.save(commit=False)
            player.lineup = lineup
            player.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'fnfl/edit_player.html', {'form': form})


@login_required
def remove_player(request, pk, player_pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = get_object_or_404(Player, pk=player_pk)
    player.delete()
    return redirect('lineup_list')


# Score Views

@login_required
def add_score(request, pk, player_pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = get_object_or_404(Player, pk=player_pk)
    try:
        score = Score.objects.get(lineup_to_score=lineup, player_to_score=player)
        if score != '':
            return redirect('lineup_detail', pk=lineup.pk)
    except:
        pass
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.lineup_to_score = lineup
            score.player_to_score = player
            score.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = ScoreForm()
    return render(request, 'fnfl/add_score.html', {'form': form})


@login_required
def edit_score(request, pk, player_pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = get_object_or_404(Player, pk=player_pk)
    try:
        score = Score.objects.get(lineup_to_score=lineup, player_to_score=player)
    except:
        return redirect('lineup_detail', pk=lineup.pk)
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            score = form.save(commit=False)
            score.lineup_to_score = lineup
            score.player_to_score = player
            score.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = ScoreForm(instance=score)
    return render(request, 'fnfl/edit_score.html', {'form': form})


# Count Views

@login_required
def player_usage(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now(), author=request.user).order_by('published_date')
    p = []
    for l in lineups:
        players = Player.objects.filter(lineup=l)
        for player in players:
            p.append((player.position, player.name, player.team))

    player_count_list = []
    p_count = Counter(p)
    for player in p_count:
        player_count_list.append((p_count[player], ' '.join(player)))

    player_count_list.sort(key=lambda tup: tup[0], reverse=True)

    return render(request, 'fnfl/player_count.html', {'player_count_list': player_count_list})


