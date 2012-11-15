
import json
import urllib2

END_POINT = 'http://www.uk-postcodes.com/postcode/'

def get(postcode):
    """ requests postcode data from web-service """
    postcode = postcode.replace(' ', '')
    url = '%s%s.json' % (END_POINT, postcode)
    resp = urllib2.urlopen(url)
    return json.loads(resp)


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