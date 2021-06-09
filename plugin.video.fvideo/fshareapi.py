# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 09:27:53 2021

@author: congtm
"""

# -- REQUIRE LIBRARIES ---
# requests - pip install

import sys
import requests
from requests.auth import HTTPBasicAuth


def login_api(user_agent, user_email, password, app_key):
    # print('Tai khoan: ' + user_email)
    data = {
        "user_email": user_email,
        "password": password,
        "app_key": app_key
    }

    headers = {
        "user-agent": user_agent
    }

    r = requests.post('https://api.fshare.vn/api/user/login', json=data, headers=headers)
    # print('download_api :', r.json())
    return r.json()


def download_api(data_url, password, token, user_agent, cookie):
    data = {
        "url": data_url,
        "password": password,
        "token": token,
        "zipflag": 0
    }

    headers = {
        'user-agent': user_agent,
        'cookie': 'session_id=' + cookie
    }

    # create a Session
    r = requests.post('https://api.fshare.vn/api/session/download', json=data, headers=headers)
    # print('location : ',r.json())

    return r.json()
