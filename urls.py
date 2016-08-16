from django.conf.urls import url

from .views import StandingsFull, TeamDetails, ScheduleFull, TeamSchedule, TeamRoster

urlpatterns = [
    url(r'^(?P<season>[-\w]+)/standings$', StandingsFull.as_view(), name='standings_full' ),
    url(r'^(?P<season>[-\w]+)/schedule$', ScheduleFull.as_view(), name='schedule_full' ),
    url(r'^(?P<season>[-\w]+)/team/(?P<team>[-\w]+)$', TeamDetails.as_view(), name='team_details' ),
    url(r'^(?P<season>[-\w]+)/team/(?P<team>[-\w]+)/roster$', TeamRoster.as_view(), name='team_roster' ),
    url(r'^(?P<season>[-\w]+)/team/(?P<team>[-\w]+)/schedule$', TeamSchedule.as_view(), name='team_schedule' ),
]