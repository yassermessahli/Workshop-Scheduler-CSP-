from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from main import WorkshopScheduler, Room
import pprint


app = Flask(__name__)
CORS(app)

# Default values matching main.py
DEFAULT_VALUES = {
    'numAttendees': 600,
    'numDays': 5,
    'topics': ['A', 'B', 'C', 'D'],
    'sessionTypes': ['Theoretical', 'Practical', 'Historical', 'Test'],
    'startTime': '08:00',
    'endTime': '18:00',
    'rooms': [
        {'name': 'Classroom 1', 'capacity': 60},
        {'name': 'Classroom 2', 'capacity': 60},
        {'name': 'Classroom 3', 'capacity': 60},
        {'name': 'Classroom 4', 'capacity': 60},
        {'name': 'Classroom 5', 'capacity': 60},
        {'name': 'Amphitheater', 'capacity': 180}
    ]
}

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    try:
        data = request.json or {}
        
        # Get values with defaults
        num_attendees = data.get('numAttendees', DEFAULT_VALUES['numAttendees'])
        num_days = data.get('numDays', DEFAULT_VALUES['numDays'])
        topics = data.get('topics', DEFAULT_VALUES['topics'])
        session_types = data.get('sessionTypes', DEFAULT_VALUES['sessionTypes'])
        start_time_str = data.get('startTime', DEFAULT_VALUES['startTime'])
        end_time_str = data.get('endTime', DEFAULT_VALUES['endTime'])
        rooms_data = data.get('rooms', DEFAULT_VALUES['rooms'])
        
        
        # Convert time strings to datetime
        start_time = datetime.strptime(start_time_str, '%H:%M').replace(year=2024, month=1, day=1)
        end_time = datetime.strptime(end_time_str, '%H:%M').replace(year=2024, month=1, day=1)
        
        # Create Room objects
        rooms = [Room(r['name'], r['capacity']) for r in rooms_data]
        
        # Initialize scheduler
        scheduler = WorkshopScheduler(
            num_attendees=num_attendees,
            num_days=num_days,
            topics=topics,
            session_types=session_types,
            rooms=rooms,
            start_time=start_time,
            end_time=end_time
        )
        
        
        # Generate schedule
        schedule = scheduler.generate_schedule()
        
        
        # Convert schedule to JSON-serializable format
        formatted_schedule = []
        for day in range(num_days):
            day_schedule = {
                'day': day + 1,
                'sessions': []
            }
            
            day_start = start_time.replace(day=day + 1)
            day_sessions = [s for s in schedule if s.start_time.date() == day_start.date()]
            
            for session in sorted(day_sessions, key=lambda x: x.start_time):
                day_schedule['sessions'].append({
                    'time': session.start_time.strftime('%H:%M'),
                    'topic': session.topic,
                    'type': session.session_type,
                    'room': session.room.name,
                    'attendees': len(session.attendees)
                })
            
            formatted_schedule.append(day_schedule)
        
        pprint.pprint(formatted_schedule)
        return jsonify(formatted_schedule)
        
    except Exception as e:
        print(e)
        return jsonify({
            'error':str(e),
            'message': 'Using default values where applicable'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)