from .utils import add_viewers
from django.contrib.auth.decorators import login_required
from .models import User, Article, Image, Opinion, Quiz
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
    if article and request.user.is_authenticated:
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
    if article and request.user.is_authenticated:
        add_viewers(request.user, article.id)
    return render(request, 'timeline/index.html', {
        'article': article,
    })


@login_required(login_url='login')    
def create_post(request):
    if not request.user.is_editor:
        raise PermissionDenied
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

@login_required(login_url='login') 
def reported_opinions(request):
    if not request.user.is_editor:
        raise PermissionDenied
    reported_opinions = [] 
    for opinion in Opinion.objects.all():
        num_reports = opinion.reporter.count()
        if (num_reports > 0):
            reported_opinions.append(opinion)
    print(reported_opinions)
    return render(request, 'timeline/reported_opinions.html',  {
        'reported_opinions' : reported_opinions,
    })

@login_required(login_url='login') 
def delete_opinion(request, opinion_id):
    if not request.user.is_editor:
        raise PermissionDenied
    # Delete the opinion from the database
    opinion = Opinion.objects.get(id=opinion_id)
    opinion.delete()

    return JsonResponse({'status': 'ok'})

@login_required(login_url='login') 
def keep_opinion(request, opinion_id):
    if not request.user.is_editor:
        raise PermissionDenied
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


def game(request):
    quiz = Quiz.objects.order_by('?').first()
    return render(request, "timeline/game.html", {
        "quiz" : quiz,
    })


def get_quiz_api(request):
    quiz = Quiz.objects.order_by('?').first()
    return JsonResponse({
        'id': quiz.id,
        'question': quiz.question,
        'answer': quiz.answer
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        mypassword = request.POST["mypassword"]
        user = authenticate(request, username=username, password=mypassword)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "timeline/login.html", {
            "message": "Invalid username and/or password."
            })
    else:
        return render(request, "timeline/login.html")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        mypassword = request.POST["mypassword"]
        myconfirmation = request.POST["myconfirmation"]
        if mypassword != myconfirmation:
            return render(request, "timeline/register.html", {
            "message": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "timeline/register.html", {
            "message": "Username already exists."
            })
        user = User.objects.create_user(username, password=mypassword)
        user.save()
        login(request, user)
        return redirect("index")
    else:
        return render(request, "timeline/register.html")