from flask import Flask,render_template,request
import requests
from datetime import datetime
from datetime import date,timedelta
application=app=Flask(__name__)
lockdown_end_date=date(2020,4,28)
date_to_show=lockdown_end_date.strftime("%b %d")
news_list=[]
t=tuple()
@app.route('/',methods=['GET','POST'])
def cases():
    response=requests.get('https://api.covid19api.com/live/country/nepal/status/confirmed')
    json_object=response.json()
    confirmed_cases=int(json_object[-1]['Confirmed'])
    deaths=int(json_object[-1]['Deaths'])
    recovered=int(json_object[-1]['Recovered'])
    active=int(json_object[-1]['Active'])
    todays_date=date.today()
    days_to_go=str(lockdown_end_date-todays_date).split(',')[0]
    time= str(datetime.now())
    time = time.split()[1].split(':')[0]
    news=requests.get('https://newsapi.org/v2/top-headlines?q=corona&apiKey=71026374f7a64e73896dfc7ef9c35d03&pageSize=50&page=2&language=en&from='+str(date.today()-timedelta(2))+'&sortBy=popularityAt')
    news_json_obj=news.json()
    for i in range(0,5):
        title=str(news_json_obj['articles'][i]['title'])
        source=str(news_json_obj['articles'][i]['source']['name'])
        nlink=str(news_json_obj['articles'][i]['url'])
        t=t+(title,)
        t=t+(source,)
        t=t+(nlink,)
        news_list.append(t)
        t=tuple()
    return render_template("main.html", total = confirmed_cases, active = active, recovered = recovered,time=time,lockdown_end_date=date_to_show,days_to_go=days_to_go,news_list=news_list)
    

if __name__=='__main__':
    app.run(debug=True)
