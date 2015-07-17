from django.conf.urls import patterns, url

from views import SlackMagicCardView, RootView


urlpatterns = patterns('',
    url(r'^', RootView.as_view()),
    url(r'^magicslack/', SlackMagicCardView.as_view()),
)
