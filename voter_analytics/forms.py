from .models import Voter
from datetime import date
from django import forms

class VoterFilterForm(forms.Form):
    # party filter
    PARTY_CHOICES = [(party, party) for party in Voter.objects.values_list('party', flat=True).distinct()]
    party = forms.ChoiceField(choices=[('', 'All')] + PARTY_CHOICES, required=False, label="Party Affiliation")

     # min dob filter
    min_dob = forms.ChoiceField(
        choices=[('', 'None')] + [(year, year) for year in range(date.today().year, 1900, -1)],
        required=False,
        label="Min Birth Year"
    )
    

    # max dob filter
    max_dob = forms.ChoiceField(
        choices=[('', 'None')] + [(year, year) for year in range(date.today().year, 1900, -1)],
        required=False,
        label="Max Birth Year"
    ) 

    # voter score filter
    VOTER_SCORE_CHOICES = [(score, score) for score in Voter.objects.values_list('voter_score', flat=True).distinct()]
    voter_score = forms.ChoiceField(choices=[('', 'All')] + VOTER_SCORE_CHOICES, required=False, label="Voter Score")

    # elections filter
    elections = forms.MultipleChoiceField(
        choices=[
            ('v20state', '2020 State Election'),
            ('v21town', '2021 Town Election'),
            ('v21primary', '2021 Primary Election'),
            ('v22general', '2022 General Election'),
            ('v23town', '2023 Town Election'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Elections"
    )