import sys
import os
import json
import pypco
import requests
import uuid
from datetime import datetime, timedelta
import pytz 
from libpcocheckin import pcocheckin # https://github.com/jcc-dhudson/libpcocheckin
import shelve
import urllib.parse


SHELVE_INIT = False # set to true to wipe out the shelf!
SHELVE_LOCATION = 'checkin-dwspectrum-shelve'
DW_TIMEZONE = 'US/Eastern'
LATENCY_CORRECT = 8000 # time in ms to subtract from checkin time to start the event in DW. 8000 seems to work pretty well
DEBUG = False
TEST_TIME = '2022-06-19T15:01:00' # set string to iso8601 in zulu to run your checkin event query for that datetime

def logger(msg):
    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print(f"{time} - {msg}")

try:
    PCO_LOCATION_ID = sys.argv[1] # can be comma separated such as 123456,654321
    DW_CAMERA_ID = sys.argv[2] # uuid from DW
except Exception as e:
    print(f"Must supply PCO_LOCATION_ID (comma separated) and DW_CAMERA_ID as ARGV vairable. - {e}")
    sys.exit(1)

try:
    PCO_APP_ID = os.environ['PCO_APP_ID'] # source ~/pco-env-vars.sh
    PCO_SECRET = os.environ['PCO_SECRET']
    DW_URL = os.environ['DW_URL'] # full url with basic auth such as "http://api:pass123@127.0.0.1:7001/"
except Exception as e:
    print(f"Must supply PCO_APP_ID, PCO_SECRET, DW_URL as environment vairables. - {e}")
    sys.exit(1)

s = shelve.open(SHELVE_LOCATION)
if 'complete' not in s or SHELVE_INIT:
    s['complete'] = []
complete = s['complete']

location_ids = PCO_LOCATION_ID.split(',')

pco = pypco.PCO(PCO_APP_ID, PCO_SECRET)
checkinsHndlr = pcocheckin.CHECKINS(pco, DEBUG) # https://github.com/jcc-dhudson/libpcocheckin

# used for testing:
if DEBUG and TEST_TIME:
    logger(f"using test time of {TEST_TIME}")
    dateNow = datetime.strptime(TEST_TIME, "%Y-%m-%dT%H:%M:%S") 
    checkins = checkinsHndlr.get_current_checkins(curr_time=dateNow, location_id=location_ids)
else:
    checkins = checkinsHndlr.get_current_checkins(location_id=location_ids)


for checkin in checkins:
    # skip anything that we have already added to DW
    if checkin['id'] in complete:
        continue
    name = checkin['person']['attributes']['name']
    message = f"{name} checked into {checkin['location']['attributes']['name']}"
    checked_in_by_name = 'not_set'
    if 'checked_in_by' in checkin:
        checked_in_by_name = checkin['checked_in_by']['attributes']['name']
    detail = f"{message} by {checked_in_by_name}"

    checkin_time = datetime.strptime(checkin['attributes']['created_at'], "%Y-%m-%dT%H:%M:%SZ") # PCO provides created_at in Zulu
    checkin_time = checkin_time.replace(tzinfo=pytz.timezone('Zulu')).astimezone(pytz.timezone(DW_TIMEZONE)) # convert them to local time

    logger(f"{detail} {checkin_time}")

    message = urllib.parse.quote(message)
    detail = urllib.parse.quote(detail)

    url = DW_URL + "ec2/bookmarks/add?"
    url += 'startTime=' + str(round(checkin_time.timestamp() * 1000)-LATENCY_CORRECT) # time in ms - LATENCY_CORRECT for delay
    url += '&duration=10000'
    url += '&name=' + message
    url += '&description=' + detail
    url += '&tag=pco_checkin'
    url += '&cameraId=' + DW_CAMERA_ID 
    url += '&guid=' + str(uuid.uuid4())
    logger(f"   {url}")
    requests.get(url)
    complete.append(checkin['id'])

s['complete'] = complete
s.sync()
s.close()