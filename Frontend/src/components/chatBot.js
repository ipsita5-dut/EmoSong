// src/components/Chatbot.js
// import React, { useState } from 'react';
import '../styles/chatbot.css'; // Create a CSS file for styling
import React, {  useEffect, useRef, useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const chatMessagesRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');


  useEffect(()=>{
    document.body.classList.add('chatbot-body');
    return()=>{
      document.body.classList.remove('chatbot-body');
    }
  },[]);

  useEffect(()=>{

    // Add default welcome message
    const defaultMessage = {
      id: Date.now(),
      text: "🎵 Welcome to MelodyMate! Share how you're feeling, and I'll recommend a perfect song for your vibe! 🌸",
      sender: 'bot'
    };
    setMessages(prevMessages => [...prevMessages, defaultMessage]);

    scrollToBottom();
  }, []);

  const scrollToBottom = () => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  };

   

  const handleSendMessage = async() => {
    if (!userInput.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: userInput,
      sender: 'user'
    };
    setMessages(prevMessages => [...prevMessages, userMessage]);

    // Call the chatbot API
    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', {
        input: userInput},
        { headers: { 'Content-Type': 'application/json' }
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'bot',
        mood: response.data.mood, // Mood detected by backend

      };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error communicating with the chatbot:', error);
    }

    // Clear input
    setUserInput("");
    scrollToBottom();
  };
  return (
    <div className="c-container">
      <div className="background">
        <div className="decor decor-left"></div>
        <div className="decor decor-right"></div>
      </div>

      {/* Main Content */}
      <div className="c-content">
        <div className="text-section">
          <p>Hi there, welcome to<strong>Melody Mate!</strong></p>
          <p>Let’s find you the perfect melody for your mood! 🎶</p>
        </div>
        <img 
          src="https://media1.tenor.com/m/KWI-Ict8_gEAAAAd/hi-there.gif" 
          alt="Person waving" 
          className="main-image" 
          style={{ height: '95px', width: '90px' }} 
        />
      </div>

      {/* Chatbot Section */}
      <div className="chat-section">
        <div className="chat-messages" ref={chatMessagesRef}>
          {messages.map((message) => (
            <div key={message.id} className={`chat-message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input type="text" placeholder="Type your message..." 
          value={userInput} 
          onChange={(e) => setUserInput(e.target.value)} />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;