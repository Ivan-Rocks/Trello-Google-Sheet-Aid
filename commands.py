from datetime import date, datetime


def get_total_sessions(cards):
    count = 0
    for i in cards:
        if i['name'].find('Session') != -1:
            count += 1
    return count


def get_remaining_sessions(cards, list_id, total):
    count = 0
    for i in cards:
        if i['idList'] == list_id and i['name'].find('Session') != -1:
            count += 1
    return count


def get_current_class(cards, doing, done):
    max_index = 0
    for i in cards:
        if (i['idList'] == done or i['idList'] == doing) and i['name'].find('Session') != -1:
            if get_index(i) > max_index:
                max_index = get_index(i)
    return max_index


def get_class_time(cards, total_sessions):
    l = []
    cnt = 1
    for index in range(1, total_sessions + 1):
        for i in cards:
            if get_index(i) == index:
                start = 0
                if i is not None and i['start'] is not None:
                    year = (i['start'][0:4])
                    month = (i['start'][5:7])
                    day = (i['start'][8:10])
                    start = year + ' ' + month + ' ' + day
                l.append(start)
    return l


def get_absence_time(cards, session):
    cur_card = None
    for i in cards:
        if get_index(i) == session:
            cur_card = i
    if cur_card is None or cur_card['start'] is None:
        return 0
    year = int(cur_card['start'][0:4])
    month = int(cur_card['start'][5:7])
    day = int(cur_card['start'][8:10])
    start = date(year, month, day)
    today = date.today()
    return (today - start).days


# Helper functions
def get_TODO_id(lists):
    list_id = ''
    for i in lists:
        if i['name'] == 'TODO':
            list_id = i['id']
    return list_id


def get_Doing_id(lists):
    list_id = ''
    for i in lists:
        if i['name'] == 'Doing':
            list_id = i['id']
    return list_id


def get_Done_id(lists):
    list_id = ''
    for i in lists:
        if i['name'] == 'Done':
            list_id = i['id']
    return list_id


def get_Feedback_id(lists):
    list_id = ''
    for i in lists:
        if i['name'] == 'Feedback':
            list_id = i['id']
    return list_id


def get_index(i):
    if i['name'].find('Session') == -1:
        return -1
    length = len(i['name'])
    s = i['name'][8:length]
    if s.isdigit() is False:
        return -2
    index = int(s)
    return index
