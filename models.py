from django.db import models
from django.utils.translation import ugettext_lazy as _
from smart_selects.db_fields import ChainedManyToManyField, ChainedForeignKey, GroupedForeignKey
from django.utils.timezone import now


STANDINGS_ORDER_HUMAN = (
    (0, _('Points, Wins, Lost, Score Lost')), 
    (1, _('Points, Score, Score Lost')), 
)
STANDINGS_ORDER = (
    (0, ('-points', 'score_lost', '-win', 'lost')), 
    (1, ('-points', '-score', 'score_lost')), 
)

class Team(models.Model):
    name = models.CharField(max_length=200, null=False, verbose_name=_('Team name'))
    short_name = models.CharField(max_length=50, null=False, verbose_name=_('Team short name'))
    slug = models.SlugField(unique=True, null=True, verbose_name=_('Slug'))
    logo = models.ImageField(upload_to='uploads/teams/%Y/%m/%d/', null=True, blank=True, verbose_name=_('Team logo'))
    my_team = models.IntegerField(verbose_name=_('Is this your team?'),
        choices=(
            (0, _('No')),
            (1, _('Yes')),
        ),
        default=0,
    )

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __str__(self):
        return self.short_name

class Season(models.Model):
    name = models.CharField(max_length=200, null=False, verbose_name=_('Name'))
    league = models.CharField(max_length=200, null=True, verbose_name=_('League'))
    slug = models.SlugField(unique=True, null=True, verbose_name=_('Slug'))
    teams = models.ManyToManyField(Team, null=True, blank=True, related_name='teams', verbose_name=_('Teams'))
    standings_order = models.IntegerField(verbose_name=_('Standings order'),
        choices=(STANDINGS_ORDER_HUMAN),
        default=0
    )
    win_points = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Points for win'))
    lost_points = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Points for loss'))
    draw_points = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Points for draw'))

    class Meta:
        verbose_name = _('Season')
        verbose_name_plural = _('Seasons')

    def __str__(self):
        return "{0} {1}".format(self.league, self.name)        
        


class Schedule(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_('Season'))
    week = models.IntegerField(null=False, blank=False, default=1, verbose_name=_('Week'))
    date = models.DateTimeField(default=now, verbose_name=_('Date'))
    home_team = ChainedForeignKey(Team, chained_field='season', chained_model_field='teams', related_name='home_team', verbose_name=_('Home team'))
    away_team = ChainedForeignKey(Team, chained_field='season', chained_model_field='teams', related_name='away_team', verbose_name=_('Away team'))
    home_team_score = models.IntegerField(null=True, blank=True, verbose_name=_('Home team score'))
    away_team_score = models.IntegerField(null=True, blank=True, verbose_name=_('Away team score'))
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

def __str__(self):
        return "{}: {} {}".format(self.week, self.home_team, self.away_team) 



class Standings(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_('Season'))
    team = ChainedForeignKey(Team, chained_field='season', chained_model_field='teams', related_name='team', verbose_name=_('Team'))
    roster_image = models.ImageField(upload_to='uploads/teams/%Y/%m/%d/rosters/', null=True, blank=True, verbose_name=_('Roster image'))
    position = models.IntegerField(null=True, blank=True, default=1, verbose_name=_('Position'))
    matches = models.IntegerField(null=True, blank=True, default=0, verbose_name=_('Matches'))
    win = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Won'))
    lost = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Lost'))
    draws = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Draw'))
    score = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Score'))
    score_lost = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Score lost'))
    points = models.IntegerField(null=True, blank=False, default=0, verbose_name=_('Points'))

    def __str__(self):
        return "{0} {1}".format(self.season, self.team)

    class Meta:
        ordering = STANDINGS_ORDER[0][1]
        unique_together = ('season', 'team')
        verbose_name = _('Table')
        verbose_name_plural = _('Tables')

class Player(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name=_('Season'))
    team = ChainedForeignKey(Team, chained_field='season', chained_model_field='teams', related_name='player_team', on_delete=models.CASCADE, verbose_name=_('Team'))
    name = models.CharField(max_length=200, null=True, verbose_name=_('First name'))
    surename = models.CharField(max_length=200, null=True, verbose_name=_('Last name'))
    jersey = models.IntegerField(null=True, blank=True, verbose_name=_('Jersey number'))
    birth_date = models.DateField(null=True, verbose_name=_('Date of birth'))
    position = models.CharField(max_length=50, null=True, verbose_name=_('Position'))
    weight = models.IntegerField(null=True, blank=False, default=0, help_text=_('Insert weight in kg'), verbose_name=_('Weight'))
    height = models.IntegerField(null=True, blank=False, default=0, help_text=_('Insert height in cm'), verbose_name=_('Height'))
    image = models.ImageField(upload_to='uploads/teams/%Y/%m/%d/players/', null=True, blank=True, verbose_name=_('Player photo'))

    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')

    def __str__(self):
        return "{} {}".format(self.name, self.surename)
    
    
class PlayerCustomFields(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    custom_field_order = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "{}".format(self.name)

# Create your models here.
