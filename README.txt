Introduction
============

collective.portlet.feedmixer is a portlet for `Plone 3`_ which can show one
or multiple content feeds.

Feedmixer uses feedparser_ to process feeds which allows it to support RSS
0.90, Netscape RSS 0.91, Userland RSS 0.91, RSS 0.92, RSS 0.93, RSS 0.94,
RSS 1.0, RSS 2.0, Atom 0.3, Atom 1.0, and CDF feeds

.. _Plone 3: http://plone.org/
.. _feedparser: http://www.feedparser.org/


Installing
==========

This package requires Plone 3.0 or later and feedparser.

Installing without buildout
---------------------------

First install feedparser. You can install this in either the system
python path or in the lib/python directory of your Zope instance. If you
have setuptools installed you can do this using easy_install::

  easy_install FeedParser

If you do not have setuptools you can install it manually using the setup.py
script in the feedparser source. If you want to install feedparser inside
your Zope instance instead of system wide you can its ''--prefix='' option
to install in the ''lib/python'' directory of your Zope instance.

Next you need to install this package. This can also be done by installing
it in either your system path packages or in the lib/python directory of
your Zope instance. As with feedparser you can do this using either
easy_install or via the setup.py script.

After installing the package it needs to be registered in your Zope
instance.  This can be done by putting a
collective.portlet.feedmixer-configure.zcml file in the etc/pakage-includes
directory with this content::

  <include package="collective.portlet.feedmixer" />

or, alternatively, you can add that line to the configure.zcml in a
package or Product that is already registered.

Installing with buildout
------------------------

If you are using `buildout`_ to manage your instance installing
collective.portlet.feedmixer is even simpler. You can install it by adding
it to the eggs line for your instance::

  [instance]
  eggs = collective.portlet.feedmixer
  zcml = collective.portlet.feedmixer

The last line tells buildout to generate a zcml snippet that tells Zope
to configure collective.portlet.feedmixer.

If another package depends on the feedmixer egg or includes its zcml
directly you do not need to specify anything in the buildout configuration:
buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'', which
will take care of updating your system.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Using the portlet
=================

In order to use the feedmixer portlet you will first need to install the
feedmixer product in your site. This is done through the standard ''Add-on
products'' control panel in the Plone site setup. After this has been done
a new ''Feed Mixer' portlet type will be available.

Feedmixer portlets have several configurable options:

Portlet Title
  This will be used as the title of the portlet.

Maximum time to cache feed data
  This determins how long feeds can be cached before feedmixer will attempt
  to refresh the feed data. In order to reduce the load on other servers
  it is advisable to set this to a reasonably large value.

Number of items to display
  How many items to show in the portlet.

URL(s) for all feeds
  A list of URLs for all feeds. All standard RSS and Atom feeds are
  supported as well as CDF feeds.


Performance
===========

The portlet tries to be very friendly and will only reload a feed if required.
It does this in several different ways.

All feeds are stored in a shared cache as defined in `plone.memoize`_. This
defaults to being a Zope RAMCache but you can choose different caches by
registering a different ''ICacheChooser'' utility. The cache key used
is ''collective.portlet.feedmixer.FeedCache''. For example for deployments with
multiple Zope instances you can use a memcached_ based cache which will
allow you to share downloaded feeds amongst all Zope instances.

If a feed entry has expired in the cache it needs to be reloaded. However
the feedmixer portlet will try to use both `ETAGs` and HTTP Last-Modified
headers to check if the feed has been updated since the last time it was
downloaded. If it has not been updated the timeout for the cached feed will
be updated and continue to be used.

.. _plone.memoize: http://pypi.python.org/pypi/plone.memoize
.. _ETAGs: http://en.wikipedia.org/wiki/HTTP_ETag
.. _memcached: http://www.danga.com/memcached/


Copyright and credits
=====================

collective.portlet.feedmixer is copyright 2007 by `Jarn`_ (formerly known
as Plone Solutions).

It was written by Wichert Akkerman.

.. _Jarn: http://www.jarn.com/


