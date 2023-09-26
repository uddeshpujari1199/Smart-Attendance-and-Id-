from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
image = Image.new('RGB', (1200,900), (255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('arial.ttf', size=45)
from time import sleep
import random
import os
import datetime
from datetime import timedelta
import pyqrcode
from flask_mysqldb import MySQL
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, g
import os
from second import second
import itertools
import smtplib

app = Flask(__name__)
Bootstrap(app)
app.permanent_session_lifetime = timedelta(minutes=3)
app.register_blueprint(second, url_prefix="/admin")

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'

mysql.init_app(app)

name="uddesh"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        session.permanent = True
        l_EMAil=request.form['l_EMAil']
        session["l_EMAil"] = l_EMAil
        
        password=request.form['password']
        
       # if request.form['password'] == 'password':
            #session['l_EMAil'] = request.form['l_EMAil']
            
            
        

        cur = mysql.connection.cursor()
        result=cur.execute("SELECT PASS FROM register WHERE EMail=%s",(l_EMAil,))
       
        
        data=cur.fetchall()
        for row in data:
            
            
            auth_pass=row[0]
            
        
        if result>0 and password==auth_pass:

            return redirect('dashboard.html')
        
        else:
            
            flash(" plase check your email or password ")

        #if data:
            #session['loggedin']= True
            #session['id']= data['id']
            #session['l_EMAil']= data['l_EMAil']
            #return redirect('dashboard.html')
       # else:
            #flash(" plase check your email or password ")
            
            
        
        mysql.connection.commit()
        cur.close()




        
     
    return render_template('login.html' )


#@app.before_request
#def before_request():
    
    #g.l_EMAil = None

    #if 'l_EMAil' in session:
        #g.l_EMAil = session['l_EMAil']



        

@app.route('/signup.html', methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        
        name=request.form['name']
        email=request.form['email']
        contact=request.form['contact']
        password=request.form['password']
        DOB=request.form['DOB']
        address=request.form['address']

        if not len(password) >= 8:
            flash("password is must be 8 charecters in length")
            return redirect(request.url)
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO register(user, EMail, PASS, contact, address, DOB) VALUES( %s, %s, %s, %s, %s, %s)",(name, email,  password, contact, address, DOB))
            mysql.connection.commit()
            cur.close()
            

       

            flash("Account created susssefully!")
            return redirect('login.html')
   
        
    return render_template('signup.html')
           
@app.route('/dashboard.html',methods=['POST','GET'])
def dashboard():
    if "l_EMAil" in session:
        l_EMAil = session["l_EMAil"]
        
        return render_template('dashboard.html',l_EMAil=l_EMAil)
    else:
        
        return redirect('login.html')

    #if request.method == 'POST':
        #cur = mysql.connection.cursor()
        #cur.execute("SELECT * FROM register")
        #data2 = cur.fetchall()
        #ud="uddsh"
        
        #return render_template('dashboard.html',data=data2)
    
    return render_template('dashboard.html')    
    

@app.route('/id_generation2.html', methods=['POST','GET'])
def idgenrat():
    if request.method == 'POST':
        (x, y) = (320, 50)
        company='UD ENTERPRISE'
        color = 'rgb(0, 0, 0)'
        bgcolor='rgb(0, 0, 0)'
        font = ImageFont.truetype('arial.ttf', size=50)
        draw.text((x, y), company, fill=color, font=font, bgcolor=bgcolor)


        # adding an unique id number. You can manually take it from user
        (x, y) = (50, 240)
        idno=random.randint(10000000,90000000)
        message = "Id: "+str('ID '+str(idno))
        ID=str(company)+str(idno)
        color = 'rgb(0, 0, 0)' # black color
        font = ImageFont.truetype('arial.ttf', size=35)
        draw.text((x, y), message, fill=color, font=font)

        # add pic in id
        
        profile = request.files['profo']
        
        ud=profile.save(ID+".bmp")

        #ud=Image.open(ID+".jpg")
     
        #box=(150,200,600,600)
        #cropped_images = image.crop(box)
        #cropped_image.save('croped.image.bmp')

        # add name in id
        (x, y) = (50, 310)
        name = request.form['ID_name']
        msg="Name: "+name
        color = 'rgb(0, 0, 0)' # black color
        font = ImageFont.truetype('arial.ttf', size=30)
        draw.text((x, y), msg, fill=color, font=font)


        # add name in age
        (x, y) = (50, 380)
        age = request.form['ID_age']
        message="Age: "+age
        color = 'rgb(0, 0, 0)' # black color 
        draw.text((x, y), message, fill=color, font=font)

        # add name in dob

        (x, y) = (50, 450)
        dob = request.form['ID_DOB']
        message="Dob: "+dob
        color = 'rgb(0, 0, 0)' # black color 
        draw.text((x, y), message, fill=color, font=font)


        # add name in contact
        (x, y) = (50, 520)
        contact = request.form['ID_contact']
        message="Contact: "+contact
        color = 'rgb(0, 0, 0)' # black color 
        draw.text((x, y),message, fill=color, font=font)

        # add name in email
        (x, y) = (50, 590)
        email = request.form['ID_email']
        message="E-mail: "+email
        color = 'rgb(0, 0, 0)' # black color 
        draw.text((x, y), message, fill=color, font=font)

        cur = mysql.connection.cursor()
        cur.execute("SELECT Email2 FROM pydata")
        data = cur.fetchall()

        emailv=[]
        for row in data:
            emailv.append(row)
        emailv2=list(itertools.chain(*emailv))
        print(emailv2)

        if email in emailv2:
            flash("use registered email")
            return redirect("id_generation2.html")


        
                         
       
                         
                     
    
                    

        (x, y) = (50, 700)
        address = request.form['ID_address']
        message="Add: "+address
        color = 'rgb(0, 0, 0)' # black color 
        draw.text((x, y), message, fill=color, font=font)




        # save the edited image
         
        image.save(str(name)+'.bmp')



        img = pyqrcode.create(str(company)+str(idno))# this info. is added in QR code, also add other things
        img.png(str(idno)+'.bmp',scale=9)


        im = Image.open(str(idno)+'.bmp')
        img_with_border = ImageOps.expand(im,border=8,fill='black') # adding border to qr code
        img_with_border.save(str(idno)+'.bmp')


        til = Image.open(name+'.bmp')
        img_with_border = ImageOps.expand(til,border=15,fill='black') # adding border to ID
        img_with_border.save(name+'.bmp')

        til = Image.open(name+'.bmp')
        im = Image.open(str(idno)+'.bmp')     # ID generation
        sym = Image.open("symbol.bmp")
        pic = Image.open(ID+".bmp")
        til.paste(sym,(50,50)) #symbol
        til.paste(pic,(880,50)) # profile
        til.paste(im,(790,340))
        til.save(name+'.bmp')
         
        
        cur = mysql.connection.cursor()
        cur.execute( "INSERT INTO pydata(ID, company, name, age, dob, contact, Email2, address, pro) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(ID, company, name, age, dob, contact, email, address, profile))
        mysql.connection.commit()
        cur.close()

        flash("id created succesfully")

       

         

        

        
    return render_template("id_generation2.html")
email=session["l_EMAil"]

def sendEmail(to, content):
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('uddesh.pujari123@gmail.com', '8898702274 ')
    server.sendmail('uddesh.pujari123@gmail.com', to, content)
    server.close()

sendEmail(email,"good evening")


    


@app.route('/about.html')
def about():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM register")
    data2 = cur.fetchall()
    
    return render_template('about.html',name=name,data=data2)

@app.route('/employee_A.html')
def employee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM register")
    data2 = cur.fetchall()
    
    return render_template("employee_A.html",data=data2)

@app.route('/logout')
def logout():
    session.pop("l_EMAil",None)
    return redirect(url_for("login"))





if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
