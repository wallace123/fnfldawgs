from django import forms

from .models import Lineup

class LineupForm(forms.ModelForm):
    class Meta:
        model = Lineup
        fields = ('week', 'qb', 'rb1', 'rb2', 'wr1', 'wr2', 'te', 'k',)
