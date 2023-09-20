import requests
import json


def update_creds(access_token, page_id, instagram_account_id, ig_username):

    arguements = [access_token, page_id, instagram_account_id, ig_username]

    for field in arguements:
        if field == False:
            continue
        else:
            creds[str(arguements.index(field))] = field

    return creds


creds = dict()


def set_creds():

    # Project specific credentials
    creds['client_id'] = ''
    creds['client_secret'] = ''
    creds['endpoint_base'] = 'https://graph.facebook.com/v16.0/'

    # User access tokens
    creds['short_lived_access_token'] = ''
    creds['access_token'] = ''

    # User specific credentials
    creds['page_id'] = ''
    creds['instagram_account_id'] = ''
    creds['ig_username'] = ''
    creds['name'] = ''

    return creds


def make_apicall(url, endpoint_params):

    data = requests.get(url, endpoint_params)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpoint_params
    response['json_data'] = json.loads(data.content)

    try:
        access_token = (response['json_data']['access_token'])

    except:
        access_token = False

    try:
        page_id = (response['json_data']['data'][0]['id'])

    except:
        page_id = False

    try:
        instagram_account_id = (
            response['json_data']['instagram_business_account']['id'])
    except:
        instagram_account_id = False

    try:
        ig_username = (
            response['json_data']['business_discovery']['username'])

    except:
        ig_username = False

    update_creds(access_token, page_id, instagram_account_id, ig_username)

    return response['json_data']
