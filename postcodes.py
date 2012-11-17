import json
import urllib2

END_POINT = 'http://www.uk-postcodes.com'

def _get_json_resp(url):
    resp = urllib2.urlopen(url)
    return json.loads(resp.read())

def get(postcode):
    """ requests postcode data from web-service """
    postcode = urllib2.quote(postcode.replace(' ', ''))
    url = '%s/postcode/%s.json' % (END_POINT, postcode)
    return _get_json_resp(url)

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


class IllegalPointException(Exception):
    """
    Raised when an illegal geographical point is specified in a request.
    """
    pass

class IllegalDistanceException(Exception):
    """
    Raised when an illegal distance is specified in a request.
    """
    pass
        

class PostCoder(object):
    """docstring for PostCoder"""

    def _check_point(self, lat, lng):
        """ Checks if latitude and longitude correct """
        if abs(lat) > 90 or abs(lng) > 180:
            msg = "Illegal lat and/or lng, (%s, %s) provided." % (lat, lng)
            raise IllegalPointException(msg)

    def _lookup(self, skip_cache, fun, *args, **kwargs):
        """ 
        Checks for cached responses, before requesting from 
        web-service
        """
        if args not in self.cache or skip_cache:
            self.cache[args] = fun(*args, **kwargs)
        return self.cache[args]

    def get(self, postcode, skip_cache=False):
        """
        Request data for postcode.

        :param postcode: the postcode to search for. The postcode may 
        contain spaces (they will be removed).

        :param skip_cache: optional argument specifying whether to skip 
        the cache and make an explicit request. Given postcode data 
        doesn't really change, it's unlikely you will ever want to 
        set this to True.

        :returns: a dict of the nearest postcode's data or None if no 
        postcode data is found.
        """
        # remove spaces and change case here due to caching
        postcode = postcode.lower().replace(' ', '')
        return self._lookup(skip_cache, get, postcode)

    def get_nearest(self, lat, lng, skip_cache=False): 
        """
        Request the nearest post code to a geographical point.

        :param lat: latitude of point.

        :param lng: longitude of point.

        :param skip_cache: optional argument specifying whether to skip 
        the cache and make an explicit request.

        :raises IllegalPointException: if the latititude or longitude 
        are out of bounds.

        :returns: a dict of the nearest postcode's data.
        """
        lat, lng = float(lat), float(lng)
        self._check_point(lat, lng)
        return self._lookup(skip_cache, get_nearest, lat, lng)

    def get_from_postcode(self, postcode, distance, skip_cache=False):
        """
        Request all postcode data within `distance` miles of `postcode`.

        :param postcode: the postcode to search for. The postcode may 
        contain spaces (they will be removed).

        :param distance: distance in miles to `postcode`.

        :param skip_cache: optional argument specifying whether to skip 
        the cache and make an explicit request.

        :raises IllegalPointException: if the latititude or longitude 
        are out of bounds.

        :returns: a list of dicts containing postcode data within the 
        specified distance.
        """
        distance = float(distance)
        if distance < 0:
            raise IllegalDistanceException("Distance must not be negative")
        # remove spaces and change case here due to caching
        postcode = postcode.lower().replace(' ', '')
        return self._lookup(skip_cache, get_from_postcode, postcode, 
                            float(distance))

    def get_from_geo(self, lat, lng, distance, skip_cache=False):
        """
        Request all postcode data within `distance` miles of a 
        geographical point.

        :param lat: latitude of point.

        :param lng: longitude of point.

        :param distance: distance in miles to `postcode`.

        :param skip_cache: optional argument specifying whether to skip 
        the cache and make an explicit request.

        :raises IllegalPointException: if the latititude or longitude 
        are out of bounds.

        :returns: a list of dicts containing postcode data within the 
        specified distance.
        """
        # remove spaces and change case here due to caching
        lat, lng, distance = float(lat), float(lng), float(distance)
        if distance < 0:
            raise IllegalDistanceException("Distance must not be negative")
        self._check_point(lat, lng)
        return self._lookup(skip_cache, get_from_geo, lat, lng, distance)


    def __init__(self):
        self.cache = {}

