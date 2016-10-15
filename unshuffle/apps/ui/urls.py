from django.conf.urls import url

from .views import StartGameView, GameView


urlpatterns = [
    url(r'^$', StartGameView.as_view(), name='index'),
    url(r'^(?P<name>[^/]+)/$', GameView.as_view(), name='game'),
]
