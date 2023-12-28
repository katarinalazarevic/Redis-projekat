import "./login.css";
import { useRef, useState, useEffect, useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import axios from 'axios';
import React from "react";

import '../api/axios';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const handleRegisterClick = () => {
    // Navigacija na '/Register' rutu
    navigate("/Register");
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

   const  LoginHandler = async (event) => {
    event.preventDefault();
    // Dobijanje vrednosti iz ref objekata
    const emailValue = emailRef.current.value;
    const passwordValue = passwordRef.current.value;

    
    setEmail(emailValue);
    setPassword(passwordValue);

    const kupacId = 1; // Primer ID-ja kupca

    // Poziv funkcije koja šalje GET zahtev na server
    try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: email,
          password: password
        }, {
          headers: {
            'Content-Type': 'application/json'
            // Dodajte dodatne zaglavlja ako su potrebna (npr. autorizacija)
          }
        });
    
        // Obrada odgovora od servera
        console.log('Poruka o uspešnoj prijavi:', response.data.message);
        // Ovde možete izvršiti operacije nakon uspešne prijave
        // ovde ide navigate
        // Na primer, preusmerite korisnika na drugu stranicu nakon uspešne prijave
         navigate("/Home");
         
        
        return response.data; // Vratite odgovor sa servera ili neki drugi podatak koji vam je potreban
      } catch (error) {
        // Uhvatite i obradite grešku ako se desi
        console.error('Došlo je do greške prilikom prijave:', error);
        throw error; // Možete proslediti grešku dalje radi obrade ili prikaza korisniku
      }

    // Prikaz vrednosti iz stanja (radi provere)
   
  };

  const stampajVrednosti= (event)=>
  {
    event.preventDefault();
    console.log("Email:", email);
    console.log("Password:", password);
  }

  return (
    <div id="algn">
      <div id="container">
        <p className="head">Login</p>
        <form action="/" className="input-container">
          <input
            type="email"
            placeholder="Enter email"
            className="inpt"
            value={email}
            ref={emailRef}
            onChange={handleEmailChange}
            required
          />
          <input
            type="password"
            placeholder="Enter password"
            className="inpt"
            value={password}
            ref={passwordRef}
            onChange={handlePasswordChange}
            required
          />
          <div className="rem-forgot">
            <div className="rem">
              <input type="checkbox" id="rem-tik" />
              <label htmlFor="rem-tik">Remember me</label>
            </div>
            <span>
              <a href="#" onClick={stampajVrednosti}>Forgot password</a>
            </span>
          </div>
          <button type="submit" className="btn" onClick={LoginHandler}>
            Login
          </button>
        </form>
        <p className="footer">
          Don't have account?{" "}
          <a href="#" onClick={handleRegisterClick}>
            {" "}
            Register
          </a>
        </p>
      </div>
    </div>
  );
};

export default Login;
