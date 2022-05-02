#This just gets the current station status, saves it in a given folder, and then waits to get the next one. It will run forever if you don't stop it.
#I think that should be OK, because you should only get about 17 megabytes per day.

from urllib.request import urlopen
import json
import time
import traceback

statusURL = 'https://gbfs.bcycle.com/bcycle_boulder/station_status.json'
saveFolder = 'GBFSTest1_StationStatus_Output'
data = {}

while True:
	try:
		response = urlopen(statusURL)
		data = json.loads(response.read())

		print("Got data from: {}".format(data['last_updated']))

		with open('{}/{}.json'.format(saveFolder, str(data['last_updated'])), 'w') as f:
			json.dump(data, f)
		
		time.sleep(data['ttl'] / 2) #Should never skip an update. It will write most times twice, but it'll just replace it the second time, so there won't be duplicates.
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
		raise KeyboardInterrupt #We want the next except to catch anything, but since literally the entire thing is in a try, we need to catch, and then reraise, keyboard inturrupts so they actually stop it.
	except:
		print("An Exception occured")
		time.sleep(5) #Wait 5 seconds then try again.
	