import sys
from suds import null, WebFault
from suds.client import Client
import logging


username = 'CristiGociu'
apiKey = '51605e80a9634a3e2c861cc5420779fdfb4e9905'
url = 'http://flightxml.flightaware.com/soap/FlightXML2/wsdl'


logging.basicConfig(level=logging.INFO)
api = Client(url, username=username, password=apiKey)
#print api

# Get the weather
result = api.service.Metar('DXB')
print result

# Get the flights enroute
result = api.service.Enroute('DXB', 10, '', 0)
flights = result['enroute']
print dir(result)

print "Aircraft en route to DXB:"
for flight in flights:
    print "%s (%s) \t%s (%s)" % ( flight['ident'], flight['aircrafttype'],
                                  flight['originName'], flight['origin'])
