from flask import Flask, render_template,request
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user,logout_user
from flask import redirect
from flask import url_for

from mockdbhelper import MockDBHelper as DBHelper
from user import User

app = Flask(__name__)
app.secret_key = 'KKh5F8B0fv9WI0b4VfQGNoTRk71fMz9IRv8zBAohD7DIbhu2F+RAqsfDPELFX0UqZlUHfYEMp6CWG8CjxE/OOgiEdZuXDn2wteT7'
login_manager = LoginManager(app)
DB = DBHelper()

@app.route("/")
def home():
   return render_template("home.html")

@app.route("/account")
@login_required
def account():
   return "You are logged in" 

@app.route("/login", methods=["POST"])
def login():
   email = request.form.get("email")
   password = request.form.get("password")
   user_password = DB.get_user(email)
   if user_password and user_password == password:
      user = User(email)
      login_user(user, remember=True)
      return redirect(url_for('account'))
   return home()  

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
       return User(user_id)      

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for("home"))   

if __name__ == '__main__':
    app.run(port=5000, debug=True)