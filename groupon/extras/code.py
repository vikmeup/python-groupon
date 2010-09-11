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
__status__ = "Beta"
__credits__ = []


class Factory( object ):


    def buildObject( self, objectRef, properties = {} ):

        if type( objectRef ) == type:
            for key, value in properties.iteritems():
                setattr( objectRef, key, value )
        else:
            return type( '%s' % objectRef, ( object, ), properties )

    def objectify( self, structure, apiVersionNumber ):

        if structure.has_key( 'deals' ):
            dealList = []
            for deal in structure['deals']:
                Deal = self.buildObject( 'Deal', {'id':deal['id'] ,
                                                  'uri':deal['deal_url' ] ,
                                                  'status':deal['status']
                                                 } )

                # Begin Groupon Deal titles object.
                dealTitles = []
                DealTitle = self.buildObject( 'DealTitle', {'short':deal['short_title']} )
                dealTitles.append( DealTitle )

                if apiVersionNumber in [1]:
                    DealTitle = self.buildObject( 'DealTitle', {'long':deal['title']} )
                    dealTitles.append( DealTitle )
                self.buildObject( Deal, {'titles':dealTitles} )


                # Begin Groupon Deal placement object.
                try:
                    DealPlacement = self.buildObject( 'DealPlacement', {'priority':deal['placement_priority']} )
                except:
                    DealPlacement = DealPlacement = self.buildObject( 'DealPlacement', {'priority':None} )

                Deal.placement = DealPlacement

                # Begin Groupon Deal media object.
                DealMedia = self.buildObject( 'DealMedia' )
                self.buildObject( DealMedia, { 'images':[] } )

                DealImage = self.buildObject( 'DealImage' )
                self.buildObject( DealImage, { 'uri':deal['small_image_url'] } )
                self.buildObject( DealImage, { 'size':'small' } )
                DealMedia.images.append( DealImage )

                DealImage = self.buildObject( 'DealImage' )
                self.buildObject( DealImage, { 'uri':deal['medium_image_url'] } )
                self.buildObject( DealImage, { 'size':'medium' } )
                DealMedia.images.append( DealImage )

                DealImage = self.buildObject( 'DealImage' )
                self.buildObject( DealImage, { 'uri':deal['large_image_url'] } )
                self.buildObject( DealImage, { 'size':'large' } )
                DealMedia.images.append( DealImage )

                self.buildObject( Deal, { 'media':DealMedia } )

                # Begin Groupon Deal division object.
                DealDivision = self.buildObject( 'DealDivision', { 'id':deal['division_id'] , 'name':deal['division_name'] } )

                DealDivisionCoordinates = self.buildObject( 'DealDivisionCoordinates', { 'lat':deal['division_lat'], 'lng':deal['division_lng'] } )
                DealDivisionGeo = self.buildObject( 'DealDivisionGeo', { 'coordinates':DealDivisionCoordinates } )
                self.buildObject( DealDivision, { 'geo':DealDivisionGeo } )
                self.buildObject( Deal, { 'division':DealDivision } )


                DealDivisionTime = self.buildObject( 'DealDivisionTime' )
                DealDivisionTimeZone = self.buildObject( 'DealDivisionTimeZone', { 'name':deal['division_timezone'] ,
                                                                                   'meridian':'gmt',
                                                                                   'offset':deal['division_offset_gmt'] } )
                self.buildObject( DealDivisionTime, { 'zone':DealDivisionTimeZone } )
                self.buildObject( DealDivision, {'time':DealDivisionTime } )
                self.buildObject( Deal, { 'division':DealDivision } )

                # Begin Groupon Deal areas object.
                dealAreas = []

                if apiVersionNumber in [1]:
                    _dealAreas = []
                    for area in deal['areas']:
                        _dealArea = dict( id = area )
                        _dealAreas.append( _dealArea )
                else:
                    _dealAreas = deal['areas']

                for area in _dealAreas:
                    DealArea = self.buildObject( 'DealArea', area )
                    dealAreas.append( DealArea )
                self.buildObject( Deal, { 'areas':dealAreas } )

                # Begin Groupon Deal shipping object.
                DealShipping = self.buildObject( 'DealShipping', { 'requirements':[] } )
                DealShippingAddress = self.buildObject( 'DealShippingAddress', { 'required':deal['shipping_address_required'] } )
                DealShippingRequirement = self.buildObject( 'DealShippingRequirement', { 'address':DealShippingAddress } )
                DealShipping.requirements.append( DealShippingRequirement )
                self.buildObject( Deal, { 'shipping':DealShipping } )

                if apiVersionNumber in [1]:
                    # Begin Groupon Deal vendor object.
                    DealVendor = self.buildObject( 'DealVendor', {'id':deal['vendor_id'],
                                                                  'name':deal['vendor_name'],
                                                                  'uri':deal['vendor_website_url'] } )
                    self.buildObject( Deal, {'vendor':DealVendor} )
                else:
                    # Begin Groupon Deal merchant object.
                    DealMerchant = self.buildObject( 'DealMerchant', {'id':deal['merchant_id'],
                                                                      'name':deal['merchant_name'],
                                                                      'uri':deal['merchant_website_url'] } )
                    self.buildObject( Deal, { 'vendor':DealMerchant } )

                # Begin Groupon Deal dates object.
                DealDates = self.buildObject( 'DealDates', {'start':deal['start_date'],
                                                            'end':deal['end_date'] } )
                self.buildObject( Deal, {'dates':DealDates} )

                # Begin Groupon Deal tip object.
                DealTip = self.buildObject( 'DealTip', { 'reached':deal['tipped'],
                                                         'point':deal['tipping_point'] } )
                try:
                    self.buildObject( DealTip, { 'date':deal['tipped_date'] } )
                except:
                    self.buildObject( DealTip, { 'date':None } )

                self.buildObject( Deal, { 'tip':DealTip } )

                # Begin Groupon Deal inventory object.
                try:
                    dealInventoryTotal = deal['conditions']['initial_quantity']
                except:
                    dealInventoryTotal = 'unlimited'

                try:
                    dealInventoryStock = deal['conditions']['quantity_remaining']
                except:
                    dealInventoryStock = 'unlimited'

                DealInventoryUnits = self.buildObject( 'DealInventoryUnits', {'total':dealInventoryTotal ,
                                                                              'sold':deal['quantity_sold'] ,
                                                                              'available':dealInventoryStock } )

                DealInventory = self.buildObject( 'DealInventory', { 'available':not deal['sold_out'], 'units':DealInventoryUnits } )

                if apiVersionNumber in [1]:
                    # This looks like an API version < 2, so:
                    self.buildObject( DealInventory, {'limited':deal['conditions']['limited_quantity'] } )

                self.buildObject( Deal, {'inventory':DealInventory } )

                # Begin Groupon Deal cost object.
                if apiVersionNumber in [1]:
                    dealCosts = []
                    DealCost = self.buildObject( 'DealCost', {
                                                       'type':'value',
                                                       'amount':deal['value'][:-3],
                                                       'units':deal['value'][-3:]
                                                     } )
                    dealCosts.append( DealCost )

                    DealCost = self.buildObject( 'DealCost', {
                                                       'type':'price',
                                                       'amount':deal['price'][:-3],
                                                       'units':deal['price'][-3:]
                                                     } )
                    dealCosts.append( DealCost )

                    DealCost = self.buildObject( 'DealCost', {
                                                       'type':'discount',
                                                       'amount':deal['discount_amount'][:-3],
                                                       'units':deal['discount_amount'][-3:],
                                                       'factor':deal['discount_percent'] * float( .01 )
                                                     } )
                    dealCosts.append( DealCost )

                    self.buildObject( Deal, {'costs':dealCosts} )

                if apiVersionNumber in [1]:
                    dealConditionsDates = []
                    DealConditions = self.buildObject( 'DealConditions' )
                    DealConditionsDate = self.buildObject( 'DealConditionsDate', {'type':'expiration', 'value':deal['conditions']['expiration_date']} )
                    dealConditionsDates.append( DealConditionsDate )
                    self.buildObject( DealConditions, {'dates':dealConditionsDates} )

                    DealConditionsPurchase = self.buildObject( 'DealConditionsPurchase', {'minimum':deal['conditions']['minimum_purchase'],
                                                                                          'maximum':deal['conditions']['maximum_purchase']} )
                    self.buildObject( DealConditions, {'purchase':DealConditionsPurchase} )

                    self.buildObject( Deal, {'conditions':DealConditions} )


                if deal.has_key( 'options' ):
                    # Begin Groupon Deal variations object.
                    dealVariations = []
                    for dealOption in deal['options']:
                        DealVariation = self.buildObject( 'DealVariation', {'id':dealOption['id'],
                                                                            'title':dealOption['title']} )
                        # Begin Groupon Deal Option inventory object.
                        try:
                            dealVariationTotalUnits = dealOption['conditions']['initial_quantity']
                        except:
                            dealVariationTotalUnits = None

                        try:
                            dealVariationUnitsInStock = dealOption['conditions']['quantity_remaining']
                        except:
                            dealVariationUnitsInStock = None

                        DealVariationInventory = self.buildObject( 'DealVariationInventory', {'total':dealVariationTotalUnits,
                                                                                              'sold':dealOption['quantity_sold'],
                                                                                              'stock':dealVariationUnitsInStock,
                                                                                              'available':not dealOption['sold_out']} )
                        self.buildObject( DealVariation, {'inventory':DealVariationInventory} )

                        # Begin Groupon Deal Option cost object.
                        dealVariationCosts = []

                        DealVariationCost = self.buildObject( 'DealVariationCost', { 'type':'value',
                                                                                     'amount':dealOption['value'][:-3],
                                                                                     'units':dealOption['value'][-3:] } )
                        dealVariationCosts.append( DealVariationCost )

                        DealVariationCost = self.buildObject( 'DealVariationCost', { 'type':'price',
                                                                                     'amount':dealOption['price'][:-3],
                                                                                     'units':dealOption['price'][-3:] } )
                        dealVariationCosts.append( DealVariationCost )

                        DealVariationCost = self.buildObject( 'DealVariationCost', { 'type':'discount',
                                                                                     'amount':dealOption['discount_amount'][:-3],
                                                                                     'units':dealOption['discount_amount'][-3:],
                                                                                     'factor':dealOption['discount_percent'] * float( .01 ) } )
                        dealVariationCosts.append( DealVariationCost )

                        self.buildObject( DealVariation, {'costs':dealVariationCosts} )

                        # Begin Groupon Deal Options conditions object.
                        dealVariationConditionsDates = []
                        DealVariationConditions = self.buildObject( 'DealVariationConditions' )
                        DealVariationConditionsDate = self.buildObject( 'DealVariationConditionsDate', {'type':'expiration', 'value':dealOption['conditions']['expiration_date']} )
                        dealVariationConditionsDates.append( DealVariationConditionsDate )
                        self.buildObject( DealVariationConditions, {'dates':dealVariationConditionsDates} )

                        DealVariationConditionsPurchase = self.buildObject( 'DealVariationConditionsPurchase', {'minimum':dealOption['conditions']['minimum_purchase'],
                                                                                              'maximum':dealOption['conditions']['maximum_purchase']} )
                        self.buildObject( DealVariationConditions, {'purchase':DealVariationConditionsPurchase} )

                        self.buildObject( DealVariation, {'conditions':DealVariationConditions} )

                        dealVariations.append( DealVariation )

                    self.buildObject( Deal, {'variations':dealVariations} )

                dealList.append( Deal )

            return dealList
        elif structure.has_key( 'divisions' ):
            divisionList = []

            for division in structure['divisions']:
                Division = self.buildObject( 'Division', {'id':division['id'],
                                                         'name':division['name']} )
                DivisionGeo = self.buildObject( 'DivisionGeo' )
                DivisionGeoCoordinates = self.buildObject( 'DivisionGeoCoordinate', {'lat':division['location']['latitude'],
                                                                                     'lng':division['location']['longitude']} )
                self.buildObject( DivisionGeo, {'coordinates':DivisionGeoCoordinates} )
                self.buildObject( Division, {'geo':DivisionGeo} )

                class DivisionTime: pass
                DivisionTime = self.buildObject( 'DivisionTime' )

                DivisionTimeZone = self.buildObject( 'DivisionTimeZone', {'name':division['location']['timezone'],
                                                                         'meridian':'gmt',
                                                                         'offset':division['location']['timezone_offset_gmt']} )
                self.buildObject( DivisionTime, {'zone':DivisionTimeZone} )
                self.buildObject( Division, {'time':DivisionTime} )

                divisionList.append( Division )
            return divisionList
        else:
            raise Exception( 1000, 'Invalid Groupon entity requested.' )
