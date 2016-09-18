from django import forms

from .models import Player, Lineup, Score

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = (
            'name',
            'position',
            'team',
        )

class LineupForm(forms.ModelForm):
    class Meta:
        model = Lineup
        fields = (
            'week', 
        )

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = (
            'tds',
            'pass_yds',
            'ints',
            'rush_yds',
            'rec_yds',
            'two_pts',
            'fgs',
            'xps',
        )
