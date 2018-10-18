from django.conf.urls import url

from .views import StartGameView, GameView


urlpatterns = [
    url(r'^$', StartGameView.as_view(), name='index'),
    url(r'^(?P<code>[^/]+)/$', GameView.as_view(), name='room'),
]
