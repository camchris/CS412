from .models import Voter
from django.views.generic import ListView, DetailView
from .forms import VoterFilterForm
from django.db.models import Q
import plotly.express as px
import plotly
import plotly.graph_objs as go

# Create your views here.
class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/show_all_voters.html'
    context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            # party
            if form.cleaned_data.get('party'):
                queryset = queryset.filter(party=form.cleaned_data['party'])

            # dob range
            if form.cleaned_data.get('min_dob'):
                queryset = queryset.filter(birth_date__gte=form.cleaned_data['min_dob'])

            if form.cleaned_data.get('max_dob'):
                queryset = queryset.filter(birth_date__lte=form.cleaned_data['max_dob']) 

            # voter score
            if form.cleaned_data.get('voter_score'):
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])


            # elections
            if form.cleaned_data.get('elections'):
                elections = form.cleaned_data['elections']
                election_filters = Q()
                for election in elections:
                    election_filters |= Q(**{f"{election}": "TRUE"})
                queryset = queryset.filter(election_filters)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context
    

class VoterDetailView(DetailView):
    template_name = 'voter_analytics/show_voter.html'
    model = Voter
    context_object_name = 'v'


class GraphsListView(ListView):
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = "v" 

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)

        if form.is_valid():
            # party
            if form.cleaned_data.get('party'):
                queryset = queryset.filter(party=form.cleaned_data['party'])

            # dob range
            if form.cleaned_data.get('min_dob'):
                queryset = queryset.filter(birth_date__gte=form.cleaned_data['min_dob'])

            if form.cleaned_data.get('max_dob'):
                queryset = queryset.filter(birth_date__lte=form.cleaned_data['max_dob']) 

            # voter score
            if form.cleaned_data.get('voter_score'):
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])


            # elections
            if form.cleaned_data.get('elections'):
                elections = form.cleaned_data['elections']
                election_filters = Q()
                for election in elections:
                    election_filters |= Q(**{f"{election}": "TRUE"})
                queryset = queryset.filter(election_filters)
        return queryset

    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        voters = self.get_queryset()

        # histogram
        birth_years = sorted([int(voter.birth_date.split('-')[0]) for voter in voters if voter.birth_date])
        birth_year_histogram = px.histogram(
            x=birth_years,
            title="Birth Year Distribution",
            labels={"x": "Birth Year"}
        )
        birth_year_histogram_div = birth_year_histogram.to_html()

        # pie chart
        parties = [voter.party for voter in voters if voter.party]
        fig = go.Pie(labels=list(set(parties)), values=[parties.count(party) for party in set(parties)]) 
        title_text = f"Party Affiliation"
        party_pie_div = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        # election participation bar graph
        elections = {
            '2020 State': sum(1 for voter in voters if voter.v20state == "TRUE"),
            '2021 Town': sum(1 for voter in voters if voter.v21town == "TRUE"),
            '2021 Primary': sum(1 for voter in voters if voter.v21primary == "TRUE"),
            '2022 General': sum(1 for voter in voters if voter.v22general == "TRUE"),
            '2023 Town': sum(1 for voter in voters if voter.v23town == "TRUE"),
        }
        election_bar = px.bar(x=list(elections.keys()), y=list(elections.values()), title="Participation in Elections", labels={"x": "Election", "y": "Number of Votes"})
        election_bar_div = election_bar.to_html()

        context['birth_year_histogram'] = birth_year_histogram_div
        context['party_pie'] = party_pie_div
        context['election_bar'] = election_bar_div

        return context
