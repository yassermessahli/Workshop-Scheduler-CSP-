# Educational Workshop Scheduler

A Python-based solution for scheduling large-scale educational workshops with an interactive web interface. The system handles multiple constraints including room capacities, teacher availability, and session requirements.

## Features

- Interactive web interface for inputting constraints
- Real-time schedule visualization
- Handles multiple session types (Theoretical, Practical, Historical, Test)
- Manages room allocations and capacity constraints
- Tracks teacher availability
- Ensures all attendees complete required sessions
- Supports flexible scheduling parameters
- Generates readable schedule output

## Prerequisites

### Backend
- Python 3.7 or higher
- Flask
- Flask-CORS

### Frontend
- Node.js 14.0 or higher
- npm (Node Package Manager)

## Project Structure

```
project/
│
├── main.py          # Main scheduling algorithm
├── api.py            # Flask API for the interface
├── code/              # Folder for additional modules
│   ├── ...
│   └── ...
├── interface/         # React frontend
│   ├── src/
│   ├── package.json
│   └── ...
├── README.md         # Instructions to run the project
└── requirements.txt  # Python dependencies
```

## Installation

1. download this zip file and extract it to your desired location

2. Navigate to the project directory
```bash
cd project
```

### Backend Setup

3. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. Install Python dependencies
```bash
pip install -r requirements.txt
```

### Frontend Setup

5. Navigate to the interface directory
```bash
cd interface
```

6. Install frontend dependencies
```bash
npm install
```

## Running the Application

### Start the Backend Server

1. Navigate to the project root directory
```bash
cd ..
```

2. Start the Flask backend server:
```bash
python api.py
```
The backend server will run on http://localhost:5000

### Start the Frontend Server

1. Navigate to the interface directory then my-app
```bash
cd interface/my-app
```

2. install the react-scripts
```bash
npm install 
```

3. Start the React frontend:
```bash
npm start
```
The frontend will run on http://localhost:3000

3. Open your browser and navigate to http://localhost:3000

## Using the Interface

1. Enter the scheduling constraints:
   - Number of attendees
   - Number of days
   - Start and end times
   - Room configurations
   - Topics and session types

2. Click "Generate Schedule" to create the schedule

3. View the generated schedule:
   - Navigate between days using the day selector
   - View session details including room, time, and attendee count
   - Sessions are color-coded by type

## Command Line Usage

You can still run the scheduler without the interface:
```bash
python main.py
```

## Output

The program generates:
- Interactive web visualization of the schedule
- Day-by-day schedule showing:
  - Session timings
  - Room assignments
  - Teacher allocations
  - Number of attendees per session
  - Topic and session type details

## Constraints Handled

- Room capacity limits
- Teacher availability
- Session timing requirements
- Break periods between sessions
- Lunch break scheduling
- Attendee session requirements

## Error Handling

The system includes validation for:
- Room availability
- Teacher availability
- Time slot validity
- Attendee scheduling conflicts
- Input constraint validation

ربي يوفق