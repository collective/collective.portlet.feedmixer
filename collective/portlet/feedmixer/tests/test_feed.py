import unittest
from zope.interface.verify import verifyObject
from collective.portlet.feedmixer.interfaces import IFeedMixer
from collective.portlet.feedmixer.portlet import Assignment

class ConstructionTests(unittest.TestCase):
    def testInterface(self):
        feed=Assignemtn()
        verifyObject(IFeedMixer, feed)

    def testParameterOrder(self):
        feed=Assignment("title", "feeds", "items_shown", "cache_timeout")
        self.assertEqual(feed.title, "title")
        self.assertEqual(feed.feeds, "feeds")
        self.assertEqual(feed.items_shown, "items_shown")
        self.assertEqual(feed.cache_timeout, "cache_timeout")

    def testNamerParameters(self):
        feed=Assignment(title="title", feeds="feeds",
                items_shown="items_shown", cache_timeout="cache_timeout")
        self.assertEqual(feed.title, "title")
        self.assertEqual(feed.feeds, "feeds")
        self.assertEqual(feed.items_shown, "items_shown")
        self.assertEqual(feed.cache_timeout, "cache_timeout")

def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConstructionTests))
    return suite
