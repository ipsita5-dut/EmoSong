// src/components/Login.js
import React, { useState } from 'react';
import '../styles/login.css'; // Import your login styles

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Add your login logic here
    };

    return (
        <div className="container">
            <div className="left">
                <img alt="Desert landscape" src="https://storage.googleapis.com/a1aa/image/OaDjwIhzzILfVSPYMcvUBM7FJ36ZiLgkRMgyBexey2lf8B8PB.jpg" />
            </div>
            <div className="right-section">
                <form onSubmit={handleSubmit}>
                    <h2>Welcome Back!</h2>
                    <p>Enter your email and password</p>
                    <div className="input-group">
                        <label htmlFor="email">Email address</label>
                        <div className="input-field">
                            <input type="email" id="user_mail_id" placeholder="Enter Your email" required value={email} onChange={(e) => setEmail(e.target.value)} />
                        </div>
                    </div>
                    <div className="input-group">
                        <label htmlFor="password">Password</label>
                        <div className="input-field">
                            <input type="password" id="password" placeholder="Enter your password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                    </div>
                    <a href="#" className="forgot-password">Forgot Password?</a>
                    <button type="submit" className="btn-signin">Sign in</button>
                </form>
            </div>
        </div>
    );
};

export default Login;