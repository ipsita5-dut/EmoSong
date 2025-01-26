// src/components/Signup.js
import React, { useState } from 'react';
import '../styles/signup.css'; // Import your signup styles

const Signup = () => {
    const [fName, setFName] = useState('');
    const [lName, setLName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [terms, setTerms] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Add your signup logic here
    };

    return (
        <div className="container">
            <div className="left">
                <img alt="Mountain view" src="https://storage.googleapis.com/a1aa/image/GWJUgtnXf6WezE3pENKUuvs1CRDQTWKOr8TuS1CF3Ae ```javascript
                9nA.jpg" />
                <div className="overlay">
                    <div className="back">
                        <i className="fas fa-arrow-left"></i>
                        Back to website
                    </div>
                    <div className="caption">Capturing Moments, Creating Memories</div>
                </div>
            </div>
            <div className="right">
                <h2>Create an account</h2>
                <p>Already have an account? <a href="/login">Log in</a></p>
                <form onSubmit={handleSubmit}>
                    <input type="text" placeholder="First name" required value={fName} onChange={(e) => setFName(e.target.value)} />
                    <input type="text" placeholder="Last name" required value={lName} onChange={(e) => setLName(e.target.value)} />
                    <input type="email" placeholder="Email" required value={email} onChange={(e) => setEmail(e.target.value)} />
                    <input type="password" placeholder="Password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                    <div className="checkbox-container">
                        <input type="checkbox" id="terms" checked={terms} onChange={() => setTerms(!terms)} />
                        <label htmlFor="terms">I agree to the <a href="#">Terms & Conditions</a></label>
                    </div>
                    <button type="submit">Create account</button>
                </form>
                <div className="or-register">Or register with</div>
                <div className="social-buttons">
                    <button><i className="fab fa-google"></i> Google</button>
                    <button><i className="fab fa-apple"></i> Apple</button>
                </div>
            </div>
        </div>
    );
};

export default Signup;