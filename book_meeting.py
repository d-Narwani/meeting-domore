from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import uuid

app = Flask(__name__)

@app.route('/create_event', methods=['POST'])
def create_event():

    data = request.get_json()

    # Extract parameters from the POST request
    access_token = data['accessToken']
    start_time = data['start_time']
    end_time = data['end_time']
    timezone = data['timezone']
    title = data['title']
    attendees_emails = data['attendees']


    # Create credentials object
    credentials = Credentials(access_token)

    # Build the service
    service = build('calendar', 'v3', credentials=credentials)

    # Prepare the attendees list
    attendees = [{'email': email} for email in attendees_emails]

    # Generate a unique requestId
    request_id = str(uuid.uuid4())

    # Create the event
    event = {
        'summary': title,
        'start': {
            'dateTime': start_time,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time,
            'timeZone': timezone,
        },
        'attendees': attendees,
        'conferenceData': {
            'createRequest': {
                'requestId': str(uuid.uuid4()),  # Use a unique requestId
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                }
            }
        }
    }

    try:
        # Call the Calendar API to create the event
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})

    # Extract the meeting link
    print(event)
    meeting_link = event['hangoutLink']

    # Return the meeting link
    return jsonify({'meetingLink': meeting_link})


@app.route('/', methods=['GET'])
def index():
    return "Chal raha hai sab"

if __name__ == '__main__':
    app.run(debug=True, port=8000)