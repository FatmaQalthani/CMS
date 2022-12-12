from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask_mail import Mail,Message
from random import randint
app = Flask(__name__)
mail=Mail(app)

#Mail Info 10-15
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='fatmaalqahapplication@gmail.com'
app.config['MAIL_PASSWORD']='lciwhwgcebqzgvgo'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)


#Database Config
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

    def __repr__(self):
        return '<User %r'% self.id

doctors=[{
    "id":1,
    "name":"Waleed",
},{
    "id":2,
    "name":"Abdullah"}]
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])

#Login Code 40-53

def login():
    
    if request.method == 'POST' and 'password' in request.form and 'email' in request.form :
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        user =User.query.filter_by(email=email).first()   #Database Query
        if not user:
            return 'User not Found!',404
        else:
            bcrypt.checkpw(password.encode('utf-8'),user.password)
            return redirect(f'http://127.0.0.1:5000/welcome/{user.id}')
    else:
        return render_template('index.html')


#
@app.route('/welcome/<id>')

def welcome(id):
    user =User.query.filter_by(id=id).first()


    return render_template('welcome.html',user=user,doctors=doctors)

@app.route('/select/<name>')
def select(name):

    return f'You have selected {name}' 

def verify(email):
    msg=Message(subject='OTP',sender='fatmaalqahapplication@gmail.com',recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    
@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return "<h3>Email verification successfull</h3"
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''

    if request.method == 'POST' and 'password' in request.form and 'email' in request.form :
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        #Hashed 90-91
        pw_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        user=User(email=email,password=pw_hash)
        db.session.add(user)
        db.session.commit()
        verify(email)
        return render_template('verify.html')
    else:

        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)