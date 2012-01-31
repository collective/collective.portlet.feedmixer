from plone.portlets.interfaces import IPortletDataProvider
from collective.portlet.feedmixer import FeedMixerMessageFactory as _
from zope import schema
from Products.validation import validation

def isUrlList(data):
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

    cache_timeout = schema.Choice(
            title=_(u"heading_cache_timeout",
                default=u"Maximum time to cache feed data"),
            description=_(u"description_cache_timeout",
                default=u""),
            default="900",
            required=True,
            vocabulary="collective.portlet.feedmixer.timeouts")

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
            constraint=isUrlList)

    def entries():
        """Return feed entries for all feeds.

        The entries from all feeds will be combined in a single listed and
        sorted by publication date.
        """

