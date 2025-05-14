import React from 'react';
import './Button.css';

const Button = ({ children, type = 'primary', onClick, className = '', ...props }) => {
  return (
    <button 
      className={`btn btn-${type} ${className}`}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;