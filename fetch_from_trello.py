from requests_oauthlib import OAuth1Session
from pprint import pp, pprint
import json


def convert_data(data):
    for i in data:
        board_name = i[0]
        api_key = i[3]
        api_secret = i[4]
        token = i[1]
        short_id = i[5]
        trello = OAuth1Session(api_key, api_secret, token)
        r = trello.get(generate_board_request_url(short_id, board_name))
        pprint(r.json())
        print(r.status_code)
        print(board_name)
        content = r.json()
        write_to_json(board_name, content)


def generate_board_request_url(short_id, board_name):
    url = 'https://trello.com/b/'
    url = url + short_id + '/'
    url = url + board_name + '.json'
    return url


def write_to_json(board_name, content):
    directory = 'JSON/' + board_name + '.json'
    with open(directory, 'w') as outfile:
        json.dump(content, outfile)


