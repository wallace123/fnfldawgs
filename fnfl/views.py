from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Player, Lineup, Score
from .forms import PlayerForm, LineupForm, ScoreForm
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'fnfl/welcome.html', {})

@login_required
def lineup_list(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'fnfl/lineup_list.html', {'lineups': lineups})

@login_required
def lineup_detail(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    return render(request, 'fnfl/lineup_detail.html', {'lineup': lineup})

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
def add_player(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.lineup = lineup
            player.save()
            return redirect('fnfl.views.lineup_detail', pk=lineup.pk)
    else:
        form = PlayerForm()
    return render(request, 'fnfl/add_player.html', {'form': form})

@login_required
def add_score(request, pk, player_pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    player = get_object_or_404(Player, pk=player_pk)
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.lineup_to_score = lineup
            score.player_to_score = player
            score.save()
            return redirect('fnfl.views.lineup_detail', pk=lineup.pk)
    else:
        form = ScoreForm()
    return render(request, 'fnfl/add_score.html', {'form': form})

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
def lineup_draft_list(request):
    lineups = Lineup.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'fnfl/lineup_draft_list.html', {'lineups': lineups})

@login_required
def lineup_publish(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.publish()
    return redirect('fnfl.views.lineup_detail', pk=pk)

@login_required
def lineup_remove(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    lineup.delete()
    return redirect('fnfl.views.lineup_list')
