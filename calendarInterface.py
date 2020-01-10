from __future__ import print_function
import datetime
import pickle
import os.path
import discord as dc
import eventCreator as eCreate
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import traceback
import json


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,  # pylint: disable=no-member
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

def getEventIdBySummary(desiredEventSummary):
    events_result = service.events().list(calendarId='primary',  # pylint: disable=no-member
                                    singleEvents=True,
                                    orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        pass # WIP


def createCalEvent(title, dateTime, desc, eventId):
    event = {
        'summary': title,
        'description': desc,
        'start': {'dateTime': dateTime[0], 'timeZone': 'America/New_York'},
        'end': {'dateTime': dateTime[1], 'timeZone': 'America/New_York'},
        'id': eventId
        }
    print(title)
    print(desc)
    print(type(dateTime[0]))
    print(dateTime[0])
    print(type(dateTime[1]))
    print(dateTime[1])

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created!')
    except:
        traceback.print_exc()
        print('There was an error when trying to add the event to the calendar')

    storedEventDetails = {
        'title': title,
        'eventID': eventId,
        'guests': []
    }
    try:
        if not eventId:
            eventId = None
        eventFile = 'event-database/' + eventId + '.json'

        with open(eventFile, 'w') as idList:
            json.dump(storedEventDetails, idList)
    except:
        traceback.print_exc()
    finally:
        idList.close()

async def listAllEvents(ctx):
    eventList = ''
    eventDetails = {}
    events_result = service.events().list(calendarId='primary',  # pylint: disable=no-member
                                    singleEvents=True,
                                    orderBy='startTime').execute()
    events = events_result.get('items', [])
    try:
        if not events:
            await ctx.send('No upcoming events found.')
        for event in events:
            rawEventDateTime = event['start'].get('dateTime', event['start'].get('date'))
            title = event['summary']
            eventDetails = eCreate.makeReadableDateTime(rawEventDateTime)
            date = eventDetails[0]
            time = eventDetails[1]
            eventList = eventList + 'Title: ' + title + '\n' \
                        + 'Date: ' + eventDetails[0] + '\n' \
                        + 'Time: ' + time['start'] + '-' + time['end'] + '\n \n'
        await ctx.send(eventList)
        print(eventList)
    except:
        traceback.print_exc()

# ! Old google calendar RSVP
# async def addRsvp(ctx, eventId, guest):
#     print('ping')
#     event = {
#         'eventId' : eventId,
#         'attendees[].displayName' : guest
#     }
#     await ctx.send('You want to rsvp for ' + eventId + ' as ' + guest)
#     try:
#         updated_event = service.events().update(calendarId='primary', eventId=event[eventId], body=event).execute()
#     except:
#         traceback.print_exc()

async def addRsvp(eventName, eventId, guest):
    eventFile = 'event-database/' + eventId + '.json'
    try:
        with open(eventFile, 'r') as rsvpDb:
            eventDetails = json.load(rsvpDb)

            if not eventDetails['guests']:
                eventDetails['guests'] = []
            print(guest)
            print(eventDetails['guests'])
            print(type(eventDetails['guests']))

            if str(guest) not in eventDetails['guests']:
                eventDetails['guests'].append(str(guest))

            print('guest list' + str(eventDetails['guests']))
            details = {
                'title': eventName,
                'eventID': eventId,
                'guests': eventDetails['guests']
            }
            print(details['guests'])
        with open(eventFile, 'w') as rsvpDb:
            json.dump(details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()

async def removeRsvp(eventName, eventId, guest):
    eventFile = 'event-database/' + eventId + '.json'

    try:
        with open(eventFile, 'r') as rsvpDb:
            eventDetails = json.load(rsvpDb)

            if not eventDetails['guests']:
                eventDetails['guests'] = []

            details = {
                'title': eventName,
                'eventID': eventId,
                'guests': eventDetails['guests'].remove(str(guest))
            }
        with open(eventFile, 'w') as rsvpDb:
            json.dump(details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


