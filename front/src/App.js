import 'bootstrap/dist/css/bootstrap.min.css';

import logo from "./logo.svg";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthContextProvider } from './UserContext/UserContext';
import "./App.css";

import Login from "./Login/login";
import Home from "./Home/home"
import Register from "./Register/register";
import Navbar from "./Navbar/navbar";

function App() {
  return (
    <AuthContextProvider>
     
    <Router>
     
      

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Register" element={<Register />} />
        <Route path="/Home" element={<Home />} />
        { <Route path="/Navbar" element={<Navbar />} /> }
        {/* Dodajte ostale rute ovde */}
      </Routes>
    </Router>
    </AuthContextProvider>
  );
}

export default App;
