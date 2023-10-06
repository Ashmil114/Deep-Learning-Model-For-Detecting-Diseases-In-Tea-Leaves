from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import predict

app=Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="tea"
app.secret_key="sample_key" # its for msg flashing
app.config['UPLOAD_FOLDER']="static/images/uploads"
mysql = MySQL(app)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    
    return render_template("about.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur =mysql.connection.cursor()
        user = cur.execute("SELECT * FROM user WHERE email = %s AND password = %s ",(email,password))
        if user == 1:
            Details = cur.fetchall()
            return  redirect(url_for('teahome',user=Details[0][1]))
        else:
            flash('User Not Found !')
            return render_template("login.html")
    return render_template("login.html")

@app.route('/registration',methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        cur = mysql.connection.cursor()
        #checking for user is already have account or not
        users = cur.execute("SELECT * FROM user WHERE name = %s AND email = %s",(name,email))
        if users == 0:
            cur.execute("INSERT INTO `user` (`name`, `email`, `password`) VALUES (%s, %s, %s)",(name,email,password))
            mysql.connection.commit()
            cur.close()
            flash('Registration Successfull,Login Now !')
            return redirect(url_for('login'))
        else:
            flash('Email already Existed !')
            return redirect(url_for('registration'))


    return render_template("registration.html")

@app.route('/teahome')
def teahome():
    
    return render_template("teahome.html")


@app.route('/teapred',methods=['POST','GET'])
def teapred():
    if request.method=='POST':
        upload_image=request.files['file']

        if upload_image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
            upload_image.save(filepath)
            path=filepath
            pred=predict.predict(path)
            p='prediction : '
            print("its path",path)
            return render_template("teapred.html",data=pred,path=path,p=p)
            


    return render_template("teapred.html")

if __name__ == '__main__':
    app.run(debug=True)
