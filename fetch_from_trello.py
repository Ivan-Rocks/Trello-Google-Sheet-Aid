from requests_oauthlib import OAuth1Session
from pprint import pp, pprint
import json

from commands import get_remaining_sessions


# Get the list of existing boards
def get_boards(data):
    api_key = data['key']
    api_secret = data['OAuth']
    token = data['token']
    trello = OAuth1Session(api_key, api_secret, token)
    url = 'https://api.trello.com/1/members/me/boards?key=add7e1644b237dd2dae95b7b2f39c3b4' \
          '&token=0732d1e3c9b5528454803f7d4992b1579ad4f821ab98ba61ec3c1afc1e7da690'
    r = trello.get(url)
    with open("JSON/Student List.json", 'w') as outfile:
        json.dump(r.json(), outfile)
    return r.json()


# Fetch board information from Trello and convert to JSON
def convert_data(data, active_student_list):
    count = 0
    for i in data:
        board_name = i['name']
        if board_name not in active_student_list:
            continue
        api_key = 'add7e1644b237dd2dae95b7b2f39c3b4'
        api_secret = '89fb5caca76cc0c24bdd7e66222b33aaaf1fad668cb6f890c397ad302bb905f1'
        token = '0732d1e3c9b5528454803f7d4992b1579ad4f821ab98ba61ec3c1afc1e7da690'
        short_id = i['shortLink']
        trello = OAuth1Session(api_key, api_secret, token)
        r = trello.get(generate_board_request_url(short_id, board_name))
        content = r.json()
        write_to_json(board_name, content)
        count += 1
        print("List Converted " + str(count) + "/" + str(len(active_student_list)))
    print('Conversion Completed')


# Helper function to generate url request to access boards
def generate_board_request_url(short_id, board_name):
    url = 'https://trello.com/b/'
    url = url + short_id + '/'
    url = url + board_name + '.json'
    return url


# Write boards into JSON file
def write_to_json(board_name, content):
    directory = 'JSON/' + board_name + '.json'
    with open(directory, 'w') as outfile:
        json.dump(content, outfile)


# Given a board name, return the JSON board file of that user
def get_user_data(board_name):
    directory = 'JSON/' + board_name + '.json'
    with open(directory) as json_file:
        user_json = json.load(json_file)
    return user_json
