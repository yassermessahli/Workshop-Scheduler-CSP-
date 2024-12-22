import React from 'react';

export const Alert = ({ children }) => (
  <div className="alert">
    {children}
  </div>
);

export const AlertDescription = ({ children }) => (
  <div className="alert-description">
    {children}
  </div>
);