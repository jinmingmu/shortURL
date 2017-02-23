import os
from database.database import db_session, init_db
from encode.base import *
from flask import Flask, request, session, redirect, url_for, abort, jsonify
from database.models import URLTable
import re
app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.route('/')
def main_page():
    addLongURL = request.args.get('add')
    if(addLongURL != None and is_valid_URL(addLongURL)):
        shortURL = add_longURL(addLongURL)
        response = jsonify(
            status=200,
            shortURL=shortURL,
            mimetype='application/json'
        )
        return response

    countLongURL = request.args.get('counter')
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


def add_longURL(longURL):
    content = URLTable.query.filter(URLTable.longURL == longURL).first()
    if(content != None):
        id = content.id
    else:
        newLongURLData = URLTable(longURL, 0)
        db_session.add(newLongURLData)
        db_session.commit()
        id = URLTable.query.filter(URLTable.longURL == longURL).first().id
    return url_for('main_page',_external=True) + encode(id)


def get_counter(longURL):
    content = URLTable.query.filter(URLTable.longURL == longURL).first()
    if(content != None):
        return content.counter
    else:
        return '0'
    
    
@app.route('/<hashValue>')
def parse_URL(hashValue):
    for char in hashValue:
        if(char not in BASE62):
            abort(404)
    entryId = decode(hashValue)
    content = URLTable.query.filter(URLTable.id == entryId).first()
    if(content != None):
        longURL = content.longURL
        content.counter += 1
        db_session.commit()
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
