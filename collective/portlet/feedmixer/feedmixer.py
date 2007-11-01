import itertools
import feedparser

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.validation import validation

from collective.portlet.feedmixer import FeedMixerMessageFactory as _

# we want to cache feeds. There are several things we can use:
# - feedparser can use an etag
# - feedparser can use the http modification time
# - a minimum refresh time

# a feed cache can be identified by:
# - the feed url



def is_url_list(data):
    verify=validation.validatorFor("isURL")
    for url in (x.strip() for x in data.split()):
        if verify(url)!=True:
            return False
    return True

class IFeedMixer(IPortletDataProvider):
    """A portlet which aggregates multiple feeds.
    """
    title = schema.TextLine(
            title=_(u"heading_title",
                default=u"Portlet Title"),
            description=_(u"description_title",
                default=u""),
            default=u"",
            required=True)

    items_shown = schema.Int(
            title=_(u"heading_items_shown",
                default=u"Number of items to display"),
            description=_(u"description_items_shown",
                default=u""),
            default=5,
            required=True)

    feeds = schema.ASCII(
            title=_(u"heading_feeds",
                default=u"URL(s) for all feeds"),
            description=_(u"description_feeds",
                default=u"Enter the URLs for all feeds here, one URL per "
                        u"line. RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3 "
                        u"and ATOM 1.0 feeds are supported."),
            required=True,
            constraint=is_url_list)



class Assignment(base.Assignment):
    """Portlet assignment.
    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IFeedMixer)

    title = u"Feed Viewer"
    feeds = u""
    items_shown = 5

    def __init__(self, title=title, feeds=feeds, items_shown=items_shown):
        self.title=title
        self.feeds=feeds
        self.items_shown=items_shown
        
    @property        
    def feed_urls(self):
        return (url.strip() for url in self.feeds.split())
        


class Renderer(base.Renderer):
    """Portlet renderer.
    """
    render = ViewPageTemplateFile('feedmixer.pt')
        
    @property
    def title(self):
        return self.data.title


    def cleanFeed(self, feed):
        """Sanitize the feed.

        This function makes sure all feed and entry data we depend on us
        present and in proper form.
        """
        for entry in feed.entries:
            if not "published_parsed" in entry:
                entry["published_parsed"]=entry["updated_parsed"]
                entry["published"]=entry["updated"]



    def getFeed(self, url):
        """Fetch a feed.

        This may return a cached result if the cache entry is considered to
        be fresh. Returned feeds have been cleaned using the cleanFeed method.
        """
        feed=feedparser.parse(url)
        self.cleanFeed(feed)
        return feed


    def mergeEntriesFromFeeds(self, feeds):
        if not feeds:
            return []
        if len(feeds)==1:
            return feeds[0].entries

        entries=list(itertools.chain(*(feed.entries for feed in feeds)))
        entries.sort(key=lambda x: x["published_parsed"], reverse=True)

        return entries

    
#    @memoize
    def entries(self):
        feeds=[self.getFeed(url) for url in self.data.feed_urls]
        feeds=[feed for feed in feeds if feed is not None]
        entries=self.mergeEntriesFromFeeds(feeds)
        return entries[:self.data.items_shown]


        
# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IFeedMixer)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IFeedMixer)
