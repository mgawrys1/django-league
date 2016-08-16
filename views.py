from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, DetailView
from league.models import Schedule, Standings, Season, Player, Team, STANDINGS_ORDER
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _



class StandingsFull(ListView):
    template_name = 'standings.html'
    model = Standings
    context_object_name = 'standings'

    def get_context_data(self, **kwargs):
        context = super(StandingsFull, self).get_context_data(**kwargs)
        
        season_name = ''
        if self.kwargs.get('season'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = ": {} {}".format(season.league, season.name)
        
        context['table_name'] = season_name
        context['slug'] = self.kwargs.get('season')
        
        return context


    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.all()
        if self.kwargs.get('season'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = season.name
            order = STANDINGS_ORDER[season.standings_order][1]
            qs = self.model.objects.filter(season=season_pk).order_by(*order)
        return qs


class TeamDetails(DetailView):
    template_name = 'team.html'
    model = Team
    context_object_name = 'team'
    slug_url_kwarg = 'team'

    def get_context_data(self, **kwargs):
        context = super(TeamDetails, self).get_context_data(**kwargs)
        if self.kwargs.get('season') and self.kwargs.get('team'):
            season_pk = Season.objects.get(slug=self.kwargs['season']).pk
            team_pk = self.model.objects.get(slug=self.kwargs.get('team')).pk
            team = Standings.objects.get(season=season_pk, team=team_pk)
            roster = Player.objects.filter(season=season_pk, team=team_pk)
            schedule = Schedule.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), season = season_pk ).order_by('date') 
            context['team_more'] = team
            context['team_roster'] = roster
            context['team_schedule'] = schedule
        
        
        return context
    


class ScheduleFull(ListView):
    template_name = 'schedule.html'
    model = Schedule
    context_object_name = 'schedule'

    def get_context_data(self, **kwargs):
        context = super(ScheduleFull, self).get_context_data(**kwargs)
        
        season_name = ''
        if self.kwargs.get('season'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = ": {} {}".format(season.league, season.name)
            context['page_name'] = _('Schedule')
            context['season'] = season
            context['slug'] = self.kwargs.get('season')
        
        return context


    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.all()
        if self.kwargs.get('season'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = season.name
            qs = self.model.objects.filter(season=season_pk).order_by('date')
        return qs


class TeamSchedule(ListView):
    template_name = 'schedule.html'
    model = Schedule
    context_object_name = 'schedule'
     

    def get_context_data(self, **kwargs):
        context = super(TeamSchedule, self).get_context_data(**kwargs)
        context['page_name'] = _('Archiwum')    
        if self.kwargs.get('team'):
            team = Team.objects.get(slug=self.kwargs['team'])
            context['team'] = team
        
        if self.kwargs.get('season'):
            season = Season.objects.get(slug=self.kwargs['season'])
            context['season'] = season
            context['page_name'] = _('Schedule')      
        
        return context


    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.all().order_by('date')
        if self.kwargs.get('team'):
            team_pk = Team.objects.get(slug=self.kwargs.get('team')).pk
            qs = self.model.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk)).order_by('date')
        if self.kwargs.get('season') and self.kwargs.get('team'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = season.name
            team_pk = Team.objects.get(slug=self.kwargs.get('team')).pk
            qs = self.model.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), season = season_pk ).order_by('date')
        return qs



class TeamRoster(ListView):
    template_name = 'roster.html'
    model = Player
    context_object_name = 'roster'

    def get_context_data(self, **kwargs):
        context = super(TeamRoster, self).get_context_data(**kwargs)
        context['page_name'] = _('Roster')    
        if self.kwargs.get('team'):
            team = Team.objects.get(slug=self.kwargs['team'])
            context['team'] = team
        
        if self.kwargs.get('season'):
            team = Team.objects.get(slug=self.kwargs['team'])
            season = Season.objects.get(slug=self.kwargs['season'])
            context['roster_image'] = Standings.objects.get(team = team.pk, season = season.pk).roster_image
            context['season'] = season
        
        return context
    
    def get_queryset(self, *args, **kwargs):
        qs = self.model.objects.all().order_by('jersey')
        if self.kwargs.get('season') and self.kwargs.get('team'):
            season = Season.objects.get(slug=self.kwargs['season'])
            season_pk = season.pk
            season_name = season.name
            team_pk = Team.objects.get(slug=self.kwargs.get('team')).pk
            qs = self.model.objects.filter(team = team_pk, season = season_pk ).order_by('jersey')
        return qs

# Create your views here.
