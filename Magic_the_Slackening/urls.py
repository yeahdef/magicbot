from django.conf.urls import patterns, url

from views import SlackMagicCardView


urlpatterns = patterns('',
    url(r'^magicslack/', SlackMagicCardView.as_view()),
)
