import urllib2
import json
from datetime import datetime


def splitDelta(timeDelta):
  seconds = timeDelta.total_seconds()
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return {
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  }


def getNextDeparture(fromWhere, toWhere):
  url = "http://transport.opendata.ch/api.php/v1/connections?from=%s&to=%s&limit=1fields[]=connections/from/departure" % (fromWhere, toWhere)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  content = json.loads(response.read())
  print content
  departureString = content['connections'][0]['from']['departure']
  departure = datetime.strptime(departureString, "%Y-%m-%dT%H:%M:%S+0100")
  now = datetime.now()
  timeDelta = departure - now
  minutes = splitDelta(timeDelta)['minutes']
  seconds = splitDelta(timeDelta)['seconds']
  return "%2i:%2i" % (minutes, seconds)


eigerplatz = "008571393"
hasler = "008590015"
bern = "008507000"
eigerplatz_string = "Eigerplatz: %s" % getNextDeparture(eigerplatz, bern)
hasler_string = "Hasler: %s" % getNextDeparture(hasler, bern)

output = open("out.txt", "w")
output.write(eigerplatz_string)
output.write(hasler_string)
output.write("\n")

