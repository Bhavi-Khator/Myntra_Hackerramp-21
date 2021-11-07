from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__);


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
    return render_template('outfits.html')


@app.route('/add')
def add_items():
    return render_template('add_items.html')

@app.route('/form', methods=["POST"])
def form():
    #The url is getting saved
    img_url = request.form.get("img_url");
    # images.append(img_url);
    return redirect('/add')



@app.route('/delete/<id_no>')
def delete_item(id_no):
    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM clothes_for_processing WHERE cloth_id = %s" % (id_no))
    mysql.connection.commit()
    cursor.close()
    return redirect('/create')