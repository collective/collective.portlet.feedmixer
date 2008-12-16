import itertools
import time
import feedparser

from zope.app.component.hooks import getSite

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.portlets.portlets import base
from plone.memoize import request
from plone.memoize.interfaces import ICacheChooser

from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.feedmixer.interfaces import IFeedMixer

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignable

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
 
class Assignment(base.Assignment):
    """Portlet assignment.
    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IFeedMixer)

    title = u"Feed Viewer"
    feeds = u""
    items_shown = 5
    cache_timeout = 900
    assignment_context_path = None

    def __init__(self, title=title, feeds=feeds, items_shown=items_shown,
                 cache_timeout=cache_timeout,
                 assignment_context_path=assignment_context_path):
        self.title=title
        self.feeds=feeds
        self.items_shown=items_shown
        self.cache_timeout=cache_timeout
        self.assignment_context_path = assignment_context_path
        
    @property        
    def feed_urls(self):
        return (url.strip() for url in self.feeds.split())
        

    def Title(self):
        """Returns the title. The function is used by Plone to render <title> correctly."""
        return self.title
        

    def cleanFeed(self, feed):
        """Sanitize the feed.

        This function makes sure all feed and entry data we depend on us
        present and in proper form.
        """
        for entry in feed.entries:
            entry["feed"]=feed.feed
            if not "published_parsed" in entry:
                entry["published_parsed"]=entry["updated_parsed"]
                entry["published"]=entry["updated"]



    def getFeed(self, url):
        """Fetch a feed.

        This may return a cached result if the cache entry is considered to
        be fresh. Returned feeds have been cleaned using the cleanFeed method.
        """
        now=time.time()

        chooser=getUtility(ICacheChooser)
        cache=chooser("collective.portlet.feedmixer.FeedCache")

        cached_data=cache.get(url, None)
        if cached_data is not None:
            (timestamp, feed)=cached_data
            if now-timestamp<self.cache_timeout:
                return feed

            newfeed=feedparser.parse(url,
                    etag=getattr(feed, "etag", None),
                    modified=getattr(feed, "modified", None))
            if newfeed.status==304:
                self.cleanFeed(feed)
                cache[url]=(now+self.cache_timeout, feed)
                return feed

        feed=feedparser.parse(url)
        self.cleanFeed(feed)
        cache[url]=(now+self.cache_timeout, feed)

        return feed


    def mergeEntriesFromFeeds(self, feeds):
        if not feeds:
            return []
        if len(feeds)==1:
            return feeds[0].entries

        entries=list(itertools.chain(*(feed.entries for feed in feeds)))
        entries.sort(key=lambda x: x["published_parsed"], reverse=True)

        return entries

    
    @request.cache(get_key=lambda func,self:self.data.feed_urls,
                   get_request="self.request")
    def entries(self):
        feeds=[self.getFeed(url) for url in self.data.feed_urls]
        feeds=[feed for feed in feeds if feed is not None]
        entries=self.mergeEntriesFromFeeds(feeds)
        return entries


class Renderer(base.Renderer):
    """Portlet renderer.
    """
    render = ViewPageTemplateFile("portlet.pt")

    @property
    def available(self):
        return bool(self.data.entries())

    @property
    def title(self):
        return self.data.title

    @property
    def entries(self):
        return self.data.entries()[:self.data.items_shown]

    @property
    def more_url(self):
        return "%s/++contextportlets++%s/%s/full_feed" % \
               (self.assignment_context.absolute_url(),
                self.manager.__name__,
                self.data.__name__)

    @property
    def assignment_context(self):
        context = getSite().unrestrictedTraverse(
            '/'.join(self.context.getPhysicalPath()))
        while not IPloneSiteRoot.providedBy(context):
            if ILocalPortletAssignable.providedBy(context) and \
                   self.data in getMultiAdapter((context, self.manager),
                                                IPortletAssignmentMapping).values():
                break
            context = context.aq_parent
        return context # content on which the portlet is assigned or portal


class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(IFeedMixer)

    def create(self, data):
        path = self.context.__parent__.getPhysicalPath()
        return Assignment(assignment_context_path='/'.join(path), **data)


class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(IFeedMixer)
