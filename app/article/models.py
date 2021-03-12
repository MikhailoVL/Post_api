from django.db import models
from django.contrib.auth.models import User

import datetime


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="author", blank=False, default=None)
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=True, default="")
    body = models.TextField(blank=False, default="")
    datetime = models.DateField(
        default=datetime.date.today().strftime('%Y-%m-%d'), blank=False)

    def __str__(self):
        return self.title


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_fan = models.BooleanField(blank=False, default=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING,
                             related_name='post')

    def __str__(self):
        return self.User.email or self.User.first_name , self.post.name
