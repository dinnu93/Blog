from flask import *
import sqlite3
import time
app = Flask(__name__)

@app.route('/')
def index():
	list_of_articles = db_connect()
	print list_of_articles
	return render_template('index.html', articles = list_of_articles ,summary = summary)

def summary(article):
	pos = article.find(" ",250)
	return article[:pos]

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	if request.method == 'POST':
		title_title = request.form['title']
		article_article = request.form['article']
		time_time = time.ctime()
		time_list = time_time.split()
		del time_list[3]
		time_time = " ".join(time_list)
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
	return render_template("WorkInProgress.html")

@app.route('/projects')
def projects():
	return render_template("WorkInProgress.html")

@app.route('/contact')
def contact():
	return render_template("WorkInProgress.html")


	

def db_connect():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute('SELECT id,title,article,time FROM blog order by id DESC')
	list_of_articles = c.fetchall()
	conn.close()
	return list_of_articles

if __name__ == '__main__':
    app.run(debug=True)
   

