import os, sys
## To import flaskr which in the parent dir
sys.path.append(os.path.join(os.getcwd(), '..'))
import flaskr
import unittest
import tempfile
import json
import mock
from flask import Flask, url_for
from flask_testing import TestCase
from database.database import db_session, init_db
from database.models import URLTable
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

class FlaskrTestCase( TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db_session.remove()
        self.engine = create_engine('sqlite:///:memory:')
        db_session.configure(bind=self.engine)
        self.metadata = MetaData()
        testTable = Table('URLTable',self.metadata, Column('id', Integer, primary_key=True),Column('longURL', String(300)),Column('counter',Integer))
        self.metadata.create_all(self.engine)
        
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        db_session.remove()
        self.metadata.drop_all(self.engine)


    def test_access_main_page(self):
        rv = self.app.get('/')
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert 'Bad request' in result.get('error')
        assert 400 == result.get('status')

          
    def test_add_long_url_not_in_data_base(self):
        longURL = 'http://www.test.com'
        rv = self.app.get('/?add=' + longURL)
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert 'localhost/1' in result.get('shortURL')
        assert 200 == result.get('status')


    def test_add_long_url_in_data_base(self):
        longURL1 = 'http://www.test.com'
        tempURL = URLTable(longURL1, 100)
        db_session.add(tempURL)
        longURL2 = 'http://www.otherURLAddress'
        tempURL = URLTable(longURL2, 1)
        db_session.add(tempURL)
        db_session.commit()
        rv = self.app.get('/?add=' + longURL1)
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert 'localhost/1' in result.get('shortURL')
        assert 200 == result.get('status')


    def test_get_long_url_counter_in_data_base(self):
        longURL = 'http://www.test.com'
        tempURL = URLTable(longURL, 5)
        db_session.add(tempURL)
        db_session.commit()
        rv = self.app.get('/?counter=' + longURL)
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert '5' == result.get('counter')
        assert 200 == result.get('status')


    def test_get_long_url_counter_not_in_data_base(self):
        longURL = 'http://www.test.com'
        rv = self.app.get('/?counter=' + longURL)
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert '0' == result.get('counter')
        assert 200 == result.get('status')

if __name__ == '__main__':
    unittest.main()

