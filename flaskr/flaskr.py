import os
import sqlite3
from encode.base import encode, decode
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password'
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
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select * from URLTable')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add/<longurl>')
def add_entry(longurl):
    db = get_db()
    contents = db.execute('select * from URLTable where longURL=(?)',
                 [longurl])
    content = contents.fetchall()
    if(len(content) > 0):
        id = content[0][0]
        counter = content[0][2]
        db.execute('update URLTable set counter = (?) where longURL=(?)',
                 [counter + 1, longurl])
    else:
        db.execute('insert into URLTable (longURL, counter) values(?,?)',
                 [longurl, 0])
        id = db.execute('select id from URLTable where longURL=(?)',
                 [longurl]).fetchall()[0][0]
    db.commit()
    flash(encode(int(id)))
    return redirect(url_for('show_entries'))


@app.route('/parse/<shortHash>')
def parseURL(shortHash):
    db = get_db()
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()