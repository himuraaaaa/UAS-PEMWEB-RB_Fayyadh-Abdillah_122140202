import { useState } from 'react';

const useForm = (initialState = {}) => {
  const [values, setValues] = useState(initialState);
  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setValues({
      ...values,
      [name]: value
    });
    
    // Clear error when field is updated
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: null
      });
    }
  };
  
  const reset = () => {
    setValues(initialState);
    setErrors({});
  };
  
  return {
    values,
    errors,
    setErrors,
    handleChange,
    reset,
    setValues
  };
};

export default useForm;