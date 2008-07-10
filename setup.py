from setuptools import setup, find_packages

version = '1.3'

setup(name='collective.portlet.feedmixer',
      version=version,
      description="Portlet which can show multiple feeds",
      long_description=open("README.txt").read() + \
                       open("docs/HISTORY.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone rss atom feed portlet',
      author='Wichert Akkerman - Jarn',
      author_email='wichert@jarn.com',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "FeedParser",
          "plone.portlets",
          "plone.app.portlets",
          "plone.memoize",
      ],
      )
