import pandas as pd
import numpy as np
import fetch_from_trello
from requests_oauthlib import OAuth1Session

raw_data = pd.read_excel('auth.xlsx')
data = np.array(raw_data)  # 先将数据框转换为数组
fetch_from_trello.convert_data(data)

api_key = data[0][3]
api_secret = data[0][4]
token = data[0][1]
trello = OAuth1Session(api_key, api_secret, token)
