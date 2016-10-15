from django.core.urlresolvers import reverse
from django.db import models


class Game(models.Model):
    name = models.SlugField(db_index=True)
    state = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('game', kwargs={'name': self.name})
