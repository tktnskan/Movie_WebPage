from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user_detail/<str:user_name>/', views.user_detail, name='user_detail'),
    path('follow/<str:user_name>/', views.follow_toggle, name='toggle_follow'),
]