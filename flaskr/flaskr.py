import os
from database.database import db_session, init_db
from encode.base import *
from flask import Flask, request, session, redirect, url_for, abort, jsonify
from database.models import URLTable
import re
app = Flask(__name__)
## The configuration of this app
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))

## Run app in silence mode
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    @fn shutdown_session
    remove the database session
    """
    db_session.remove()


@app.cli.command('initdb')
def initdb_command():
    """
    @fn initdb_command
    init the database, you can run flask command initdb to run this function
    """
    init_db()
    print('Initialized the database.')


@app.route('/')
def main_page():
    """
    @fn main_page
    handle add and counter request
    @return response
    if your request is add or counter, it will return a json file with requested data
    otherwise it will return status code 400 with error message
    """
    ## Only allow one command each time 
    if(len(request.args) > 1):
        return jsonify(
                status=400,
                error='Bad request'
                )

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
    """
    @fn add_longURL
    add the longURL to database if it is not in database.
    @param longURL
    the url string
    @return
    the short url web address
    """
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
    """
    @fn get_counter
    get the longURL counter from database.
    @param longURL
    the url string
    @return
    value of counter if it is in database
    0 if it is not in database
    """
    content = URLTable.query.filter(URLTable.longURL == longURL).first()
    if(content != None):
        return content.counter
    else:
        return '0'
    
    
@app.route('/<hashValue>')
def parse_URL(hashValue):
    """
    @fn parse_URL
    check whether hash is valid, then get the id from database. If the id is in database, redirect to longURL.
    If id is not in database or input is invalid, abort 404
    @param hashValue
    the hashed address value
    @return
    redirect the website to longURL if it is in database
    abort 404 is it is not in database
    """
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
    """
    @fn is_valid_URL
    use regular expression to check whether input url is valid
    @param url
    url string
    @return
    True if it is valid
    False if it is not valid
    """
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run()
