from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import itertools

@dataclass(frozen=True)
class Room:
    name: str
    capacity: int

    def __hash__(self):
        return hash((self.name, self.capacity))

    def __eq__(self, other):
        if not isinstance(other, Room):
            return NotImplemented
        return self.name == other.name and self.capacity == other.capacity

@dataclass
class Session:
    topic: str
    session_type: str
    teacher: str
    room: Room
    start_time: datetime
    end_time: datetime
    attendees: Set[int]

class WorkshopScheduler:
    def __init__(self, 
                 num_attendees: int,
                 num_days: int,
                 topics: List[str],
                 session_types: List[str],
                 rooms: List[Room],
                 start_time: datetime,
                 end_time: datetime):
        self.num_attendees = num_attendees
        self.num_days = num_days
        self.topics = topics
        self.session_types = session_types
        self.rooms = rooms
        self.start_time = start_time
        self.end_time = end_time
        
        # Initialize schedule
        self.schedule: List[Session] = []
        self.attendee_sessions: Dict[int, List[Session]] = {i: [] for i in range(num_attendees)}
        
        # Create teacher assignments (2 teachers per topic)
        self.teachers = {topic: [f"Teacher_{topic}_1", f"Teacher_{topic}_2"] for topic in topics}

    def is_valid_time(self, time: datetime) -> bool:
        """Check if the given time is within operating hours."""
        return (time.hour >= self.start_time.hour and 
                time.hour < self.end_time.hour)

    def get_available_rooms(self, time: datetime) -> List[Room]:
        """Get rooms that are not occupied at the given time."""
        occupied_rooms = {session.room for session in self.schedule 
                         if session.start_time <= time < session.end_time}
        return [room for room in self.rooms if room not in occupied_rooms]

    def get_available_teachers(self, time: datetime, topic: str) -> List[str]:
        """Get teachers for a topic who are not teaching at the given time."""
        busy_teachers = {session.teacher for session in self.schedule 
                        if session.start_time <= time < session.end_time}
        return [teacher for teacher in self.teachers[topic] 
                if teacher not in busy_teachers]

    def get_available_attendees(self, time: datetime) -> Set[int]:
        """Get attendees who are not in any session at the given time."""
        busy_attendees = set()
        for session in self.schedule:
            if session.start_time <= time < session.end_time:
                busy_attendees.update(session.attendees)
        return set(range(self.num_attendees)) - busy_attendees

    def schedule_session(self, topic: str, session_type: str, 
                        start_time: datetime) -> bool:
        """Attempt to schedule a session at the given time."""
        # Check if time is valid
        if not self.is_valid_time(start_time):
            return False

        end_time = start_time + timedelta(hours=2)
        
        # Get available resources
        available_rooms = self.get_available_rooms(start_time)
        if not available_rooms:
            return False
            
        available_teachers = self.get_available_teachers(start_time, topic)
        if not available_teachers:
            return False
            
        available_attendees = self.get_available_attendees(start_time)
        if not available_attendees:
            return False

        # Select room and teacher
        room = random.choice(available_rooms)
        teacher = random.choice(available_teachers)
        
        # Select attendees who need this session
        eligible_attendees = set()
        for attendee in available_attendees:
            attended_sessions = self.attendee_sessions[attendee]
            if not any(s.topic == topic and s.session_type == session_type 
                      for s in attended_sessions):
                eligible_attendees.add(attendee)
        
        if not eligible_attendees:
            return False
            
        # Take only up to room capacity
        selected_attendees = set(random.sample(
            list(eligible_attendees),
            min(len(eligible_attendees), room.capacity)
        ))
        
        # Create and add session
        session = Session(
            topic=topic,
            session_type=session_type,
            teacher=teacher,
            room=room,
            start_time=start_time,
            end_time=end_time,
            attendees=selected_attendees
        )
        
        self.schedule.append(session)
        for attendee in selected_attendees:
            self.attendee_sessions[attendee].append(session)
        
        return True

    def generate_schedule(self) -> List[Session]:
        """Generate the complete workshop schedule."""
        current_day = 0
        while current_day < self.num_days:
            current_time = self.start_time + timedelta(days=current_day)
            
            # Morning sessions
            for hour in [8, 11]:  # 8:00 AM and 11:00 AM slots
                current_slot = current_time.replace(hour=hour)
                for topic, session_type in itertools.product(self.topics, self.session_types):
                    self.schedule_session(topic, session_type, current_slot)
            
            # Afternoon sessions
            for hour in [14, 17]:  # 2:00 PM and 5:00 PM slots
                current_slot = current_time.replace(hour=hour)
                for topic, session_type in itertools.product(self.topics, self.session_types):
                    self.schedule_session(topic, session_type, current_slot)
            
            current_day += 1
        
        return self.schedule

    def print_schedule(self):
        """Print the generated schedule in a readable format."""
        for day in range(self.num_days):
            print(f"\nDay {day + 1}:")
            day_start = self.start_time + timedelta(days=day)
            day_sessions = [s for s in self.schedule 
                          if s.start_time.date() == day_start.date()]
            
            for session in sorted(day_sessions, key=lambda x: x.start_time):
                print(f"""
                Time: {session.start_time.strftime('%H:%M')} - {session.end_time.strftime('%H:%M')}
                Topic: {session.topic}
                Type: {session.session_type}
                Room: {session.room.name}
                Teacher: {session.teacher}
                Attendees: {len(session.attendees)}
                """)

def main():
    # Example usage with the given problem constraints
    start_time = datetime(2024, 1, 1, 8, 0)  # 8:00 AM
    end_time = datetime(2024, 1, 1, 18, 0)   # 6:00 PM
    
    # Define rooms
    rooms = [
        Room("Classroom_1", 60),
        Room("Classroom_2", 60),
        Room("Classroom_3", 60),
        Room("Classroom_4", 60),
        Room("Classroom_5", 60),
        Room("Amphitheater", 180)
    ]
    
    # Define topics and session types
    topics = ["A", "B", "C", "D"]  # A: AI in Healthcare, B: Ethics in AI, etc.
    session_types = ["Theoretical", "Practical", "Historical", "Test"]
    
    # Create scheduler instance
    scheduler = WorkshopScheduler(
        num_attendees=600,
        num_days=5,
        topics=topics,
        session_types=session_types,
        rooms=rooms,
        start_time=start_time,
        end_time=end_time
    )
    
    # Generate and print schedule
    schedule = scheduler.generate_schedule()
    scheduler.print_schedule()

if __name__ == "__main__":
    main()
