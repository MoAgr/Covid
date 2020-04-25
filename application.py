from flask import Flask, render_template, request
import requests
from datetime import datetime
from datetime import date, timedelta
from pytz import timezone

application = app = Flask(__name__)
lockdown_end_date = date(2020, 4, 27)
date_to_show = lockdown_end_date.strftime("%b %d")
UTC=timezone('UTC')

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
        title = str(nepali_news_json['data'][i]['title'])
        source = str(nepali_news_json['data'][i]['source'])
        nlink = str(nepali_news_json['data'][i]['url'])
        t = t + (title,)
        t = t + (source,)
        t = t + (nlink,)
        news_list.append(t)
        t = tuple()

    for i in range(0, 2):
        title = str(news_json_obj['articles'][i]['title'])
        source = str(news_json_obj['articles'][i]['source']['name'])
        nlink = str(news_json_obj['articles'][i]['url'])
        t = t + (title,)
        t = t + (source,)
        t = t + (nlink,)
        news_list.append(t)
        t = tuple()

    response = requests.get('http://brp.com.np/covid/nepal.php')
    json_object = response.json()
    confirmed_cases = int(json_object['latest_stat_by_country'][0]['total_cases'])
    # deaths = int(json_object['latest_stat_by_country'][0]['total_deaths'])
    recovered = int(json_object['latest_stat_by_country'][0]['total_recovered'])
    active =int(json_object['latest_stat_by_country'][0]['active_cases'])
    todays_date = date.today()
    days_to_go = str((lockdown_end_date+timedelta(1)) - todays_date).split(',')[0]
    update_time=str(json_object['latest_stat_by_country'][0]['record_date']).split()[1]
    current_time = str(datetime.now(UTC)).split()[1]
    update_time_hrs=int(update_time.split(':')[0])
    current_time_hrs=int(current_time.split(':')[0])
    if(update_time_hrs==current_time_hrs):
        update_time_min=int(update_time.split(':')[1])
        current_time_min = int(current_time.split(':')[1])
        if(current_time_min-update_time_hrs==1):
            time=str(current_time_min-update_time_min)+' minute'
        else:
            time = str(current_time_min - update_time_min) + ' minutes'
    else:
        if(current_time_hrs-update_time_hrs==1):
            time=str(current_time_hrs-update_time_hrs)+' hour'
        else:
            time = str(current_time_hrs - update_time_hrs) + ' hours'

    return render_template("main.html", total=confirmed_cases, active=active, recovered=recovered, time=time,
                           lockdown_end_date=date_to_show, days_to_go=days_to_go, news_list=news_list)

@app.route('/contact')
def contact():
    return render_template("contact.html")
