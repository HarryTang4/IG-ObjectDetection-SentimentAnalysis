import instaloader
from django.conf import settings
from instaloader import Profile, Post
import shutil
import os
from os import path
import json


def get_images(username, profile_photo_url):

    local_dir = settings.STATIC_ROOT + '/media/' + username
    json_dir = settings.JSON_ROOT

    with open(json_dir + "keyed_media_urls.json") as file:
        keyed_media_urls = json.load(file)

    keyed_shortcodes = []
    for key, value in keyed_media_urls.items():
        current_list = []
        current_list.append(str(key))
        current_list.append(str(value[0]))
        keyed_shortcodes.append(current_list)

    if os.path.exists(local_dir):
        for file in os.listdir(local_dir):
            if not file.endswith(".xz") and not file.endswith(".mp4") and not file.endswith(".txt"):
                if file.endswith("/_1.jpg"):
                    new_name = file.replace('/_1.jpg', '/.jpg')
                    os.rename(local_dir + file,
                              local_dir + new_name)
                continue
            os.remove(os.path.join(local_dir, file))

    else:
        for shortcode in keyed_shortcodes:
            I = instaloader.Instaloader(
                dirname_pattern=local_dir, filename_pattern=shortcode[0], slide='1')
            post = Post.from_shortcode(I.context, shortcode=shortcode[1])
            I.download_post(
                post, target=username)

    gallery_id_list = []
    for key, value in keyed_media_urls.items():
        gallery_id_list.append(key)

    return gallery_id_list