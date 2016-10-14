from django.db import models


class Game(models.Model):
    name = models.SlugField(db_index=True)
    state = models.TextField()
