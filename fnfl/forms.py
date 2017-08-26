"""Forms for adding Player, Lineup, and Score"""

from django import forms

from .models import Player, Lineup, Score

class PlayerForm(forms.ModelForm):
    """Add Player form"""

    class Meta:
        model = Player
        fields = (
            'position',
            'team',
            'name',
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
        exclude = ('player_to_score', 'lineup_to_score')
