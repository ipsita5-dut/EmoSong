// src/api.js
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://your-api-url.com', // Replace with your API URL
});

export const loginUser  = (email, password) => {
    return api.post('/user/login', { email, password });
};

export const registerUser  = (fName, lName, email, password) => {
    return api.post('/user/register', { fName, lName, email, password });
};

// Add more API functions as needed