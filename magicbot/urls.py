from django.conf.urls import url
from django.views.generic.base import RedirectView

from views import MagicCardView, WelcomeView


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^$', WelcomeView.as_view(), name='welcome'),
    url(r'^magic-cards$', MagicCardView.as_view(), name='magic-cards')
]
