from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
import os
from dotenv import load_dotenv 
from sqlalchemy.exc import IntegrityError
import requests
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY']='123456'
db = SQLAlchemy(app)
load_dotenv()
global api_key
api_key=os.environ.get('api_key')
login_manager=LoginManager()
login_manager.init_app(app)
class users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(200))
@login_manager.user_loader
def load_user(id):
    return users.query.get(id)

@app.route('/login',methods=['POST'])
def loginUser():
    name=request.form["username"]
    password=request.form["password"]
    detail=users.query.filter_by(name=name).first()
    try:
        detail.name
    except(AttributeError):
        return "USER NAME DOES NOT EXIST"
    if(check_password_hash(detail.password,password)):
            login_user(detail)
            return redirect(url_for('form'))
        
            
    return"INCORRECT PASSWORD"


@app.route('/logout')
@login_required
def logoutUser():
      logout_user()
      return redirect(url_for('home'))
      

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/signUp')
def signUp():
    return render_template("signup.html")

@app.route('/register',methods=['POST'])
def register():
    name = request.form['username']
    password = request.form['pass']
    hash_password = generate_password_hash(password,"pbkdf2:sha256",salt_length=8)
    db.create_all()
    data = users(name=name,password=hash_password)
    try : 
       db.session.add(data)
       db.session.commit()
    except(IntegrityError):
       db.session.rollback()
       print ("error adding user")
       return "User already exists"
    return redirect(url_for("home"))
@app.route('/getWeather',methods=["POST","GET"])
@login_required
def getWeather():

    cityy=request.form["city"]
    details={
        "q":cityy,
        "aqi":"yes",
        "key":api_key
    }  
    print (api_key)
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
@app.route('/weather')
@login_required
def form():
 return render_template("base.html")
 
if __name__ == "__main__":
    app.run( debug=True)