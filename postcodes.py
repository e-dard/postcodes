
import json
import urllib2

END_POINT = 'http://www.uk-postcodes.com/'

def _get_json_resp(url):
    resp = urllib2.urlopen(url)
    return json.loads(resp)

def get(postcode):
    """ requests postcode data from web-service """
    postcode = urllib2.quote(postcode.replace(' ', ''))
    url = '%s/postcode/%s.json' % (END_POINT, postcode)
    resp = urllib2.urlopen(url)
    return json.loads(resp)

def get_nearest(lat, lng):
    """ Return the nearest postcode to the lat-long point provided """
    url = '%s/latlng/%s,%s.json' % (END_POINT, lat, lng)
    return _get_json_resp(url)

def _get_from(distance, *dist_params):
    params = '&'.join([p for p in dist_params])
    query = '%s&distance=%s&format=%s' % (params, distance, 'json')
    url = '%s/distance.php?%s' % (END_POINT, query)
    return _get_json_resp(url)

def get_from_postcode(postcode, distance):
    """ return all postcodes within `distance` miles of `postcode` """
    postcode = urllib2.quote(postcode.replace(' ', ''))
    return _get_from(distance, 'postcode=%s' % postcode)

def get_from_geo(lat, lng, distance):
    """ 
    Return all postcodes within `distance` miles of the `lat` `lng` 
    pair.
    """
    return _get_from(distance, 'lat=%s' % lat, 'lng=%s' % lng)

class PostCoder(object):
    """docstring for PostCoder"""

    def find(self, postcode, skip_cache=False):
        """
        Request data for postcode. The postcode can have spaces or not.

        :param postcode: the postcode to search for
        :param skip_cache: optional argument specifying whether to skip 
        the cache and make a guarenteed external request. Given postcode 
        data doesn't really change, it's unlikely you will ever want to 
        set this to true.
        """
        if postcode not in self.cache or skip_cache:
            hit = get(postcode)
            self.cache[postcode] = hit
        return self.cache[postcode]

    def __init__(self):
        self.cache = {}