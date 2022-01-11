# From External Libraries
from time import sleep

import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import xlsxwriter
from datetime import datetime

# From Own Script
import fetch_from_trello
import commands

# 建立Local Sheet
student_workbook = xlsxwriter.Workbook('Results/Student Info.xlsx')
students = student_workbook.add_worksheet()
notice_workbook = xlsxwriter.Workbook('Results/Notice.xlsx')
notice = notice_workbook.add_worksheet()

# Extract local student list
active_file = open("Active Student List.txt", "r", encoding='utf-8', errors='ignore')
active_student_list = active_file.read().splitlines()

# 绘制Student Info表头
students.write(0, 0, 'Name')
students.write(0, 1, '总课时')
students.write(0, 2, '剩余课时')
students.write(0, 3, 'Current Class')
students.write(0, 4, '多少天没上课')

# 绘制Notice表头
notice.write(0, 0, 'Notice')
notice.write(0, 1, 'Students')
notice.write(1, 0, '三周没上课')

# Authorize with Google
scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
credential = ServiceAccountCredentials.from_json_keyfile_name('Auth Info/Google Auth.json', scope)
client = gspread.authorize(credential)
sheet = client.open("Demo Sheet").worksheet("Test")

# Extract Data from Trello
with open('Auth Info/Trello Auth.json') as json_file:
    auth_data = json.load(json_file)
board_list = fetch_from_trello.get_boards(auth_data)  # get list of boards
fetch_from_trello.convert_data(board_list, active_student_list)

# Run Commands and Update to Google Sheet
count = 0
absent_list = []

for board in board_list:
    # Identify whether to track this board
    board_name = board['name']
    if board_name not in active_student_list:
        continue

    count += 1  # Set Counter

    # Retrieve data from trello
    students.write(count, 0, board_name)
    data = fetch_from_trello.get_user_data(board_name)  # Fetch JSON file

    # Basic variables
    TODO_id = commands.get_TODO_id(data['lists'])
    Doing_id = commands.get_Doing_id(data['lists'])
    Done_id = commands.get_Done_id(data['lists'])

    # Run them commands
    total_sessions = commands.get_total_sessions(data['cards'])
    students.write(count, 1, total_sessions)
    remaining_sessions = commands.get_remaining_sessions(data['cards'], TODO_id, total_sessions)
    students.write(count, 2, remaining_sessions)
    current_session = commands.get_current_class(data['cards'], Doing_id, Done_id)
    students.write(count, 3, current_session)
    absence_time = commands.get_absence_time(data['cards'], current_session)
    students.write(count, 3, absence_time)
    if absence_time != 'NA' and int(absence_time) > 21:
        absent_list.append(board_name)

print(absent_list)
for i in range(0, len(absent_list)):
    notice.write(1, i + 1, absent_list[i])

# Close local sheet and push to Google
student_workbook.close()
notice_workbook.close()
