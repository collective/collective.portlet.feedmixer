from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.feedmixer import portlet as portlet_mod
from collective.portlet.feedmixer.tests.base import TestCase

from collective.portlet.feedmixer.tests import FEED_ONE

class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType,
                name='collective.portlet.feedmixer.FeedMixer')
        self.assertEquals(portlet.addview,
                'collective.portlet.feedmixer.FeedMixer')

    def testInterfaces(self):
        portlet = portlet_mod.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddView(self):
        portlet = getUtility(IPortletType,
                name='collective.portlet.feedmixer.FeedMixer')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data=dict(
            title="Test Title",
            feeds="Test Feeds",
            items_shown=16,
            cache_timeout=32))

        self.assertEquals(len(mapping), 1)
        assignment=mapping.values()[0]
        self.failUnless(isinstance(assignment, portlet_mod.Assignment))
        self.assertEqual(assignment.title, "Test Title")
        self.assertEqual(assignment.feeds, "Test Feeds")
        self.assertEqual(assignment.items_shown, 16)
        self.assertEqual(assignment.cache_timeout, 32)


    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = portlet_mod.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, portlet_mod.EditForm))

        editview.setUpWidgets(True)
        editview.handle_edit_action.success(dict(
            title="Test Title",
            feeds="Test Feeds",
            items_shown=16,
            cache_timeout=32))
        assignment=mapping.values()[0]
        self.failUnless(isinstance(assignment, portlet_mod.Assignment))
        self.assertEqual(assignment.title, "Test Title")
        self.assertEqual(assignment.feeds, "Test Feeds")
        self.assertEqual(assignment.items_shown, 16)
        self.assertEqual(assignment.cache_timeout, 32)

    def testObtainRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                context=self.portal)
        
        assignment = portlet_mod.Assignment()

        renderer = getMultiAdapter(
                (context, request, view, manager, assignment),
                IPortletRenderer)
        self.failUnless(isinstance(renderer, portlet_mod.Renderer))


class TestRenderer(TestCase):
    
    def afterSetUp(self):
        self.setRoles(('Manager',))

    def renderer(self, context=None, request=None, view=None,
            manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager,
                name='plone.rightcolumn', context=self.portal)
        
        assignment = assignment or portlet_mod.Assignment()
        return getMultiAdapter(
                (context, request, view, manager, assignment),
                IPortletRenderer)

    def testRender(self):
        r = self.renderer(context=self.portal,
                assignment=portlet_mod.Assignment(
                    title="Test Title",
                    items_shown=2,
                    feeds=FEED_ONE))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.failUnless("Test Title" in output)
        self.failUnless("Feed One Item One" in output)
        self.failUnless("Nov 02, 2007" in output)
        self.failUnless("http://test.one/item/1" in output)
        self.failUnless("Feed One Item Two" in output)
        self.failUnless("Nov 01, 2007" in output)
        self.failUnless("http://test.one/item/2" in output)
        self.failUnless("http://test.one/item/3" not in output)

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
