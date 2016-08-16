from django import template
from datetime import date, timedelta
from league.models import Schedule, Season, Team, Standings
import datetime
from django.db.models import Q




register = template.Library()

@register.simple_tag
def pct(won, matches):
    try:
        win_pct = float(won)/float(matches)
    except:
        win_pct = 0
    return "{}".format("%.3f" % round(float(win_pct),3))

@register.simple_tag
def score_diff(score, score_lost):
    return score-score_lost

@register.simple_tag
def player_age(birth_date):
    age = (date.today() - birth_date) // timedelta(days=365.2425)
    return age


@register.inclusion_tag('content/matches_widget.html')
def matches_widget(team, season = None, past_num=5, future_num=1):
    now = datetime.datetime.now()
    team_pk = Team.objects.get(slug=team).pk
    past = Schedule.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), date__lt=now).order_by('date')
    future = Schedule.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), date__gte=now).order_by('date')      
    if team and season:
        season_pk = Season.objects.get(slug=season).pk
        past = Schedule.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), season=season_pk, date__lt=now).order_by('date')
        future = Schedule.objects.filter(Q(home_team=team_pk) | Q(away_team=team_pk), season=season_pk, date__gte=now).order_by('date')
    
    if future.count() < future_num:
        past_num += abs(future.count() - future_num)
    if past.count() < past_num:
        future_num += abs(past.count() - past_num)   

    return {
        'future_matches': future[:future_num],
        'past_matches': past[:past_num],
        'my_team': team_pk,
    }

@register.inclusion_tag('content/standings_widget.html')
def standings_widget(season):
    season_pk = Season.objects.get(slug=season).pk
    standings = Standings.objects.filter(season=season_pk).order_by('position')

    return {
        'standings': standings,
        'season': season,
    }