from flask import *
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
	list_of_articles = db_connect()
	return render_template('index.html', articles = list_of_articles ,summary = summary)

def summary(article):
	pos = article.find(" ",250)
	return article[:pos]

@app.route('/newpost',methods=['GET','POST'])
def newpost():
	if request.method == 'POST':
		title_title = request.form['title']
		article_article = request.form['article']
		conn = sqlite3.connect('example.db')
		c = conn.cursor()
		c.execute('INSERT INTO blog VALUES (NULL, ?, ?)',(title_title,article_article))
		conn.commit()
		conn.close
		return redirect(url_for('index'))
	return render_template('newpost.html')

@app.route('/post/<id>')
def post(id):
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute('SELECT title,article FROM blog where id = %s'%id)
	title,article = c.fetchone()
	conn.close()
	return render_template('post.html',title = title,article = article)


def db_connect():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	c.execute('SELECT id,title,article FROM blog order by id DESC')
	list_of_articles = c.fetchall()
	conn.close()
	return list_of_articles

if __name__ == '__main__':
    app.run()
   

