import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
// import Dashboard from './components/Dashboard';
// import Logout from './components/Logout';
// import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home';

// The main App component defines all the routes
const App = () => {
  return (
    <div>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} /> */}
        
        {/* <Route path="/logout" element={<Logout />} /> */}

        <Route path="/" element={<Home/>} />
      </Routes>
    </div>
  );
};

export default App;
