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
        metadata = MetaData()
        self.url = Table('URLTable',metadata, Column('id', Integer, primary_key=True),Column('longURL', String(300)),Column('counter',Integer))
        metadata.create_all(self.engine)
        self.url = URLTable("http://www.test.com", 0)
        db_session.add(self.url)
        db_session.commit()
        
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        db_session.remove()


    def test_access_main_page(self):
        rv = self.app.get('/')
        assert '200 OK' == rv.status
        result = json.loads(rv.data)
        assert 'Bad request' in result.get('error')
        assert 400 == result.get('status')

          
    def test_add_long_url_not_int_data_base(self):
        longURL = 'http://www.test.com'
        rv = self.app.get('/?add=' + longURL)
        assert '200 OK' == rv.status
        result = json.loads(rv.data)

if __name__ == '__main__':
    unittest.main()

