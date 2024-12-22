import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Clock, Users, MapPin } from 'lucide-react';
import { useLocation } from 'react-router-dom';

interface Session {
  attendees: number;
  room: string;
  time: string;
  topic: string;
  type: string;
}

interface DaySchedule {
  day: number;
  sessions: Session[];
}



const Results = () => {
  const [activeDay, setActiveDay] = useState(1);
  const { schedule } = useLocation().state as { schedule: DaySchedule[] };

  const typeColors = {
    'Theoretical': 'bg-blue-100 border-blue-500 text-blue-800',
    'Practical': 'bg-green-100 border-green-500 text-green-800',
    'Historical': 'bg-yellow-100 border-yellow-500 text-yellow-800',
    'Test': 'bg-red-100 border-red-500 text-red-800'
  };

  const timeSlots = ['08:00', '11:00', '14:00', '17:00'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-7xl mx-auto"
      >
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-blue-600">Workshop Schedule</h1>
          <button
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Back to Form
          </button>
        </div>

        {/* Day Tabs */}
        <div className="flex space-x-2 mb-6 overflow-x-auto">
          {schedule.map((day) => (
            <button
              key={day.day}
              onClick={() => setActiveDay(day.day)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeDay === day.day
                  ? 'bg-blue-600 text-white'
                  : 'bg-white hover:bg-gray-50'
              }`}
            >
              Day {day.day}
            </button>
          ))}
        </div>

        {/* Schedule Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {timeSlots.map((timeSlot) => (
            <div key={timeSlot} className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-700 flex items-center gap-2">
                <Clock size={18} />
                {timeSlot}
              </h3>
              <div className="space-y-3">
                {schedule
                  .find((d) => d.day === activeDay)
                  ?.sessions.filter((s) => s.time === timeSlot)
                  .map((session, idx) => (
                    <motion.div
                      key={`${session.room}-${idx}`}
                      initial={{ scale: 0.95, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ delay: idx * 0.1 }}
                      className={`p-4 rounded-lg border-l-4 shadow-sm ${
                        typeColors[session.type as keyof typeof typeColors]
                      }`}
                    >
                      <div className="font-semibold mb-2">Topic {session.topic}</div>
                      <div className="text-sm space-y-1">
                        <div className="flex items-center gap-2">
                          <MapPin size={14} />
                          {session.room}
                        </div>
                        <div className="flex items-center gap-2">
                          <Users size={14} />
                          {session.attendees} attendees
                        </div>
                        <div className="text-sm font-medium">
                          {session.type}
                        </div>
                      </div>
                    </motion.div>
                  ))}
              </div>
            </div>
          ))}
        </div>

        {/* Legend */}
        <div className="mt-8 p-4 bg-white rounded-lg shadow-sm">
          <h3 className="font-semibold mb-2">Session Types</h3>
          <div className="flex gap-4 flex-wrap">
            {Object.entries(typeColors).map(([type, color]) => (
              <div key={type} className="flex items-center">
                <div className={`w-4 h-4 rounded ${color.split(' ')[0]}`} />
                <span className="ml-2 text-sm text-gray-600">{type}</span>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Results;