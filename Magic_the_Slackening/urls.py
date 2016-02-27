from django.conf.urls import patterns, url

from views import MagicCardView


urlpatterns = patterns(
    url(r'^magic-cards/', MagicCardView.as_view()),
)
