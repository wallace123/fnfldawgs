"""Register classes in models.py for view in <url>/admin"""

from django.contrib import admin
from .models import Player, Lineup, Score

admin.site.register(Player)
admin.site.register(Lineup)
admin.site.register(Score)
