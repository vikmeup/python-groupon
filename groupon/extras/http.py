from groupon import Version

__author__ = "Allan Bunch"
__copyright__ = "Copyright (C) 2010 Webframeworks LLC"
__license__ = """Copyright 2010 Webframeworks LLC Licensed under the Apache
                 License, Version 2.0 (the "License"); you may not use this
                 file except in compliance with the License. You may obtain
                 a copy of the License at
                 http://www.apache.org/licenses/LICENSE-2.0 Unless required
                 by applicable law or agreed to in writing, software
                 distributed under the License is distributed on an "AS IS"
                 BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
                 express or implied. See the License for the specific language
                 governing permissions and limitations under the License."""
__version__ = Version
__maintainer__ = "Allan Bunch"
__status__ = "Development"
__credits__ = []


class Request( object ):


    baseURI = 'http://www.groupon.com/api/'

    def _objectify( self, structure, apiVersionNumber ):
        from code import Factory

        factory = Factory()

        return factory.objectify( structure, apiVersionNumber )

    def _request( self, key, entrypoint, data, action, options = None ):
        '''
        @requires: httplib2
        @note: Python version <2.6 @requires: simplejson
        '''

        import tempfile
        from urllib import urlencode
        from groupon import UserAgent
        try:
            import json
        except:
            import simplejson as json # for pre Python 2.6. Note: requires simplejson library.
        import httplib2

        requestHeaders = {}
        resourceBase = self.baseURI
        requestHeaders['X-GrouponToken'] = key
        requestHeaders['User-Agent'] = UserAgent

        try:
            clientWantsObjects = not options['flat']
            del( options['flat'] )
        except:
            clientWantsObjects = True

        # Extract the requested API version number from the options object.
        try:
            apiVersionNumber = options['api'].pop( 'version' )
        except:
            raise Exception( 'Invalid Groupon API version specifier.' )

        if len( options['api'] ) == 0:
            del( options['api'] )

        if options:
            options = '?format=json&%(options)s' % {'options':urlencode( options )}
        else:
            options = '?format=json'

        resourceURI = str( '%(resourceBase)s%(entrypoint)s%(options)s' % {'resourceBase':resourceBase, 'entrypoint':entrypoint, 'options':options} )

        if data:
            data = json.dumps( data )

        http = httplib2.Http( tempfile.mkdtemp() )

        responseHeaders, content = http.request( resourceURI, action, data, requestHeaders )

        try:
            response = json.loads( content, 'utf-8' )
        except:
            return responseHeaders, content

        if clientWantsObjects:
            response = self._objectify( response, apiVersionNumber )
        else:
            del( response['status'] )
            response = response

        return responseHeaders, response

    def get( self, key, entrypoint, options = None ):
        return self._request( key, entrypoint, None, 'GET', options )
