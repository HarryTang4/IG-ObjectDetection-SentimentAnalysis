from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.template import loader
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
import json
import requests
from .getinfo import get_images
from .sentimentanalysis import comments_to_analyze
from .objectdetection import image_to_detect
from .instagramapi import load_instance, set_access_token
import math
import numpy as np
import os
import threading
import time
import re
# Create your views here.

json_dir = settings.JSON_ROOT
local_dir = settings.STATIC_ROOT + "/media/cached/"


@login_required
def home(request):

    access_token = get_access_token(request)

    load_instance(access_token)

    with open(json_dir + "basic_profile_info.json") as file:
        basic_profile_info = json.load(file)

    username = basic_profile_info[0]
    name = basic_profile_info[1]
    follower_count = basic_profile_info[2]
    profile_photo_url = basic_profile_info[3]

    request.session['username'] = username
    request.session['name'] = name

    gallery_list = get_images(username, profile_photo_url)

    chunks = [gallery_list[x:x+4]
              for x in range(0, len(gallery_list), 4)]

    list_length = max(map(len, chunks))

    transposed_gallery = []

    for i in range(list_length):
        temp = []
        for list in chunks:
            if i < len(list):
                temp.append(list[i])
        transposed_gallery.append(temp)

    if request.method == 'GET' and 'current_image_id' in request.GET:
        current_image = str(request.GET.get('current_image_id'))
        image_exists = os.path.exists(local_dir + current_image)
        request.session['current_image'] = current_image
        current_image_id = os.path.splitext(current_image)[0]

        request.session['comments'] = comments_to_analyze(current_image_id)

        if current_image and image_exists == False:
            event = threading.Event()

            def image_processing_thread():
                show_loader(request)
                print("loading")
                image_processing(current_image_id)
                event.set()  # Signal that the image processing is finished

            t = threading.Thread(target=image_processing_thread)
            t.start()  # Start the thread

            event.wait()  # Wait until the process is finished
            return redirect(reverse('analytics'))

        else:
            return redirect(reverse('analytics'))

    return render(request, 'index.html', {'name': name,
                                          'username': username,
                                          'follower_count': follower_count,
                                          'gallery_list1': transposed_gallery[0],
                                          'gallery_list2': transposed_gallery[1],
                                          'gallery_list3': transposed_gallery[2],
                                          'gallery_list4': transposed_gallery[3]})


def image_processing(current_image_id):
    image_to_detect(current_image_id)


def analytics(request):
    username = request.session['username']
    current_image = request.session['current_image']
    name = request.session['name']
    comments = request.session['comments']
    print("current image jpg: %s" % current_image)

    if request.method == 'POST':
        selected_comments = request.POST.getlist('comments')
        sentiment_data = {"positive": 0, "neutral": 0, "negative": 0}
        count = 0
        for comment in selected_comments:
            if comment in comments:
                sentiment_data['positive'] += comments[comment]['positive']
                sentiment_data['neutral'] += comments[comment]['neutral']
                sentiment_data['negative'] += comments[comment]['negative']
                count += 1
        if count > 0:
            total = sentiment_data['positive'] + \
                sentiment_data['neutral'] + sentiment_data['negative']
            sentiment_data['positive'] = round(
                (sentiment_data['positive'] / total) * 100, 2)
            sentiment_data['neutral'] = round(
                (sentiment_data['neutral'] / total) * 100, 2)
            sentiment_data['negative'] = round(
                (sentiment_data['negative'] / total) * 100, 2)

        sentiment_data = mark_safe(sentiment_data)

        return render(request, 'analytics.html', {'name': name,
                                                  'username': username,
                                                  'current_image': current_image,
                                                  'comments': comments,
                                                  'sentiment_data': sentiment_data})
    else:
        return render(request, 'analytics.html', {'name': name,
                                                  'username': username,
                                                  'current_image': current_image,
                                                  'comments': comments})


def show_loader(request):
    print("show_loader")
    name = request.session['name']
    username = request.session['username']
    show_div = True
    return render(request, 'index.html', {'show_div': show_div,
                                          'name': name,
                                          'username': username})


def get_metrics(request):

    likes = 0
    comments = 0
    engagement = 0

    if request.method == 'POST':

        with open(json_dir + "is_keyed_photo_metrics.json") as file:
            is_keyed_photo_metrics = json.load(file)

        with open(json_dir + "basic_profile_info.json") as file:
            basic_profile_info = json.load(file)

        follower_count = basic_profile_info[2]

        current_image = request.POST.get('current_image_id')
        current_image_id = os.path.splitext(current_image)[0]

        likes_and_comments = is_keyed_photo_metrics[current_image_id]
        regex = r"(\d+) likes, (\d+) comments"
        match = re.match(regex, likes_and_comments)

        likes = int(match.group(1))
        comments = int(match.group(2))

        engagement_rate = round(
            ((likes + comments) / follower_count * 100), 2)

        engagement = str(engagement_rate) + "%"

        data = {
            'likes': likes,
            'comments': comments,
            'engagement': engagement
        }
    return JsonResponse(data)


def facebook(request):
    return render(request, 'facebook.html')


def motivation(request):
    username = request.session['username']
    name = request.session['name']

    return render(request, 'motivation.html', {'username': username,
                                               'name': name})


def get_access_token(request):
    user = request.user
    try:
        user_social_auth = UserSocialAuth.objects.get(
            user=user, provider='facebook')
        access_token = user_social_auth.extra_data['access_token']
    except UserSocialAuth.DoesNotExist:
        access_token = None

    return access_token


def welcome(request):

    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            code = os.path.splitext(code)[0]

            url = 'https://api.instagram.com/oauth/access_token'

            payload = {
                'client_id': '',
                'client_secret': '',
                'grant_type': 'authorization_code',
                'redirect_uri': 'https://localhost:8000/welcome/',
                'code': code
            }

            response = requests.post(url, data=payload)

            data = response.json()
            data = data['access_token']

            set_access_token(data)

    return redirect('facebook')


def login(request):
    client_id = ''
    redirect_uri = 'https://localhost:8000/welcome/'
    scope = 'user_profile'

    url = (
        f'https://api.instagram.com/oauth/authorize?'
        f'client_id={client_id}&'
        f'redirect_uri={redirect_uri}&'
        f'scope={scope}&'
        f'response_type=code'
    )

    return redirect(url)
