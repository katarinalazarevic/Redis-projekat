import logo from "./logo.svg";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import "./App.css";

import Login from "./Login/login";
import Home from "./Home/home"
import Register from "./Register/register";

function App() {


  



  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Register" element={<Register />} />
        <Route path="/Home" element={<Home />} />


        {/* Dodajte ostale rute ovde */}
      </Routes>
    </Router>
  );
}

export default App;
