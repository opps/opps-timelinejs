from django.conf.urls import patterns, url
from .views import TimelineView

urlpatterns = patterns(
    '',
    url(
        r'^(?P<pk>\d+)/$',
        TimelineView.as_view(),
        name='timelineview'
    )
)
