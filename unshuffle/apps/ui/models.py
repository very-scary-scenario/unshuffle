import datetime
from random import choice
from string import ascii_lowercase

from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class RoomQuerySet(models.QuerySet):
    def recently_active(self):
        return self.filter(last_active__gt=now() - datetime.timedelta(days=1))


class Room(models.Model):
    code = models.SlugField(db_index=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = models.Manager.from_queryset(RoomQuerySet)()

    def get_absolute_url(self):
        return reverse('room', kwargs={'code': self.code})

    @classmethod
    def create_new(cls):
        for attempt in range(20):
            random_string = ''.join(
                (choice(ascii_lowercase) for i in range(4))
            )
            # probably want to reject slurs and swears and stuff
            if not Room.objects.all().recently_active().filter(
                    code=random_string).exists():
                return Room.objects.create(code=random_string)

        raise RuntimeError('could not find a free room code')


class Game(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    state = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'updated_at'
