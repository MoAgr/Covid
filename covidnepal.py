from flask import Flask,render_template,request
import requests
from datetime import datetime
from datetime import date
application=app=Flask(__name__)
lockdown_end_date=date(2020,4,28)
date_to_show=lockdown_end_date.strftime("%b %d")
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
    return render_template("main.html", total = confirmed_cases, active = active, recovered = recovered,time=time,lockdown_end_date=date_to_show,days_to_go=days_to_go)
    

if __name__=='__main__':
    app.run(debug=True)
