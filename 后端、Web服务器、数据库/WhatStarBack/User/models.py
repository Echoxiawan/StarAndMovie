from django.db import models

class Star(models.Model):
    starname = models.CharField('star', max_length=10, primary_key=True)
    moviename = models.CharField('movie', max_length=20, default="",)
    movieurl = models.CharField('movieurl', max_length=100, default="",)
    description = models.TextField()

class User(models.Model):
    username = models.CharField('username', max_length=20, default="",)
    userpic = models.CharField('userpic', max_length=250, default="")
    starname = models.ForeignKey(Star, on_delete=models.CASCADE)
    starpic = models.CharField('starpic', max_length=250, default="",)
    similarity = models.CharField(max_length=10, default="")
