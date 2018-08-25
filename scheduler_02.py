from __future__ import print_function
import datetime
from datetime import timedelta
import json
from pprint import pprint
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():

    calID = raw_input('Enter the calendar ID of your colleague (cardinalblue email address):\n' )
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    myNow = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    myEvents_result = service.events().list(calendarId='primary', timeMin=myNow,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    myEvents = myEvents_result.get('items', [])
    startTimes = []
    endTimes =[]
    dates = []
    if not myEvents:
        print('No upcoming events found.')
    for myEvent in myEvents:
        start = myEvent['start'].get('dateTime', myEvent['start'].get('date'))
        end = myEvent['end'].get('dateTime', myEvent['end'].get('date'))
        print(start, end, myEvent['summary'], sep = ' ')
        endTimes.append(end)
        startTimes.append(start)
        dates.append(start)
    
    busy_slots = []
    #available_slots["dates"] = []
    #for i, j, k in zip(startTimes, endTimes, xrange(0,len(startTimes))):
    #	startTime = str(i)
    #	endTime = str(j)
    #	if startTime.split('T',1)[0] not in available_slots["dates"]:
    #		available_slots["dates"].append(startTime.split('T',1)[0])
    #	available_slots["dates"][k] = {}
    #	available_slots["dates"][k] = endTime.split('T',1)[1] 
    
    for i, j, k in zip(startTimes, endTimes, dates):
    	startTime = str(i)
    	startTime.replace('+', 'T')
    	endTime = str(j)
    	endTime.replace('+', 'T')
    	date = str(k)	
    	info = {
    		"date" : date.split('T',1)[0],
    		"start": startTime.split('T',1)[1],
    		"end": endTime.split('T',1)[1],
    	}
    	busy_slots.append(info)
    	#available_slots["dates"][0]["start"] = endTime.split('T',1)[1] 
    	#available_slots["dates"][1]["end"] = startTime.split('T',1)[1]
    print(busy_slots)

    available_slots = []
    for busy_slot, available_slot in zip(busy_slots, available_slots):
    	if busy_slot['date'] not in available_slot:
    		info = {
    			"date": busy_slot['date'],
    			"start": "10:30:00+08:00", 
    			"end": busy_slot['start']
    		}
    	else:
    		info = {
    			"date": busy_slot['date'],
    			"start": busy_slot['end'],
    			"end": busy_slot['start'],
    		}
    	available_slots.append(info)
    print(available_slots)
    





    #coworker's calendar
    coNow = datetime.datetime.utcnow().isoformat() + 'Z'

    coEvents_result = service.events().list(calendarId= calID, timeMin=coNow,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    coEvents = coEvents_result.get('items', [])

if __name__ == '__main__':
	main()