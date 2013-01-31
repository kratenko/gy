import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'Markdown',
    'Mako',
    'pyramid_beaker',
    'pyramid_mailer',
    'Unidecode',
    'pyramid_simpleform',
    'pbkdf2',
    ]

setup(name='gy',
      version='0.0a1',
      description='gy',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='kratenko',
      author_email='',
      url='http://github.com/kratenko/gy',
      keywords='web wsgi bfg pylons pyramid cms blog',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='gy',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = gy:main
      [console_scripts]
      initialize_gy_db = gy.scripts.initializedb:main
      """,
      )
