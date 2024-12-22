from main import WorkshopScheduler, Room, Session
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns

class SchedulerEvaluator:
    def __init__(self, schedule: List[Session]):
        self.schedule = schedule
        self.metrics = {}
        
    def evaluate_room_utilization(self) -> Dict:
        """Calculate room utilization percentage"""
        room_usage = defaultdict(int)
        total_slots = 4 * 5  # 4 slots per day * 5 days
        
        for session in self.schedule:
            room_usage[session.room.name] += 1
            
        utilization = {
            room: (count / total_slots) * 100 
            for room, count in room_usage.items()
        }
        
        self.metrics['room_utilization'] = utilization
        return utilization
    
    def evaluate_teacher_workload(self) -> Dict:
        """Analyze teacher workload distribution"""
        teacher_sessions = defaultdict(int)
        
        for session in self.schedule:
            teacher_sessions[session.teacher] += 1
            
        self.metrics['teacher_workload'] = dict(teacher_sessions)
        return dict(teacher_sessions)
    
    def evaluate_session_distribution(self) -> Dict:
        """Analyze distribution of session types and topics"""
        topic_count = defaultdict(int)
        type_count = defaultdict(int)
        
        for session in self.schedule:
            topic_count[session.topic] += 1
            type_count[session.session_type] += 1
            
        self.metrics['topic_distribution'] = dict(topic_count)
        self.metrics['type_distribution'] = dict(type_count)
        return {'topics': dict(topic_count), 'types': dict(type_count)}
    
    def evaluate_attendee_coverage(self) -> Dict:
        """Analyze if all attendees get all required sessions"""
        attendee_sessions = defaultdict(lambda: defaultdict(set))
        
        for session in self.schedule:
            for attendee in session.attendees:
                attendee_sessions[attendee][session.topic].add(session.session_type)
        
        coverage = {
            'complete': 0,
            'incomplete': 0,
            'avg_completion': 0.0
        }
        
        total_combinations = 16  # 4 topics * 4 session types
        for attendee, sessions in attendee_sessions.items():
            total_sessions = sum(len(types) for types in sessions.values())
            if total_sessions == total_combinations:
                coverage['complete'] += 1
            else:
                coverage['incomplete'] += 1
            coverage['avg_completion'] += total_sessions
        
        coverage['avg_completion'] /= len(attendee_sessions)
        self.metrics['attendee_coverage'] = coverage
        return coverage
    
    def visualize_results(self):
        """Create visualizations of the evaluation metrics"""
        # Room utilization plot
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=list(self.metrics['room_utilization'].keys()),
            y=list(self.metrics['room_utilization'].values())
        )
        plt.title('Room Utilization (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('room_utilization.png')
        
        # Session distribution plot
        plt.figure(figsize=(12, 6))
        topics = self.metrics['topic_distribution']
        sns.barplot(x=list(topics.keys()), y=list(topics.values()))
        plt.title('Session Distribution by Topic')
        plt.tight_layout()
        plt.savefig('topic_distribution.png')

def main():
    # Create test scheduler with same parameters as main.py
    start_time = datetime(2024, 1, 1, 8, 0)
    end_time = datetime(2024, 1, 1, 18, 0)
    
    rooms = [
        Room("Classroom_1", 60),
        Room("Classroom_2", 60),
        Room("Classroom_3", 60),
        Room("Classroom_4", 60),
        Room("Classroom_5", 60),
        Room("Amphitheater", 180)
    ]
    
    topics = ["A", "B", "C", "D"]
    session_types = ["Theoretical", "Practical", "Historical", "Test"]
    
    scheduler = WorkshopScheduler(
        num_attendees=600,
        num_days=5,
        topics=topics,
        session_types=session_types,
        rooms=rooms,
        start_time=start_time,
        end_time=end_time
    )
    
    schedule = scheduler.generate_schedule()
    
    # Evaluate schedule
    evaluator = SchedulerEvaluator(schedule)
    
    print("\n=== Schedule Evaluation Results ===\n")
    
    print("Room Utilization:")
    for room, util in evaluator.evaluate_room_utilization().items():
        print(f"{room}: {util:.1f}%")
    
    print("\nTeacher Workload:")
    for teacher, sessions in evaluator.evaluate_teacher_workload().items():
        print(f"{teacher}: {sessions} sessions")
    
    print("\nSession Distribution:")
    distribution = evaluator.evaluate_session_distribution()
    print("Topics:", distribution['topics'])
    print("Types:", distribution['types'])
    
    print("\nAttendee Coverage:")
    coverage = evaluator.evaluate_attendee_coverage()
    print(f"Complete: {coverage['complete']}")
    print(f"Incomplete: {coverage['incomplete']}")
    print(f"Average Completion: {coverage['avg_completion']:.1f} sessions per attendee")
    
    # Generate visualizations
    evaluator.visualize_results()
    print("\nVisualization plots have been saved.")

if __name__ == "__main__":
    main()