#!/usr/bin/python

# Copyright 2010 Webframeworks LLC Licensed under the Apache
# License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License. You may obtain
# a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 Unless required
# by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import os
import platform
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from groupon import Version

def read( fname ):
    return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()

reauiredPackages = ['httplib2']

if float( platform.python_version()[:3] ) < 2.6:
    reauiredPackages.append( 'simplejson' )

setup( name = 'python-groupon',
      version = Version,
      description = 'Groupon Web Services Interface Library',
      long_description = read( 'README' ),
      author = 'The python-groupon development team.',
      author_email = 'python-groupon@googlegroups.com',
      url = 'http://code.google.com/p/python-groupon/',
      install_requires = reauiredPackages,
      packages = ['groupon', 'groupon.extras', 'groupon.resources'],
      license = 'Apache License, Version 2.0',
      platforms = 'Posix; MacOS X; Windows',
      classifiers = [ 'Development Status :: 2 - Beta',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: Apache License, Version 2.0',
                      'Operating System :: OS Independent',
                      'Topic :: Internet',
                      ],
      )
