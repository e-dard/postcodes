import unittest

from mock import patch, call

import postcodes
from postcodes import PostCoder, IllegalPointException, \
                      IllegalDistanceException

class TestPostCodes(unittest.TestCase):

    def setUp(self):
        pass

    @patch('postcodes._get_json_resp')
    def test_get(self, mock):
        """ Tests postcodes.get """
        postcodes.get("foo")
        exp = "http://www.uk-postcodes.com/postcode/foo.json"
        mock.assert_called_once_with(exp)

    @patch('postcodes._get_json_resp')
    def test_get_nearest(self, mock):
        """ Tests postcodes.get_nearest """
        postcodes.get_nearest(1.1, -2.2)
        exp = "http://www.uk-postcodes.com/latlng/1.1,-2.2.json"
        mock.assert_called_once_with(exp)

    @patch('postcodes._get_json_resp')
    def test__get_from(self, mock):
        """ Tests postcodes._get_from """
        postcodes._get_from(1, 'foo=bar', 'zoo=boo')
        exp = "http://www.uk-postcodes.com/distance.php?"\
              "foo=bar&zoo=boo&distance=1&format=json"
        mock.assert_called_once_with(exp)

    @patch('postcodes._get_json_resp')
    def test_get_from_postcode(self, mock):
        """ Tests postcodes.get_from_postcode """
        postcodes.get_from_postcode('W1 1', 1)
        exp = "http://www.uk-postcodes.com/distance.php?"\
              "postcode=W11&distance=1&format=json"
        mock.assert_called_once_with(exp)

    @patch('postcodes._get_json_resp')
    def test_get_from_geo(self, mock):
        """ Tests postcodes.get_from_geo """
        postcodes.get_from_geo(1, 2, 1)
        exp = "http://www.uk-postcodes.com/distance.php?"\
              "lat=1&lng=2&distance=1&format=json"
        mock.assert_called_once_with(exp)


class TestPostCoder(unittest.TestCase):
    def setUp(self):
        self.pc = PostCoder()

    def tearDown(self):
        pass

    def test__check_point(self):
        """ Tests postcodes._check_point """
        f = self.pc._check_point
        self.assertRaises(IllegalPointException, f, -91, 181)               
        self.assertRaises(IllegalPointException, f, 90.1, -180.1)
        self.assertIsNone(f(0,0))

    @patch('postcodes.get')
    def test_get(self, mock):
        """ Tests PostCoder.get """
        self.pc.get("F0 0BA")
        self.pc.get("F00BA") # should use cache
        self.pc.get("f00b a") # should use cache
        mock.assert_called_once_with("f00ba")
        self.pc.get("f00b a", skip_cache=True)
        mock.assert_has_calls([call("f00ba"), call("f00ba")])

    @patch('postcodes.get_nearest')
    def test_get_nearest(self, mock):
        """ Tests PostCoder.get_nearest """
        self.pc.get_nearest(0, 0)
        self.pc.get_nearest(0, 0, skip_cache=True)
        mock.assert_has_calls([call(0, 0), call(0, 0,)]) 
        self.assertRaises(IllegalPointException, self.pc.get_nearest, -91, 0)

    @patch('postcodes.get_from_postcode')
    def test_get_from_postcode(self, mock):
        """ Tests PostCoder.get_from_postcode """
        self.pc.get_from_postcode("F0 0BA", 1.1)
        self.pc.get_from_postcode("F00BA", "12.32")
        self.pc.get_from_postcode("F00BA", 12.32) # use cache
        mock.assert_has_calls([call("f00ba", 1.1), call("f00ba", 12.32)])
        
        mock.reset_mock()
        self.pc.get_from_postcode("F00BA", 12.32, skip_cache=True)
        mock.assert_called_once_with("f00ba", 12.32)
        self.assertRaises(IllegalDistanceException, self.pc.get_from_postcode, 
                          None, -11)

    @patch('postcodes.get_from_geo')
    def test_get_from_geo(self, mock):
        """ Tests PostCoder.get_from_geo """
        self.pc.get_from_geo(-40, 100, 1)
        self.pc.get_from_geo("-30", "20", "12")
        self.pc.get_from_geo(-30, 20, 12)
        mock.assert_has_calls([call(-40, 100, 1), call(-30, 20, 12)])
        
        mock.reset_mock()
        self.pc.get_from_geo(-30, 20, 12, skip_cache=True)
        mock.assert_called_once_with(-30, 20, 12)
        f = self.pc.get_from_geo
        self.assertRaises(IllegalPointException, f, 91, 0, 0)
        self.assertRaises(IllegalDistanceException, f, -30, 20, -11)





