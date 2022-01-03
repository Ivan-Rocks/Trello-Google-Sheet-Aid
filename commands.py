def get_sessions(cards, lists):
    list_id = ''
    count = 0
    for i in lists:
        if i['name'] == 'Doing':
            list_id = i['id']
    for i in cards:
        if i['idList'] == list_id:
            count += 1
    return count


def get_time(cards):
    l = ['', '', '', '', '', '', '', '', '', '', '', '']
    for i in cards:
        if i['name'].find('session') != -1:
            length = len(i['name'])
            s = i['name'][7:length]
            index = int(s)
            r = ''
            if i['start'] is None:
                r = 'NA'
            else:
                r = str(i['start'])
            l[index - 1] = r
    return l
