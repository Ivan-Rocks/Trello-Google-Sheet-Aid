from pprint import pp
import pandas as pd
import numpy as np
import requests
import request
from requests_oauthlib import OAuth1Session

# print('Hi')  # Sanity Check

raw_data = pd.read_excel('auth.xlsx')
data = np.array(raw_data)  # 先将数据框转换为数组

api_key = data[0][3]
api_secret = data[0][4]
token = data[0][1]
trello = OAuth1Session(api_key, api_secret, token)

r = trello.get('https://trello.com/b/wZlfoT6y/intern-record.json')
pp(r.content)
print(r.status_code)

x = request.generate_request()
print(x);
