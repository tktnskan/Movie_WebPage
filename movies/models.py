from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    actor1 = models.CharField(max_length=30, default='', null=True)
    actor2 = models.CharField(max_length=30, default='', null=True)
    audiAcc = models.IntegerField(default=0, null=True)
    description = models.TextField(default='No Description', null=True)
    director = models.CharField(max_length=30, default='', null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    movieNm = models.CharField(max_length=100, default='', null=True)
    movieNmEn = models.CharField(max_length=100, default='', null=True)
    openDt = models.CharField(max_length=100, default='', null=True)
    posterUrl = models.TextField(default='', null=True)
    videoUrl = models.CharField(max_length=100, default='', null=True)
    sum_score = models.IntegerField(default=0, null=True)
    count_score = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.movieNm}'


class Score(TimeStampedModel):
    review = models.CharField(max_length=1000)
    value = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review[:11]}: {self.value}'

