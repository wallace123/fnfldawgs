from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Lineup

def lineup_list(request):
    lineups = Lineup.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'fnfl/lineup_list.html', {'lineups': lineups})

def lineup_detail(request, pk):
    lineup = get_object_or_404(Lineup, pk=pk)
    return render(request, 'fnfl/lineup_detail.html', {'lineup': lineup})
