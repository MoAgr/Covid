from flask import Flask, render_template, request
import requests,datetime
from datetime import date,timedelta
from datetime import datetime as dttime
import pytz
from pytz import timezone

application = app = Flask(__name__)
lockdown_end_date = date(2020, 6, 2)
date_to_show = lockdown_end_date.strftime("%b %d")
UTC=timezone('UTC')
ktm=timezone('Asia/Kathmandu')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def cases():
    news_list = []
    t = tuple()
    news = requests.get(
        'https://newsapi.org/v2/top-headlines?q=corona&apiKey=71026374f7a64e73896dfc7ef9c35d03&pageSize=50&page=2&language=en&from=' + str(
            date.today() - timedelta(2)) + '&sortBy=popularityAt')
    news_json_obj = news.json()
    nepali_news = requests.get('https://nepalcorona.info/api/v1/news')
    nepali_news_json = nepali_news.json()

    for i in range(0, 3):
        title = (nepali_news_json['data'][i]['title'])
        source = (nepali_news_json['data'][i]['source'])
        nlink = (nepali_news_json['data'][i]['url'])
        t = t + (title,)
        t = t + (source,)
        t = t + (nlink,)
        news_list.append(t)
        t = tuple()

    for i in range(0, 2):
        title = (news_json_obj['articles'][i]['title'])
        source = (news_json_obj['articles'][i]['source']['name'])
        nlink = (news_json_obj['articles'][i]['url'])
        t = t + (title,)
        t = t + (source,)
        t = t + (nlink,)
        news_list.append(t)
        t = tuple()

    response = requests.get('https://nepalcorona.info/api/v1/data/nepal')
    json_object = response.json()
    response1=requests.get('https://data.nepalcorona.info/api/v1/covid')
    json_object_1=response1.json()
    confirmed_cases = int(json_object['tested_positive'])
    deaths = int(json_object['deaths'])
    recovered = int(json_object['recovered'])
    active =confirmed_cases-recovered-deaths
    todays_date = date.today()

    # NEW CASES COUNT:
    # list_of_cases = [630, 675]
    # if active != list_of_cases[-1]:
    #     list_of_cases.append(active)
    # new_cases = list_of_cases[-1] - list_of_cases[-2]

    days_to_go = str((lockdown_end_date+timedelta(1)) - todays_date).split(',')[0]
    # update_time=str(json_object_1[-2]['createdOn']).split('+')[0]
    # update_time=dttime.strptime(update_time,'%Y-%m-%dT%H:%M:%S.%f')
    # # update_time = update_time.replace(tzinfo=pytz.timezone('Asia/Kathmandu'))
    # update_time=pytz.timezone('Asia/Kathmandu').localize(update_time)
    # current_time =(dttime.now(ktm))
    # tdelta=current_time-update_time
    # if(tdelta.days==0):
    #     time1_hour=str(tdelta).split(':')[0]
    #     if(int(time1_hour)==0):
    #         time1_minute=str(tdelta).split(':')[1]
    #         if(int(time1_minute)==1):
    #             time=time1_minute+ ' minute'
    #         else:
    #             time=time1_minute+' minutes'
    #     elif(int(time1_hour)==1):
    #         time=time1_hour+ ' hour'
    #     else:
    #         time=time1_hour+' hours'
    # else:
    #     time1_day=str(tdelta).split(',')[0]
    #     time=time1_day

    return render_template("main.html", total=confirmed_cases, active=active, recovered=recovered,
                           lockdown_end_date=date_to_show, days_to_go=days_to_go, news_list=news_list, deaths = deaths)

@app.route('/contact')
def contact():
    return render_template("contact.html")
