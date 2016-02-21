from flask import *
import sqlite3
from datetime import date
import requests
import os
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
		article_article = article_article.replace("\n","<br>")
		d_time = date.today()
		time_time = d_time.strftime("%B %d, %Y")
		conn = sqlite3.connect('/var/www/FlaskApps/Blog/example.db')
		c = conn.cursor()
		c.execute('INSERT INTO blog VALUES (NULL, ?, ?, ?)',(title_title,article_article,time_time))
		conn.commit()
		conn.close
		return redirect(url_for('index'))
	return render_template('newpost.html')

@app.route('/post/<id>')
def post(id):
	conn = sqlite3.connect('/var/www/FlaskApps/Blog/example.db')
	c = conn.cursor()
	c.execute('SELECT title,article,time FROM blog where id = %s'%id)
	title,article,time = c.fetchone()
	conn.close()
	return render_template('post.html',title = title,article = article)

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

def db_connect():
	conn = sqlite3.connect('/var/www/FlaskApps/Blog/example.db')
	c = conn.cursor()
	c.execute('SELECT id,title,article,time FROM blog order by id DESC')
	list_of_articles = c.fetchall()
	conn.close()
	return list_of_articles

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)
   

