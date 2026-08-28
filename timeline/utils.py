from django.contrib.auth.models import User
from .models import Article
from django.contrib.auth.decorators import login_required


def add_viewers(user, article_id):
  article = Article.objects.get(pk=article_id)
  article.views.add(user)
