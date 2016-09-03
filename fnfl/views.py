from django.shortcuts import render

def lineup_list(request):
    return render(request, 'fnfl/lineup_list.html', {})
