from flask import Flask,render_template ,request
from dotenv import load_dotenv

import os
import requests
load_dotenv()
app=Flask(__name__)

@app.route('/getWeather/',methods=["POST","GET"])
def getWeather():
    cityy=request.form["city"]
    details={
        "q":cityy,
        "aqi":"yes",
        "key":os.environ.get('api_key')
    }   
    global response
    response = requests.post(url="http://api.weatherapi.com/v1/current.json",data=details)
    if response.status_code!=200:
        return render_template("base.html",w_name="",w_state="",w_country="",w_temp="",w_condition="",w_image="",w_isCityNotFound=1)
   
    status=response.status_code
    location=response.json()['location']['name']
    state=response.json()['location']['region']
    country=response.json()['location']['country']
    temperature = response.json()['current']['temp_c']
    condition = response.json()['current']['condition']['text']
    icon=response.json()['current']['condition']['icon']
    return render_template("base.html",w_name=location,w_state=state,w_country=country,w_temp = temperature,w_condition = condition,w_celcius="°C",w_image=icon,w_isCityNotFound=0)
@app.route('/')
def form():
 return render_template("base.html")
if __name__=="__main__":
 app.run(debug=True)