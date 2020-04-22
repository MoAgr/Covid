from flask import Flask,render_template,request
import requests
app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def cases():
    response=requests.get('https://api.covid19api.com/live/country/nepal/status/confirmed')
    json_object=response.json()
    confirmed_cases=int(json_object[-1]['Confirmed'])
    deaths=int(json_object[-1]['Deaths'])
    recovered=int(json_object[-1]['Recovered'])
    active=int(json_object[-1]['Active'])
    return render_template("main.html", total = confirmed_cases, active = active, recovered = recovered)
    

