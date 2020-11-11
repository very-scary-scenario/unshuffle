from django.conf.urls import url

from .views import StartGameView, GameStateView, GameView


urlpatterns = [
    url(r'^$', StartGameView.as_view(), name='index'),
    url(r'^(?P<code>[^/.]+)\.json/$', GameStateView.as_view(),
        name='room-state'),
    url(r'^(?P<code>[^/]+)/$', GameView.as_view(), name='room'),
]
