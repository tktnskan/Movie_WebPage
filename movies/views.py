from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import *
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
import json
from django.contrib.auth import get_user_model
User = get_user_model()

@require_http_methods(['GET'])
@login_required
def movie_list(request):
    return render(request, 'movies/list.html', {
        # 'movies': movie_info,
        # 'test': top_10,
    })


def video(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie = model_to_dict(movie)
    return JsonResponse({
        'movie': movie,
    })


def video_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    print('********done******')
    return render(request, 'movies/test.html', {
        'movie': movie,
    })


def all_movies(request):
    movies = Movie.objects.all()
    movie_set = []
    dic = []
    for movie in movies:
        if movie.count_score:
            avg_score = round(movie.sum_score / movie.count_score, 1)
            a = (movie.movieNm, movie.audiAcc)
            dic.append(a)
        else:
            avg_score = 0.0
            a = (movie.movieNm, movie.audiAcc)
            dic.append(a)
        fields = {
            'id': movie.id,
            'movieNm': movie.movieNm,
            'movieNmEn': movie.movieNmEn,
            'avgScore': avg_score,
            'openDt': int(movie.openDt),
            'genre': movie.genre.name,
            'audiAcc': format(movie.audiAcc, ','),
            'description': movie.description,
            'posterUrl': movie.posterUrl,
            'videoUrl': movie.videoUrl,
        }
        movie_set.append(fields)

    word_list = sorted(dic, key=lambda x: x[1], reverse=True)
    top10 = []
    for i in range(10):
        for movie in movie_set:
            if movie['movieNm'] == word_list[i][0]:
                top10.append(movie)

    return JsonResponse({
        'movie_set': movie_set,
        'top10': top10,
        'userId': request.user.id
    })


def sort_movie(request, condition=''):
    movies = Movie.objects.all()
    movie_set = []
    for movie in movies:
        if condition in movie.movieNm:
            if movie.count_score:
                avg_score = round(movie.sum_score / movie.count_score, 1)
            else:
                avg_score = 0.0

            fields = {
                'id': movie.id,
                'movieNm': movie.movieNm,
                'movieNmEn': movie.movieNmEn,
                'avgScore': avg_score,
                'openDt': int(movie.openDt),
                'genre': movie.genre.name,
                'audiAcc': format(movie.audiAcc, ','),
                'description': movie.description,
                'posterUrl': movie.posterUrl,
                'videoUrl': movie.videoUrl,
            }
            movie_set.append(fields)
    return JsonResponse({
        'movie_set': movie_set
    })


def score_new(request, movie_id):
    if request.method == 'GET':
        return render(request, 'movies/list.html')
    else:
        movie = get_object_or_404(Movie, id=movie_id)
        score = Score()
        data = json.loads(request.body.decode('utf-8'))
        # print(data)

        score.review = data['inputScore']['review']
        score.value = data['inputScore']['value']
        score.movie = movie
        score.user = request.user
        movie.sum_score += int(score.value)
        movie.count_score += 1
        movie.save()
        score.save()
        movie = model_to_dict(movie)
        score = model_to_dict(score)

        # print(movie)
        # print(score)
        return JsonResponse({
            "movie": movie,
            "score": score,
        })


def get_score(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    scores = movie.score_set.all()
    result = []
    for score in scores:
        user = User.objects.get(id=score.user_id)
        score = model_to_dict(score)
        score['username'] = user.username
        result.append(score)
    return JsonResponse({
        "scores": result
    })


def edit_score(request, movie_id, score_id):
    movie = get_object_or_404(Movie, id=movie_id)
    score = get_object_or_404(Score, id=score_id)
    data = json.loads(request.body.decode('utf-8'))
    score.review = data['inputScore']['review']
    movie.sum_score -= int(data['preScore']['value'])
    score.value = data['inputScore']['value']
    movie.sum_score += int(score.value)
    score.save()
    movie.save()
    score = model_to_dict(score)
    return JsonResponse({
        "score": score
    })


def delete_score(request, movie_id, score_id):
    if request.method == 'POST':
        score = Score.objects.get(id=score_id)
        movie = get_object_or_404(Movie, id=movie_id)
        movie.sum_score -= int(score.value)
        movie.count_score -= 1
        movie.save()
        score.delete()
        return JsonResponse({
            "done": True
        })

