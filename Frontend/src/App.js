// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/Home';
// import Login from './components/Login';
// import Signup from './components/Signup';
import CaptureMood from './components/CaptureMood';
import Chatbot from './components/chatBot';

// import './styles/header.css';
// import './styles/footer.css';
import './styles/home.css';
// import './styles/login.css';
// import './styles/signup.css';
// import './styles/captureMood.css';

// const App = () => {
//     return (
//         <Router>
//             <Routes>
//                 <Route path="/" element={<Home />} />
//                 <Route path="/home" element={<Home />} />

//                 <Route path="/login" element={<Login />} />
//                 <Route path="/signup" element={<Signup />} />
//                 <Route path="/capture-mood" element={<CaptureMood />} />
//             </Routes>
//         </Router>
//     );
// };

const App = () => {
    return (
        <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/capture-mood" element={<CaptureMood />} /> Add the CaptureMood route
          <Route path="/chatbot" element={<Chatbot />} />

        </Routes>
      </Router>  
    );
  };
export default App;