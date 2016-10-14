from django.conf.urls import url

from .views import GameView


urlpatterns = [
    url(r'^game/(?P<name>[^/]+)/$', GameView.as_view())
]
