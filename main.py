# From External Libraries
from time import sleep

import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json

# From Own Script
import commands
import fetch_from_trello
import commands

# Authorize with Google
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
credential = ServiceAccountCredentials.from_json_keyfile_name('Auth Info/Google Auth.json', scope)
client = gspread.authorize(credential)
sheet = client.open("Demo Sheet").worksheet("Test")

# 绘制Google Sheet表头
sheet.update_cell(1, 1, 'Name')
sheet.update_cell(1, 2, '课时')

# Extract Data from Trello
with open('Auth Info/Trello Auth.json') as json_file:
    auth_data = json.load(json_file)
board_list = fetch_from_trello.get_boards(auth_data)  # get list of boards
fetch_from_trello.convert_data(board_list)

sheet.update_cell(1, 1, 'Name')
sheet.update_cell(1, 2, '课时')
sheet.update_cell(1, 3, 'Time')

board_name = board_list[26]['name']
sheet.update_cell(2, 1, board_name)
data = fetch_from_trello.get_user_data(board_name)
sessions = commands.get_sessions(data['cards'], data['lists'])
sheet.update_cell(2, 2, sessions)
time = commands.get_time(data['cards'])
print(time)

print('Finished updating to Google Sheet')

# Run Commands and Update to Google Sheet
count = 1
for board in board_list:
    count += 1
    board_name = board['name']
    sheet.update_cell(count, 1, board_name)
    data = fetch_from_trello.get_user_data(board_name)
    sessions = commands.get_sessions(data['cards'], data['lists'])
    sheet.update_cell(count, 2, sessions)
    class_time = commands.get_time(data['cards'])
    for i in range(11):
        sheet.update_cell(count, 3 + i, class_time[i])
    if count % 30 == 0:
        sleep(100)
        print('Sleeping Started')
    if count % 30 == 0:
        print('Sleeping Finished')