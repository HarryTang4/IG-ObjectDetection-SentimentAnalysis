from defines import get_creds, make_apicall
import json


def get_user_media(params):

    endpoint_params = dict()
    endpoint_params[
        'fields'] = 'timestamp,id,caption,media_type,shortcode'
    endpoint_params['access_token'] = params['access_token']

    url = params['endpoint_base'] + \
        params['instagram_account_id'] + '/media'

    response = make_apicall(url, endpoint_params)

    id_shortcodes = {post['id']: post['shortcode']
                     for post in response['data']}

    with open("json/" + "keyed_shortcodes" + ".json", 'w') as outfile:
        json.dump(id_shortcodes, outfile)

    with open("json/" + "current_profile_photos" + ".json", 'w') as outfile:
        json.dump(response, outfile)

    return response


def get_comments_and_likes(params):

    endpoint_params = dict()
    endpoint_params[
        'fields'] = 'id,comments,like_count,comments_count'
    endpoint_params['access_token'] = params['access_token']

    url = params['endpoint_base'] + \
        params['instagram_account_id'] + '/media'

    response = make_apicall(url, endpoint_params)

    print(response)

    with open("json/" + "current_comments" + ".json", 'w') as outfile:
        json.dump(response, outfile)

    is_keyed_comments = {}
    is_keyed_photo_metrics = {}

    for obj in response['data']:
        photo_id = obj['id']
        if 'comments' in obj:
            comments = []
            for comment in obj['comments']['data']:
                comments.append(comment['text'])
            is_keyed_comments[photo_id] = comments

    for key in response['data']:
        photo_id = key['id']
        like_count = key['like_count']
        comments_count = key['comments_count']
        count_str = str(like_count) + ' likes, ' + \
            str(comments_count) + ' comments'
        is_keyed_photo_metrics[photo_id] = count_str

    with open("json/" + "is_keyed_comments" + ".json", 'w') as outfile:
        json.dump(is_keyed_comments, outfile)

    with open("json/" + "is_keyed_photo_metrics" + ".json", 'w') as outfile:
        json.dump(is_keyed_photo_metrics, outfile)

    return make_apicall(url, endpoint_params)


def get_long_lived_token(params):
    endpoint_params = dict()
    endpoint_params['grant_type'] = 'fb_exchange_token'
    endpoint_params['client_id'] = params['client_id']
    endpoint_params['client_secret'] = params['client_secret']
    endpoint_params['fb_exchange_token'] = params['access_token']

    url = params['endpoint_base'] + 'oauth/access_token'

    response = make_apicall(url, endpoint_params)

    long_lived_token = str(response['access_token'])

    return long_lived_token


def get_page_id(params):

    endpoint_params = dict()
    endpoint_params['access_token'] = params['access_token']

    url = params['endpoint_base'] + 'me/accounts'

    response = make_apicall(url, endpoint_params)

    page_id = str(response['data'][0]['id'])

    return page_id


def get_instagram_account_id(params):

    endpoint_params = dict()
    endpoint_params['access_token'] = params['access_token']
    endpoint_params['fields'] = 'instagram_business_account'

    url = params['endpoint_base'] + params['page_id']

    response = make_apicall(url, endpoint_params)

    instagram_account_id = str(response['instagram_business_account']['id'])

    return instagram_account_id


def get_ig_username(params):

    endpoint_params = dict()
    endpoint_params['access_token'] = params['access_token']
    endpoint_params['fields'] = 'username,name,followers_count'

    url = params['endpoint_base'] + params['instagram_account_id']

    response = make_apicall(url, endpoint_params)

    basic_profile_info = [response['username'],
                          response['name'], response['followers_count']]

    with open("json/" + "basic_profile_info" + ".json", 'w') as outfile:
        json.dump(basic_profile_info, outfile)

    print(basic_profile_info)

    ig_username = str(response['username'])

    return ig_username


def set_creds():
    params = get_creds()

    page_id = get_page_id(params)
    params['page_id'] = page_id

    instagram_account_id = get_instagram_account_id(params)
    params['instagram_account_id'] = instagram_account_id

    username = get_ig_username(params)
    params['ig_username'] = username

    long_lived_token = get_long_lived_token(params)
    params['access_token'] = long_lived_token

    print(params)

    return params


def main():
    params = set_creds()

    get_user_media(params)
    get_comments_and_likes(params)


main()
