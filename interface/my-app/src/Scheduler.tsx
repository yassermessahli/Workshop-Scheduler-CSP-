import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { motion } from 'framer-motion';
import { Calendar, Clock } from 'lucide-react';
import './index.css';
import App from './App';
import { useNavigate } from 'react-router-dom';


const SchedulerInterface = () => {
  const [formData, setFormData] = useState({
    numAttendees: 600,
    numDays: 5,
    topics: ['A', 'B', 'C', 'D'],
    sessionTypes: ['Theoretical', 'Practical', 'Historical', 'Test'],
    startTime: '08:00',
    endTime: '18:00',
    rooms: [
      { name: 'Classroom 1', capacity: 60 },
      { name: 'Classroom 2', capacity: 60 },
      { name: 'Classroom 3', capacity: 60 },
      { name: 'Classroom 4', capacity: 60 },
      { name: 'Classroom 5', capacity: 60 },
      { name: 'Amphitheater', capacity: 180 }
    ]
  });

  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeDay, setActiveDay] = useState(1);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
  
    try {
      const response = await fetch('http://localhost:5000/generate-schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
  
      if (!response.ok) {
        throw new Error('Failed to generate schedule');
      }
  
      const data = await response.json();
      setSchedule(data);
      // Navigate to Results component if successful
      if (data) {
        navigate('/results', { state: { schedule: data } });
      }
    } catch (err) {
      setError('Failed to generate schedule. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-4"
      >
        <h1 className="text-3xl font-bold text-center">Workshop Scheduler</h1>
        <p className="text-gray-600 text-center">Enter your constraints to generate an optimized workshop schedule.</p>
      </motion.div>

      <motion.form
        onSubmit={handleSubmit}
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white p-6 rounded-lg shadow"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Number of Attendees</label>
            <input
              type="number"
              name="numAttendees"
              value={formData.numAttendees}
              onChange={handleInputChange}
              className="w-full p-2 border rounded"
              min="1"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Number of Days</label>
            <input
              type="number"
              name="numDays"
              value={formData.numDays}
              onChange={handleInputChange}
              className="w-full p-2 border rounded"
              min="1"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Start Time</label>
            <input
              type="time"
              name="startTime"
              value={formData.startTime}
              onChange={handleInputChange}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">End Time</label>
            <input
              type="time"
              name="endTime"
              value={formData.endTime}
              onChange={handleInputChange}
              className="w-full p-2 border rounded"
            />
          </div>
        </div>

        <div className="space-y-4">
          {/* Add other form fields here */}
        </div>

        <div className="col-span-2">
          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Schedule'}
          </button>
        </div>
      </motion.form>

      {error && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="alert bg-red-100 text-red-700 p-4 rounded"
        >
          <div className="alert-description">{error}</div>
        </motion.div>
      )}

      {/* Render the schedule here */}
    </div>
  );
};


export default SchedulerInterface;