from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from PIL import ImageGrab
from datetime import datetime, timedelta
from math import log
import time
import webbrowser

app = Flask(__name__);

epoch = datetime(1970, 1, 1)
def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
def score(ups, downs):
    return ups - downs


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myntra_hackerramp'
 
mysql = MySQL(app)


@app.route('/')
def home(): 
    return render_template("home.html");

@app.route('/details')
def add_details():
    return render_template("add_details.html");

@app.route('/create')
def order():
    cursor = mysql.connection.cursor()
    cursor.execute(" SELECT * FROM clothes_for_processing")
    images = []
    for cloth_url in cursor:
        images.append(cloth_url)
    cursor.close()
    return render_template('order.html', images = images);


@app.route('/browse')
def outfits():
    cursor1 = mysql.connection.cursor()
    cursor1.execute(" SELECT * FROM votes_table ORDER BY position DESC")
    images = []
    for cloth_url in cursor1:
        images.append(cloth_url) 
    cursor1.close()

    return render_template('outfits.html', outfits=images)
    
@app.route('/update')
def change_position():
    cursor1 = mysql.connection.cursor()
    cursor1.execute(" SELECT upvotes, downvotes, date_created, clothes_id FROM votes_table")
    outfits = []
    for outfit in cursor1:
        outfits.append(outfit)
    for outfit in outfits:
        s = score(outfit[0], outfit[1])
        order = log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = epoch_seconds(outfit[2]) - 1134028003
        p = round(sign * order + seconds / 45000, 7)
        p = p/1000
        print(p)
        id = outfit[3]
        cursor1.execute("UPDATE votes_table SET position=%f WHERE clothes_id = %s" % (p, id))
        mysql.connection.commit()
    cursor1.close()
    return redirect('/browse')

@app.route('/add')
def add_items():
    return render_template('add_items.html')

@app.route('/form', methods=["POST"])
def form():
    #The url is getting saved
    img_url = request.form.get("img_url");
    # images.append(img_url);
    return redirect('/add')


@app.route('/check')
def check():
    image = ImageGrab.grab(bbox=(950,120,1800,900))
    image.save('./static/images/1.png')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from clothes_for_processing")
    s = ""
    for url in cursor:
        s = s + "," + url[1]
    s = s[1:]
    #cursor.execute("Insert into votes_table values(default, 'https://i.ibb.co/0Fpky4z/Outfit3.jpg', now(), 0, 0, 11.162433 , %s)" % (s));
    mysql.connection.commit()
    cursor.close()
    return redirect('/browse')

@app.route('/delete/<id_no>')
def delete_item(id_no):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clothes_for_processing WHERE cloth_id = %s" % (id_no))
    mysql.connection.commit()
    cursor.close()
    return redirect('/create')


@app.route('/upvote/<id>')
def upvote(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE votes_table SET upvotes=upvotes+1 WHERE clothes_id = %s" % (id))
    mysql.connection.commit()
    cursor.close()
    return redirect('/browse')


@app.route('/downvote/<id>')
def downvote(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE votes_table SET downvotes=downvotes+1 WHERE clothes_id = %s" % (id))
    mysql.connection.commit()
    cursor.close()
    return redirect('/browse')

@app.route('/show/<id>')
def show(id):
    cursor = mysql.connection.cursor()
    cursor.execute(" SELECT * FROM votes_table WHERE clothes_id = %s" % (id))
    for id in cursor:
        names = id[6]
    print(names)
    urls = names.split(',')
    print(urls)
    for i in range(len(urls)):
        webbrowser.open_new_tab(urls[i])
    return redirect('/browse')
