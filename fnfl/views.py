from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Lineup
from .forms import LineupForm

def lineup_list(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'fnfl/lineup_list.html', {'lineups': lineups})

def lineup_detail(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    return render(request, 'fnfl/lineup_detail.html', {'lineup': lineup})

def lineup_new(request):
    if request.method == "POST":
        form = LineupForm(request.POST)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.published_date = timezone.now()
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm()
    return render(request, 'fnfl/lineup_edit.html', {'form': form})

def lineup_edit(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    if request.method == "POST":
        form = LineupForm(request.POST, instance=lineup)
        if form.is_valid():
            lineup = form.save(commit=False)
            lineup.author = request.user
            lineup.published_date = timezone.now()
            lineup.save()
            return redirect('lineup_detail', pk=lineup.pk)
    else:
        form = LineupForm(instance=lineup)
    return render(request, 'fnfl/lineup_edit.html', {'form': form})
