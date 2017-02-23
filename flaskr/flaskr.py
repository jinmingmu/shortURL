import os
import sqlite3
from encode.base import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, abort, jsonify
import re
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
    
@app.route('/')
def main_page():
    addLongURL = request.args.get('add')
    print addLongURL
    if(addLongURL != None and is_valid_URL(addLongURL)):
        shortURL = add_longUrl(addLongURL)
        response = jsonify(
            status=200,
            shortURL=shortURL,
            mimetype='application/json'
        )
        return response

    countLongURL = request.args.get('count')
    if(countLongURL != None and is_valid_URL(countLongURL)):
        counter = get_counter(countLongURL)
        response = jsonify(
            status=200,
            counter=counter,
            mimetype='application/json'
        )
        return response

    return jsonify(
            status=400,
            error='Bad request'
            )

def add_longUrl(longURL):
    db = get_db()
    contents = db.execute('select * from URLTable where longURL=(?)',[longURL])
    content = contents.fetchall()
    if(len(content) > 0):
        id = content[0][0]
    else:
        db.execute('insert into URLTable (longURL, counter) values(?,?)',[longURL, 0])
        id = db.execute('select id from URLTable where longURL=(?)',[longURL]).fetchall()[0][0]
        db.commit()
    return url_for('main_page',_external=True) + encode(id)

def get_counter(longURL):
    db = get_db()
    contents = db.execute('select counter from URLTable where longURL=(?)',[longURL])
    db.commit()
    content = contents.fetchall()
    print content
    if(len(content) > 0):
        return str(content[0][0])
    else:
        return '0'
    
    
@app.route('/<hashValue>')
def parse_URL(hashValue):
    for char in hashValue:
        if(char not in BASE62):
            abort(404)
    entryId = decode(hashValue)
    db = get_db()
    contents = db.execute('select * from URLTable where id=(?)',
                 [entryId])
    content = contents.fetchall()
    if(len(content) > 0):
        longURL = content[0][1]
        counter = content[0][2]
        db.execute('update URLTable set counter = (?) where id=(?)',[counter + 1, entryId])
        db.commit()
        return redirect(longURL)
    else:
        abort(404)

def is_valid_URL(url):
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()
