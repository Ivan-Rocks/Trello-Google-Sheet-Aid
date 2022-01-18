# From External Libraries
from time import sleep

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
inactive_file = open("Inactive Student List.txt", "r", encoding='utf-8', errors='ignore')
inactive_student_list = inactive_file.read().splitlines()

# 绘制Student Info表头
students.write(0, 0, 'Name')
students.write(0, 1, '总课时')
students.write(0, 2, '剩余课时')
students.write(0, 3, 'Current Class')
students.write(0, 4, '多少天没上课')
students.write(0, 5, '课程时间')

# 绘制Notice表头
notice.write(0, 0, 'Notice')
notice.write(0, 1, 'Students')
notice.write(1, 0, '三周没上课')
notice.write(2, 0, '科普论文start')
notice.write(3, 0, '科普论文due')
notice.write(4, 0, '开题due')
notice.write(5, 0, '答辩due')
notice.write(6, 0, '论文due')
notice.write(7, 0, '提醒Due')

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
fetch_from_trello.convert_data(board_list, inactive_student_list)

# Run Commands and Update to Google Sheet
count = 0
absent_list = []
KEPU_start_list = []
KEPU_due_list = []
KAITI_due_list = []
DABIAN_due_list = []
essay_due_list = []
feedback_due_list = []


for board in board_list:
    # Identify whether to track this board
    board_name = board['name']
    if board_name in inactive_student_list:
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
    students.write(count, 4, absence_time)
    class_time_list = commands.get_class_time(data['cards'], total_sessions)
    print(board_name)
    print(class_time_list)
    session_cnt = 0
    for session_time in class_time_list:
        students.write(count, 5 + session_cnt, session_time)
        session_cnt += 1

    # 三周不上课提醒
    if absence_time != 'NA' and int(absence_time) > 21:
        absent_list.append(board_name)
    # 科普论文开题提醒
    if current_session == 2:
        KEPU_start_list.append(board_name)
    # 科普论文due提醒
    if current_session == 4:
        KEPU_due_list.append(board_name)
    # 开题due提醒
    if current_session == 6:
        KAITI_due_list.append(board_name)
    # 答辩due提醒
    if current_session == 12:
        DABIAN_due_list.append(board_name)
    # 论文due提醒
    if current_session == 12 and absence_time > 28:
        essay_due_list.append(board_name)
    # Feedback提醒
    if current_session % 3 == 0:
        feedback_due_list.append(board_name)

# Write Notices
for i in range(0, len(absent_list)):
    notice.write(1, i + 1, absent_list[i])
for i in range(0, len(KEPU_start_list)):
    notice.write(2, i + 1, KEPU_start_list[i])
for i in range(0, len(KEPU_due_list)):
    notice.write(3, i + 1, KEPU_due_list[i])
for i in range(0, len(KAITI_due_list)):
    notice.write(4, i + 1, KAITI_due_list[i])
for i in range(0, len(DABIAN_due_list)):
    notice.write(5, i + 1, DABIAN_due_list[i])
for i in range(0, len(essay_due_list)):
    notice.write(6, i + 1, essay_due_list[i])
for i in range(0, len(feedback_due_list)):
    notice.write(7, i + 1, feedback_due_list[i])

# Close local sheet and push to Google
student_workbook.close()
notice_workbook.close()
