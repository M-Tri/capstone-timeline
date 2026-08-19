from .forms import PostNews, PostOpinion
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Article, Image, Supervise


def index(request):
    article = Article.objects.all().order_by('-post_creation_time').first()
    return render(request, 'timeline/index.html', {
        'article': article,
    })

def opinions(request):
    return render(request, "timeline/opinions.html")

def create_post(request):
    if request.method == 'POST':
        form = PostNews(request.POST)
        
        if form.is_valid():
            form_data = form.cleaned_data
            
            new_post = Article(
                editor = request.user,
                title=form_data['title'],
                author_name=form_data['author_name'],
                content=form_data['content'],
                popularity=form_data['popularity'],
                url_source=form_data['url_source']
            )
            main_image.save()
            
            if form_data['url_field_2']:
                image_2 = Image(
                    article=new_post,
                    url=form_data['url_field_2'],
                    is_main_image=False
                )
                image_2.save()
            
            if form_data['url_field_3']:
                image_3 = Image(
                    article=new_post,
                    url=form_data['url_field_3'],
                    is_main_image=False
                )
                image_3.save()

            return redirect(reverse('index'))
    else:
        form = PostNews()
    
    return render(request, 'timeline/create_post.html', {'form': form})

# Extract info from form and create an opinion.
# After : Connect opinions to related button opiniono in post
def create_opinion(request):
    if request.method == 'POST':
        form = PostOpinion(request.POST)
        
        if form.is_valid():
            form_data = form.cleaned_data
            
            article_id = form_data['article_id']
            related_article = Article.objects.get(article_id)

            new_opinion = Opinion(
                writer=request.user,
                title=form_data['title'],
                author_name=form_data['author_name'],
                content=form_data['content'],
                popularity=form_data['popularity'],
                url_source=form_data['url_source']
            )

            return redirect(reverse('index'))
    else:
        form = PostOpinion()
        
    return render(request, 'timeline/create_opinion.html', {'form': form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "timeline/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "timeline/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "timeline/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "timeline/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "timeline/register.html")