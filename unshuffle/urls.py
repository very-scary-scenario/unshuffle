from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('unshuffle.apps.ui.urls')),
]
