# Introduction #
This library provides a pure Python interface to the [Groupon REST API](http://www.groupon.com/pages/api). The interface provides standard, consistent, and predictable object-based interaction between your Python code and Groupon's API resources.

## Features include: ##
  * Groupon API support through version 2.
  * Support for Groupon's documented API call options.
  * Object-oriented request and response structures for straightforward application integration.
  * Optional support for Groupon's standard response structure.

## Required Python Packages: ##
The following Python Packages will be automatically installed where necessary.

  * [httplib2](http://code.google.com/p/httplib2/)
  * [simplejson](http://pypi.python.org/pypi/simplejson/) (Python versions < 2.6)

## Installation ##
Get the [latest package release](http://code.google.com/p/python-groupon/downloads/list?q=label:Featured), expand it, make your way into the extracted directory, then run:
```
$ python setup.py install
```
... and you're set. **However**, if you're feeling really adventurous, you may want to install the latest development version instead:
```
$ pip install http://python-groupon.googlecode.com/svn/trunk/
```


## Documentation ##
Full documentation coming **very** soon. Interface call documentation is available in each resource's (deals, and divisions) `get` method docstring, and can be browsed via Python's `pydoc` functionality.

## Quick Start ##
Want to get started right away? Once you have the _groupon_ module in place, along with the required package(s), this will get have you going in no time:

```
# Here's how get the available New York Groupon Deals:

>>> from groupon.resources.deals import Deal
>>> 
>>> key = 'my_groupon_api_key'
>>> dealInterface = Deal()
>>> myOptions = {'division':'new-york'}
>>> status, deals = dealInterface.get(key, options=myOptions)
>>> print( [deal.id for deal in deals] )
[u'chom-chom-new-york', u'cake-shake-new-york']
```

That's it! Your `deals` variable now contains a nicely structured object-oriented representation of Groupon's current deals.

If you prefer Groupon's standard (flat) Deal representation, you'd simply add an option named "flat" with its value set to True. Here's how that would look in the code above:

```
...
>>> myOptions = {'division':'new-york', 'flat':True}
...
```

Here's how to specify the Groupon API version you're interested in calling:

```
...
>>> status, deals = dealInterface.get(key, {'api':{'version':1}}, options)
...
```

Requesting Groupon's divisions is just as easy:

```
# Here's how get the available Groupon Divisions:

>>> from groupon.resources.divisions import Division
>>> 
>>> key = 'my_groupon_api_key'
>>> divisionInterface = Division()
>>> status, divisions = divisionInterface.get(key)
>>> print([division.id for division in divisions])
[u'akron-canton', u'albuquerque', u'atlanta', u'austin', u'bakersfield', u'baltimore', ...]
```

Note: The _API version_, and _flat_ options work here as well. Specify them as in the `deals` example.

Enjoy!