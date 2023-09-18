import requests
import json

creds = dict()


def update_creds(page_id, instagram_account_id, ig_username):

    arguements = [page_id, instagram_account_id, ig_username]

    for field in arguements:
        if field == False:
            continue
        else:
            creds[str(arguements.index(field))] = field

    return creds


def get_creds():

    creds['access_token'] = 'EAAD64s4jSDMBAJ8sv6RYnErMB0sa9ScLD1d3hJTtFVpUyegLR5HQy4UDMfwbEbrDoDzUDCfA8F240SJkOZAL1EysgCpm1ZAdhPOTQFFX1Wcow86KSZAaPRKNC1HKxTYZCeMFeDTwSiSSvGqNwEEoS04tngdXpAJP70ZAtfWXFeMc9o85bUIHR'
    creds['client_id'] = '275852027971635'
    creds['client_secret'] = '4101b06db1a41a2513f97f0f99d5bb3b'
    creds['endpoint_base'] = 'https://graph.facebook.com/v16.0/'

    '''

    the following fields are inputted by the user but are by default
    set to 1.harrytang (my personal account).

    '''

    creds['instagram_account_id'] = ''
    creds['page_id'] = ''
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

    update_creds(page_id, instagram_account_id, ig_username)

    with open("json/" + "defines" + ".json", 'w') as outfile:
        json.dump(response['json_data'], outfile)

    return response['json_data']
