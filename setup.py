from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.portlet.feedmixer',
      version=version,
      description="Portlet which can show multiple feeds",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
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
      namespace_packages=['collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          "FeedParser",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
