from django.conf.urls import url

from views import MagicCardView


urlpatterns = [
    url(r'^magic-cards$', MagicCardView.as_view())
]
