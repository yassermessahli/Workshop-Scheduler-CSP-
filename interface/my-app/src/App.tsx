import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Results from './Results.tsx';
import Scheduler from './Scheduler.tsx';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Scheduler />} />
        <Route path="/results" element={<Results />} /> {/* Remove static props */}
      </Routes>
    </Router>
  );
};

export default App;