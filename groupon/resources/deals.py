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


class Deal( object ):


    def get( self, key, resource = None, options = None ):
        '''
        Here's how get all your available Groupon Deals:
        @note: The options object is indeed optional! Omit it from your
        interface 'get' call if you choose.
        @note: Setting the 'flat' option to True (recommended & default)
        returns a predictable, object-oriented representation of the standard
        Groupon API result structure. False returnes the Groupon standard
        result structure.

        >>> from groupon.resources.deals import Deal
        >>> key = 'my_groupon_api_key'
        >>> dealInterface = Deal()
        >>> options = {'flat':True}
        >>> status, deals = dealInterface.get(key, {'api':{'version':2}}, options)
        '''

        from groupon.extras.http import Request as APIRequest

        try:
            apiVersion = resource['api']['version']
        except:
            apiVersion = 1

        try:
            options['api'] = {'version':apiVersion}
        except:
            options = {'api':{'version':apiVersion}}

        entrypoint = 'v%(apiVersion)d/deals/' % {'apiVersion':apiVersion}

        request = APIRequest()

        return request.get( key, entrypoint, options )
