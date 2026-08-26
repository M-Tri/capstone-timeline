from .utils import add_viewers
from django.contrib.auth.decorators import login_required
from .models import User, Article, Image, Supervise, Opinion
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



def index(request):
    article = Article.objects.all().order_by('-post_creation_time').first()
    add_viewers(request.user, article.id)
    return render(request, 'timeline/index.html', {
        'article': article,
    })


def display_all_opinions(request):
    opinions = Opinion.objects.all().order_by('-post_creation_time')
    return render(request, "timeline/opinions.html",{
        'opinions': opinions,
    })


def display_specific_opinions(request):
    article_id = request.POST.get("article_id")
    article = Article.objects.get(id=article_id)
    opinions = article.opinions_to_this_article.all().order_by('-post_creation_time')
    return render(request, "timeline/opinions.html",{
        'opinions': opinions,
    })


def random_post(request):
    article = Article.objects.order_by('?').first()
    add_viewers(request.user, article.id)
    return render(request, 'timeline/index.html', {
        'article': article,
    })


@login_required(login_url='login')    
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
            new_post.save()
            
            if form_data['url_field_1']:
                image_1 = Image(
                    article=new_post,
                    url=form_data['url_field_1'],
                    is_main_image=True
                )
                image_1.save()
            
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

            return redirect('index')
        
        # If validation fails 👎
        else:
            print("Form validation error num 1 👎")
        
    else:
        form = PostNews()
        print("Form with 'Get', not 'POST' num 2 👎")
        
    return render(request, 'timeline/create_post.html', {'form': form})


def report_opinion(request, opinion_id):
    if request.method == 'POST':
        opinion = Opinion.objects.get(pk=opinion_id)
        opinion.reporter.add(request.user)
    
    return redirect('all_opinions')


def reported_opinions(request):
    reported_opinions = [] 
    for opinion in Opinion.objects.all():
        num_reports = opinion.reporter.count()
        if (num_reports > 0):
            reported_opinions.append(opinion)
    print(reported_opinions)
    return render(request, 'timeline/reported_opinions.html',  {
        'reported_opinions' : reported_opinions,
    })


def delete_opinion(request, opinion_id):
    # Delete the opinion from the database
    opinion = Opinion.objects.get(id=opinion_id)
    opinion.delete()

    return JsonResponse({'status': 'ok'})


def keep_opinion(request, opinion_id):
    opinion = Opinion.objects.get(id=opinion_id)
    opinion.reporter.clear()

    return JsonResponse({'status': 'ok'})


@login_required(login_url='login')
def create_opinion(request):
    # Rendered for article selection suggestive search
    articles = Article.objects.all()
    
    if request.method == 'POST':
        form = PostOpinion(request.POST)
        
        if form.is_valid():
            form_data = form.cleaned_data

            new_opinion = Opinion(
                writer=request.user,
                title=form_data['title'],
                article=form_data['article'],
                content=form_data['content'],
                bias=form_data['bias'],
            )
            new_opinion.save()
            
            # Create label object connections
            selected_labels = form_data['labels_select']
            new_opinion.labels.set(selected_labels)

            return redirect(reverse('all_opinions'))
    else:
        form = PostOpinion()
      
    return render(request, 'timeline/create_opinion.html', {
        'form': form,
        'articles': articles,
        })


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


@login_required(login_url='login')
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