import os
import sqlite3
from encode.base import encode, decode
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, abort
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
	
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db	
	
	
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()	
	
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
		
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')
    
@app.route('/', methods=['POST'])
def add_entry():
    if request.headers['Content-Type'] == 'text/plain':
        longurl = request.data
        db = get_db()
        contents = db.execute('select * from URLTable where longURL=(?)',
                 [longurl])
        content = contents.fetchall()
        if(len(content) > 0):
            id = content[0][0]
            counter = content[0][2]
            db.execute('update URLTable set counter = (?) where longURL=(?)',[counter + 1, longurl])
        else:
            db.execute('insert into URLTable (longURL, counter) values(?,?)',[longurl, 0])
            id = db.execute('select id from URLTable where longURL=(?)',[longurl]).fetchall()[0][0]
        db.commit()
    else:
        print "please send post request with text/plain content type"
    return url_for('add_entry',_external=True) + encode(id)


@app.route('/<hashValue>')
def parseURL(hashValue):
    entryId = decode(hashValue)
    db = get_db()
    contents = db.execute('select * from URLTable where id=(?)',
                 [entryId])
    content = contents.fetchall()
    if(len(content) > 0):
        longURL = content[0][1]
        counter = content[0][2]
        db.execute('update URLTable set counter = (?) where id=(?)',[counter + 1, entryId])
        return longURL 
    else:
        abort(404)

if __name__ == '__main__':
    app.run()
