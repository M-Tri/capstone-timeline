from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_editor = models.BooleanField(default=False)
    pass


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    editor = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'edited',
    )
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    popularity = models.CharField(
        max_length=15,
        default='Low',
        )
    url_source = models.URLField(max_length=1000)
    views = models.ManyToManyField(
        User,
        related_name = 'article_viewers',
        blank=True,
        )
    post_creation_time = models.DateTimeField(auto_now_add=True)


class Opinion(models.Model):
    """ Opinion ManyToManyField with model Label """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'opinions_to_this_user',
    )
    # Related article
    article = models.ForeignKey(
        Article,
        on_delete = models.CASCADE,
        related_name= "opinions_to_this_article",
    )

    content = models.CharField(max_length=255)
    post_creation_time = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(
        User,
        related_name = 'opinion_viewers',
        )
    reporter = models.ManyToManyField(
        User,
        related_name = 'reporters_of_this_opinion',
        blank=True,
        )
    bias = models.IntegerField()


class Label(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    opinions = models.ManyToManyField(
        Opinion,
        related_name = 'labels',
        blank=True,
        )
    def __str__(self): 
        return self.name 


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name = 'images',
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=1000)
    is_main_image = models.BooleanField(default=False)


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
