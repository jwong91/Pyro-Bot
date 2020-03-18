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
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,  # pylint: disable=no-member
                                      maxResults=10, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('date_time', event['start'].get('date'))
    print(start, event['summary'])


def get_event_id_by_summary(desired_event_summary):
    events_result = service.events().list(calendarId='primary',  # pylint: disable=no-member
                                          single_events=True,
                                          order_by='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        pass  # WIP


def create_cal_event(title, date_time, desc, event_id, date):
    event = {
        'summary': title,
        'description': desc,
        'start': {'date_time': date_time[0], 'timeZone': 'America/New_York'},
        'end': {'date_time': date_time[1], 'timeZone': 'America/New_York'},
        'id': event_id
        }
    print(title)
    print(desc)
    print(type(date_time[0]))
    print(date_time[0])
    print(type(date_time[1]))
    print(date_time[1])

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created!')
    except:
        traceback.print_exc()
        print('There was an error when trying to add the event to the calendar')

    stored_event_details = {
        'title': title,
        'eventID': event_id,
        'date': date,
        'attending': [],
        'not attending': [],
        'maybe attending': []
    }
    try:
        if not event_id:
            event_id = None
        event_file = 'event-database/' + event_id + '.json'

        with open(event_file, 'w') as idList:
            json.dump(stored_event_details, idList)
    except:
        traceback.print_exc()
    finally:
        idList.close()


async def list_all_events(ctx):
    event_list = ''
    event_details = {}
    events_result = service.events().list(calendarId='primary',  # pylint: disable=no-member
                                          single_events=True,
                                          order_by='startTime').execute()
    events = events_result.get('items', [])
    try:
        if not events:
            await ctx.send('No upcoming events found.')
        for event in events:
            raw_event_date_time = event['start'].get('date_time', event['start'].get('date'))
            title = event['summary']
            event_details = eCreate.make_readable_date_time(raw_event_date_time)
            date = event_details[0]
            time = event_details[1]
            event_list = event_list + 'Title: ' + title + '\n' \
                        + 'Date: ' + event_details[0] + '\n' \
                        + 'Time: ' + time['start'] + '-' + time['end'] + '\n \n'
        await ctx.send(event_list)
        print(event_list)
    except:
        traceback.print_exc()

# ! Old google calendar RSVP
# async def addRsvp(ctx, event_id, guest):
#     print('ping')
#     event = {
#         'event_id' : event_id,
#         'attendees[].displayName' : guest
#     }
#     await ctx.send('You want to rsvp for ' + event_id + ' as ' + guest)
#     try:
#         updated_event = service.events().update(calendarId='primary', event_id=event[event_id], body=event).execute()
#     except:
#         traceback.print_exc()


async def add_rsvp(event_name, event_id, guest):
    event_file = 'event-database/' + event_id + '.json'
    try:
        with open(event_file, 'r') as rsvpDb:
            event_details = json.load(rsvpDb)

            if not event_details['attending']:
                event_details['attending'] = []

            if str(guest) not in event_details['attending']:
                event_details['attending'].append(str(guest))

            print('guest list' + str(event_details['attending']))
            details = {
                'title': event_name,
                'eventID': event_id,
                'date': event_details['date'],
                'attending': event_details['attending'],
                'not attending': event_details['not attending'],
                'maybe attending': event_details['maybe attending']
            }
            print(details)
        with open(event_file, 'w') as rsvpDb:
            json.dump(details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def add_not_going(event_name, event_id, guest):
    event_file = 'event-database/' + event_id + '.json'
    try:
        with open(event_file, 'r') as rsvpDb:
            event_details = json.load(rsvpDb)

            if not event_details['not attending']:
                event_details['not attending'] = []

            if str(guest) not in event_details['not attending']:
                event_details['not attending'].append(str(guest))

            details = {
                'title': event_name,
                'eventID': event_id,
                'date': event_details['date'],
                'attending': event_details['attending'],
                'not attending': event_details['not attending'],
                'maybe attending': event_details['maybe attending']
            }
            print(details)
        with open(event_file, 'w') as rsvpDb:
            json.dump(details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def add_maybe_going(event_name, event_id, guest):
    event_file = 'event-database/' + event_id + '.json'
    try:
        with open(event_file, 'r') as rsvpDb:
            event_details = json.load(rsvpDb)

            if not event_details['maybe attending']:
                event_details['maybe attending'] = []

            if str(guest) not in event_details['maybe attending']:
                event_details['maybe attending'].append(str(guest))

            details = {
                'title': event_name,
                'eventID': event_id,
                'date': event_details['date'],
                'attending': event_details['attending'],
                'not attending': event_details['not attending'],
                'maybe attending': event_details['maybe attending']
            }
            print(details)
        with open(event_file, 'w') as rsvpDb:
            json.dump(details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def remove_rsvp(eventName, eventId, guest):
    eventFile = 'event-database/' + eventId + '.json'

    try:
        with open(eventFile, 'r') as rsvpDb:
            eventDetails = json.load(rsvpDb)

            attending_list = eventDetails['attending'].remove(str(guest))

            # details = {
            #     'title': event_name,
            #     'eventID': event_id,
            #     'date': eventDetails['date'],
            #     'attending': attending_list,
            #     'not attending': eventDetails['not attending'],
            #     'maybe attending': eventDetails['maybe attending']
            # }
        with open(eventFile, 'w') as rsvpDb:
            json.dump(eventDetails, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def remove_not_going(event_name, event_id, guest):
    event_file = 'event-database/' + event_id + '.json'

    try:
        with open(event_file, 'r') as rsvpDb:
            event_details = json.load(rsvpDb)

            attending_list = event_details['not attending'].remove(str(guest))

            # details = {
            #     'title': event_name,
            #     'eventID': event_id,
            #     'date': event_details['date'],
            #     'attending': event_details['attending'],
            #     'not attending': event_details['not attending'].remove(str(guest)),
            #     'maybe attending': event_details['maybe attending']
            # }
        with open(event_file, 'w') as rsvpDb:
            json.dump(event_details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def remove_maybe_going(event_name, event_id, guest):
    event_file = 'event-database/' + event_id + '.json'

    try:
        with open(event_file, 'r') as rsvpDb:
            event_details = json.load(rsvpDb)

            attending_list = event_details['maybe attending'].remove(str(guest))

            # details = {
            #     'title': event_name,
            #     'eventID': event_id,
            #     'date': event_details['date'],
            #     'attending': event_details['attending'],
            #     'not attending': event_details['not attending'],
            #     'maybe attending': event_details['maybe attending'].remove(str(guest))
            # }
        with open(event_file, 'w') as rsvpDb:
            json.dump(event_details, rsvpDb)
    except:
        traceback.print_exc()
    finally:
        rsvpDb.close()


async def get_attendees(ctx, title, date, desired_type):
    try:
        event_found = False
        for file in os.listdir('event-database'):
            try:
                with open('event-database/' + file, 'r') as rsvpDb:
                    event_details = json.load(rsvpDb)
                    if title in event_details['title'] and date in event_details['date']:
                        guest_list = ''

                        if desired_type == 'going':
                            if not event_details['attending']:
                                guest_list = 'No one is attending.'
                            else:
                                for guest in event_details['attending']:
                                    guest_list = guest_list + guest + '\n'

                        elif desired_type == 'notgoing':
                            if not event_details['not attending']:
                                guest_list = 'No one is not attending.'
                            else:
                                for guest in event_details['not attending']:
                                    guest_list = guest_list + guest + '\n'

                        elif desired_type == 'maybegoing':
                            if not event_details['maybe attending']:
                                guest_list = 'No one is maybe attending.'
                            else:
                                for guest in event_details['maybe attending']:
                                    guest_list = guest_list + guest + '\n'
                        else:
                            await ctx.send('The type of guest that was specified is not correct. \n \
                                    The vaild types are: going, notgoing, maybegoing.')
                        await ctx.send(guest_list)
                        event_found = True
            finally:
                rsvpDb.close()
        if not event_found:
            await ctx.send('The bot could not find the event specified.')
    except:
        traceback.print_exc()
