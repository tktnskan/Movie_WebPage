from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('sort_movie/<str:condition>/', views.sort_movie, name='sort_movie'),
    path('all_movies/', views.all_movies, name='all_movie'),
    path('<int:movie_id>/scores/', views.get_score, name='get_score'),
    path('<int:movie_id>/scores/new/', views.score_new, name='score_new'),
    path('<int:movie_id>/scores/<int:score_id>/edit/', views.edit_score, name='edit_score'),
    path('<int:movie_id>/scores/<int:score_id>/delete/', views.delete_score, name='delete_score'),
    path('<int:movie_id>/video/', views.video, name='video'),
    path('<int:movie_id>/video/detail/', views.video_detail, name='video_detail'),
]
