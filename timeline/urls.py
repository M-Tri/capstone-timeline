from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('specific/opinions/', views.display_specific_opinions, name="specific_opinions"),
    path('all/opinions/', views.display_all_opinions, name="all_opinions"),
    path('create/post/', views.create_post, name="create_post"),
    path('create/opinion/', views.create_opinion, name="create_opinion"),
    path('random/post/', views.random_post, name="random_post"),
    path('report/opinion/<str:opinion_id>/', views.report_opinion, name="report_opinion"),
    path('reported/opinions/', views.reported_opinions, name="reported_opinions"),
    path('delete/opinion/<str:opinion_id>/', views.delete_opinion, name="delete_opinion"),
]