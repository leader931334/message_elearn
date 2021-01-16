import os
import time
import datetime
import random
import requests
from bs4 import BeautifulSoup

try:
    import settings as st
except ModuleNotFoundError:
    import sample_settings as st
    st.payload['login']['username'] = os.environ['USERNAME']
    st.payload['login']['password'] = os.environ['PASSWORD']


def login(session):
    return session.post(st.url['login'], st.payload['login'], headers=st.headers)


def getTodayId(session):
    res = session.get(st.url['date_list'], headers=st.headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    today = datetime.date.today()
    keyword = '{}/{}検温'.format(today.month, today.day)

    for e in soup.find_all(class_='activityinstance')[1:]:
        if keyword in e.find('span').text:
            return e.find('a').get('href').split('=')[-1]
    return None


def hasSubmitted(session, idx):
    res = ss.get(st.url['input']+idx, headers=st.headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup.find('input').get('value') == '続ける'


def kenon_submit(session, idx):
    res = session.get(st.url['input']+idx, headers=st.headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    payload = dict()

    for e in soup.find_all('select'):
        payload[e.get('name')] = '1'

    for e in soup.find_all('input'):
        payload[e.get('name')] = e.get('value')
    
    return session.post(st.url['submit'], payload, headers=st.headers)


if __name__ == '__main__':
    time.sleep(60 * random.randint(1, 5))
    with requests.Session() as ss:
        login(ss)

        kenon_id = getTodayId(ss)

        if kenon_id is not None and not hasSubmitted(ss, kenon_id):
            kenon_submit(ss, kenon_id)
            print(datetime.datetime.now(), 'submitted.')
        else:
            print(datetime.date.today(), 'id is not found or has submitted.')
            
