# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__, static_url_path='/static') # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:////db/fs.db'
db = SQLAlchemy(app)
app.config.from_envvar('POTZY_SETTINGS', silent=True)


@app.route('/',methods=['GET','POST'])
def index():
	stock = request.form.get('stock-select')
	item = request.form.get('item-select')
	return render_template("index.html",stock=stock,item=item)

@app.route("/test" , methods=['GET', 'POST'])
def test():
	select = request.form.get('stock-select')
	return(str(select)) 	

@app.route("/api/<stock>/<item>")
def get_stock_item(stock,item):

    # My code here to get the time series of <item> for <stock>

    ##load database


    ## query stock

	return data

@app.route("/")