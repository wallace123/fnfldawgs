"""Forms for adding Player, Lineup, and Score"""

from django import forms

from .models import Player, Lineup, Score

class PlayerForm(forms.ModelForm):
    """Add Player form"""

    class Meta:
        model = Player
        fields = (
            'name',
            'position',
            'team',
        )

class LineupForm(forms.ModelForm):
    """Add Lineup form"""

    class Meta:
        model = Lineup
        fields = (
            'week',
        )

class ScoreForm(forms.ModelForm):
    """Add Score form"""

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
