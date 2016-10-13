from django.conf.urls import url

from .views import GameView


urlpatterns = [
    url(r'^game/$', GameView.as_view())
]
