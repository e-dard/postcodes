import json
import sys

if sys.version_info.major < 3:
    from urllib2 import quote, URLError, urlopen
else:
    from urllib.error import URLError
    from urllib.parse import quote
    from urllib.request import urlopen

END_POINT = 'http://www.uk-postcodes.com'

def _get_json_resp(url):
    try:
        resp = urlopen(url)
    except URLError as e:
        if e.code == 404: # no available data   
            return None
    else:
        return json.loads(resp.read().decode('utf-8'))

def get(postcode):
    """
    Request data associated with `postcode`.

    :param postcode: the postcode to search for. The postcode may 
                     contain spaces (they will be removed).

    :returns: a dict of the nearest postcode's data or None if no 
              postcode data is found.
    """
    postcode = quote(postcode.replace(' ', ''))
    url = '%s/postcode/%s.json' % (END_POINT, postcode)
    return _get_json_resp(url)

def get_nearest(lat, lng):
    """
    Request the nearest `postcode` to a geographical point, 
    specified by `lat` and `lng`.

    :param lat: latitude of point.

    :param lng: longitude of point.

    :returns: a dict of the nearest postcode's data.
    """
    url = '%s/latlng/%s,%s.json' % (END_POINT, lat, lng)
    return _get_json_resp(url)

def _get_from(distance, *dist_params):
    params = '&'.join([p for p in dist_params])
    query = '%s&distance=%s&format=%s' % (params, distance, 'json')
    url = '%s/distance.php?%s' % (END_POINT, query)
    return _get_json_resp(url)

def get_from_postcode(postcode, distance):
    """
    Request all postcode data within `distance` miles of `postcode`.

    :param postcode: the postcode to search for. The postcode may 
                     contain spaces (they will be removed).

    :param distance: distance in miles to `postcode`.

    :returns: a list of dicts containing postcode data within the 
              specified distance or `None` if `postcode` is not valid.
    """
    postcode = quote(postcode.replace(' ', ''))
    return _get_from(distance, 'postcode=%s' % postcode)

def get_from_geo(lat, lng, distance):
    """
    Request all postcode data within `distance` miles of a 
    geographical point specified by `lat` and `lng`.

    :param lat: latitude of point.

    :param lng: longitude of point.

    :param distance: distance in miles to `postcode`.

    :returns: a list of dicts containing postcode data within the 
              specified distance.
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
    """
    The `PostCoder` object provides state for maintaining a cache of 
    historical requests. It's the recommended way to interact with the 
    underlying web-service.

    Because `PostCoder` caches all previously requested postcode data 
    it's fine to repeatedly request the same data as much as you like, 
    and you don't need to worry about explicitly storing any data in 
    your application. 

    Because the underlying data is not likely to change very much, if 
    at all, cached postcode data never expires. However, if for some 
    perverse reason you do want to skip the cache and make an explicit 
    request for data then you can set ``skip_cache=True`` in all of the 
    available methods. 

    """

    def __init__(self):
        self.cache = {}

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
        Calls `postcodes.get` and by default utilises a local cache.
        
        :param skip_cache: optional argument specifying whether to skip 
                           the cache and make an explicit request. 
                           Given postcode data doesn't really change, 
                           it's unlikely you will ever want to set this 
                           to `True`.
        """
        # remove spaces and change case here due to caching
        postcode = postcode.lower().replace(' ', '')
        return self._lookup(skip_cache, get, postcode)

    def get_nearest(self, lat, lng, skip_cache=False): 
        """
        Calls `postcodes.get_nearest` but checks correctness of `lat` 
        and `long`, and by default utilises a local cache.

        :param skip_cache: optional argument specifying whether to skip 
                           the cache and make an explicit request.

        :raises IllegalPointException: if the latitude or longitude 
                                       are out of bounds.

        :returns: a dict of the nearest postcode's data.
        """
        lat, lng = float(lat), float(lng)
        self._check_point(lat, lng)
        return self._lookup(skip_cache, get_nearest, lat, lng)

    def get_from_postcode(self, postcode, distance, skip_cache=False):
        """
        Calls `postcodes.get_from_postcode` but checks correctness of 
        `distance`, and by default utilises a local cache.

        :param skip_cache: optional argument specifying whether to skip 
                           the cache and make an explicit request.

        :raises IllegalPointException: if the latitude or longitude 
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
        Calls `postcodes.get_from_geo` but checks the correctness of 
        all arguments, and by default utilises a local cache.

        :param skip_cache: optional argument specifying whether to skip 
                           the cache and make an explicit request.

        :raises IllegalPointException: if the latitude or longitude 
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


