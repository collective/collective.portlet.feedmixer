import unittest
from collective.portlet.feedmixer.interfaces import isUrlList

class IsUrlListTests(unittest.TestCase):
    def testEmptyList(self):
        self.assertEqual(isUrlList(""), True)

    def testInvalidURL(self):
        self.assertEqual(isUrlList("www.jarn.com"), False)

    def testSingleHTTPURL(self):
        self.assertEqual(isUrlList("http://www.jarn.com/"), True)

    def testSingleHTTPSURL(self):
        self.assertEqual(isUrlList("https://www.jarn.com/"), True)

    def testSingleFeedURL(self):
        # This test needs Plone 3.0.3 or later
        self.assertEqual(isUrlList("feed://www.jarn.com/"), True)

    def testMultipleValidURLs(self):
        self.assertEqual(
                isUrlList("http://www.jarn.com/ http://simplon.biz"),
                True)

    def testValidAndInvalid(self):
        self.assertEqual(
                isUrlList("http://www.jarn.com/ simplon.biz"),
                False)

def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(IsUrlListTests))
    return suite
