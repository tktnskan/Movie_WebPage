from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_http_methods, require_POST
from .models import User
from .forms import UserCustomCreationForm


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('movies:movie_list')
        else:
            error_message = '비밀번호가 일치하지 않습니다'
            user_form = UserCustomCreationForm()
            return render(request, 'accounts/signup.html', {
                'user_form': user_form,
                'error_message': error_message,
            })
    user_form = UserCustomCreationForm()
    return render(request, 'accounts/signup.html', {
        'user_form': user_form,
    })


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'movies:movie_list')
        else:
            error_message1 = '아이디 또는 비밀번호를 다시 확인하세요.'
            error_message2 = '등록되지 않은 아이디거나, 아이디 또는 비밀번호를 잘못 입력하셨습니다.'
            login_form = AuthenticationForm()
            return render(request, 'accounts/login.html', {
                'login_form': login_form,
                'error_message1': error_message1,
                'error_message2': error_message2,
            })
    login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'login_form': login_form,
    })


@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET'])
def user_detail(request, user_name):
    user_info = get_object_or_404(User, username=user_name)
    user_rec = ''
    movie = ''
    movie_id = 0
    value = 0
    for user in user_info.followings.all():
        for i in user.score_set.all():
            if i.value > value:
                value = i.value
                movie = i.movie.movieNm
                movie_id = i.movie.id
                user_rec = user.username
    return render(request, 'accounts/user_detail.html', {
        'user_info': user_info,
        'movie': movie,
        'user_rec': user_rec,
        'value': value,
        'movie_id': movie_id,
    })
# def user_detail(request, user_name):
#     user = get_object_or_404(User, username=user_name)
#     if len(user.score_set.all()) != 0:
#         recent_score = user.score_set.all()[::-1][0]
#         max_score = 0
#         best_score = 0
#         for score in user.score_set.all():
#             if score.value >= max_score:
#                 max_score = score.value
#                 best_score = score
#         context = {
#             'user': user,
#             'recent_score': recent_score,
#             'best_score': best_score,
#         }
#     else:
#         context = {
#             'user': user,
#         }
#     return render(request, 'accounts/user_detail.html', context)


@login_required
@require_POST
def follow_toggle(request, user_name):
    sender = request.user
    receiver = get_object_or_404(User, username=user_name)

    if sender != receiver:
        if receiver in sender.followings.all():
            sender.followings.remove(receiver)
        else:
            sender.followings.add(receiver)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/movie_pjt/'))

