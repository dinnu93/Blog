from flask import *
import sqlite3
from datetime import date
import requests
app = Flask(__name__)

@app.route('/')
def index():
	list_of_articles = db_connect()
	print list_of_articles
	return render_template('index.html', articles = list_of_articles ,summary = summary)

def summary(article):
	pos = article.find(" ",300)
	return article[:pos]

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	if request.method == 'POST':
		title_title = request.form['title']
		article_article = request.form['article']
		d_time = date.today()
		time_time = d_time.strftime("%B %d, %Y")
		conn = sqlite3.connect('example.db')
		c = conn.cursor()
		c.execute('INSERT INTO blog VALUES (NULL, ?, ?, ?)',(title_title,article_article,time_time))
		conn.commit()
		conn.close
		return redirect(url_for('index'))
	return render_template('newpost.html')

@app.route('/post/<id>')
def post(id):
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute('SELECT title,article,time FROM blog where id = %s'%id)
	title,article,time = c.fetchone()
	conn.close()
	return render_template('post.html',title = title,article = article)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/projects')
def projects():
	return render_template("WorkInProgress.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/hyd',methods=['GET','POST'])
def local():
	if request.method == 'POST':
		locality = request.form['locality']
		lat,lng,polyCoord = code(locality)
		return render_template("hyd.html",locality = locality,lat = lat,lng = lng, polyCoord = polyCoord)
	else:
		return render_template("hyd.html",locality="Hyderabad",lat = 17.385044,lng = 78.486671, polyCoord =[{'lat': 17.2168886, 'lng': 78.1599217}, {'lat': 17.2168886, 'lng': 78.6561694}, {'lat': 17.6078088, 'lng': 78.6561694}, {'lat': 17.6078088, 'lng': 78.1599217}, {'lat': 17.2168886, 'lng': 78.1599217}] )

@app.route('/hyderabad',methods=['GET','POST'])
def locality():
	if request.method == 'POST':
		locality = request.form['locality']
		lat,lng,polyCoord = code(locality)
		return render_template("hyderabad.html",locality = locality,lat = lat,lng = lng)
	else:
		return render_template("hyderabad.html",locality="Hyderabad",lat = 17.385044,lng = 78.486671)


def code(locality):
	url = "https://maps.googleapis.com/maps/api/geocode/json"
	key = "AIzaSyC3ugnQvcHCgvybxUXClZIACZMnbDxfmrk"
	payload = {'key': key,'address': locality+", Hyderabad, Telangana, India"}
	r = requests.get(url, params=payload)
	json = r.json()
	lat =json['results'][0]['geometry']['location']['lat']
	lng = json['results'][0]['geometry']['location']['lng']
	lat_sw,lng_sw = json['results'][0]['geometry']['bounds']['southwest']['lat'],json['results'][0]['geometry']['bounds']['southwest']['lng']
	lat_ne,lng_ne = json['results'][0]['geometry']['bounds']['northeast']['lat'],json['results'][0]['geometry']['bounds']['northeast']['lng']
	polyCoord = []
	polyCoord.append({'lat':lat_sw,'lng':lng_sw})
	polyCoord.append({'lat':lat_sw,'lng':lng_ne})
	polyCoord.append({'lat':lat_ne,'lng':lng_ne})
	polyCoord.append({'lat':lat_ne,'lng':lng_sw})
	polyCoord.append({'lat':lat_sw,'lng':lng_sw})
	return lat,lng,polyCoord

def db_connect():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute('SELECT id,title,article,time FROM blog order by id DESC')
	list_of_articles = c.fetchall()
	conn.close()
	return list_of_articles

if __name__ == '__main__':
    app.run(debug=True)
   

