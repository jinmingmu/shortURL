import os, sys
## To import flaskr which in the parent dir
sys.path.append(os.path.join(os.getcwd(), '..'))
from encode.base import encode,decode
import unittest

class BaseTestCase(unittest.TestCase):

    def test_encode(self):
        testNum = 1
        assert '1' == encode(testNum)
        testNum = 100
        assert '1C' == encode(testNum)
        testNum = 999999
        assert '4c91' == encode(testNum)
        
    def test_decode(self):
        testStr = '1'
        assert 1 == decode('1')
        testNum = '1C'
        assert 100 == decode(testNum)
        testNum = '4c91'
        assert 999999 == decode(testNum)


if __name__ == '__main__':
    unittest.main()
