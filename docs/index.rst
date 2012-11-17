.. postcodes documentation master file, created by
   sphinx-quickstart on Sat Nov 17 11:27:27 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Postcodes
*********
.. module:: postcodes

Postcodes is a small library for getting information about, postcodes 
in the UK. At its core, the postcode data is provided by the 
`Ordnance Survey OS OpenData`_ initiative, but this library is actually a
wrapper for a `web\-service`_ provided by `Stuart Harrison`_.

.. _Stuart Harrison: http://twitter.com/pezholio
.. _web-service: http://www.uk-postcodes.com/
.. _Ordnance Survey OS OpenData: http://www.ordnancesurvey.co.uk/oswebsite/products/os-opendata.html


Installation
============

If you use pip then installation is simply::

    $ pip install postcodes

or, if you want the latest github version::

    $ pip install git+git://github.com/e-dard/postcodes.git

You can also install Postcodes via Easy Install::

    $ easy_install postcodes

    
Features
========
Postcodes allows you to do the following:

* Lookup the postcode data associated with a specific postcode;
* Get the nearest postcode data associated to a specific geographical 
  point;
* Get all of the postcode data within a specific distance to a 
  geographical point;
* Get all of the postcode data within a specific distance to a 
  known postcode.

As well as being a thin wrapper over the `uk-postcodes`_ `web-service`_, 
Postcodes also provides a simple caching and validation layer, in the 
form of the `PostCoder` object, meaning you don't have to worry about 
keeping track of any previously requested data.

.. _uk-postcodes: http://www.uk-postcodes.com/

Usage
-----

Postcodes is very simple. Simply create a new `PostCoder` object and 
away you go:

.. code-block:: pycon

    >>> from pprint import PrettyPrinter
    >>> from postcodes import PostCoder
    >>>
    >>> pc = PostCoder()
    >>> result = pc.get("SW1A 2TT")
    >>> PrettyPrinter(indent=4).pprint(result['geo'])
    {   u'easting': u'530283',
        u'geohash': u'http://geohash.org/gcpuvptqwyh4',
        u'lat': u'51.502308',
        u'lng': u'-0.124331',
        u'northing': u'179820'}
    >>>

If for any reason you want to use your own caching or validation, you 
also have access to the functions in the `postcodes` module, which are 
also documented in the `API`_ section.

Returned Data
-------------

For each postcode, a Python dictionary is returned containing all the 
available data from the Ordanance Survey Code-Point Open dataset. 
For example, ``postcodes.get("W1A 2TT")`` returns:

.. code-block:: json

    { u'administrative': { u'constituency': { u'code': u'',
                                              u'title': u'',
                                              u'uri': u''},
                           u'district': { u'snac': u'',
                                          u'title': u'',
                                          u'uri': u''},
                           u'ward': { u'snac': u'',
                                      u'title': u'',
                                      u'uri': u''}},
      u'geo': { u'easting': u'',
                u'geohash': u'',
                u'lat': u'',
                u'lng': u'',
                u'northing': u''},
      u'postcode': u''}

Values have been removed for brevity; all returned types are `unicode` 
stings.

.. _API:


API Documentation
=================

.. autofunction:: get
.. autofunction:: get_nearest
.. autofunction:: get_from_postcode
.. autofunction:: get_from_geo

The PostCoder Object
--------------------
.. autoclass:: PostCoder

    .. automethod:: get
    .. automethod:: get_nearest
    .. automethod:: get_from_postcode
    .. automethod:: get_from_geo

© 2012, `Edward Robinson`_

.. _Edward Robinson: http://twitter.com/eddrobinson
