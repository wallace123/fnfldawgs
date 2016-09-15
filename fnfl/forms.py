from django import forms

from .models import Player, Lineup, Score

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = (
            'first_name', 
            'last_name',
            'position',
            'team',
        )

class LineupForm(forms.ModelForm):
    class Meta:
        model = Lineup
        fields = (
            'week', 
            'qb_position',
            'qb_first_name',
            'qb_last_name',
            'qb_team',
            'rb1_position',
            'rb1_first_name',
            'rb1_last_name',
            'rb1_team',
            'rb2_position',
            'rb2_first_name',
            'rb2_last_name',
            'rb2_team',
            'wr1_position',
            'wr1_first_name',
            'wr1_last_name',
            'wr1_team',
            'wr2_position',
            'wr2_first_name',
            'wr2_last_name',
            'wr2_team',
            'te_position',
            'te_first_name',
            'te_last_name',
            'te_team',
            'k_position',
            'k_first_name',
            'k_last_name',
            'k_team',
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
            'ret_tds',
            'two_pts',
            'fgs',
            'xps',
        )
