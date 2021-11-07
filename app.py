from flask import Flask, render_template, request, redirect

app = Flask(__name__);


images = []

@app.route('/')
def home():
    return render_template("home.html");

@app.route('/details')
def add_details():
    return render_template("add_details.html");

@app.route('/create')
def order():
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
    images.append(img_url);
    return redirect('/add')