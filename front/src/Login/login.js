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


  useEffect(() => {
    console.log('Email:', email);
  }, [email]);

  useEffect(() => {
    console.log('Password:', password);
   
  }, [password]);


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
        const response = await axios.get(`http://127.0.0.1:5000/vratiKupca/${kupacId}`, {
          headers: {
            'Content-Type': 'application/json'
            // Dodajte dodatne zaglavlja ako su potrebna (npr. autorizacija)
          }
        });
    
        // Obrada odgovora od servera (response.data sadrži podatke koji su poslati)
        console.log('Podaci o kupcu:', response.data);
        // Ovde možete izvršiti operacije na dobijenim podacima
      } catch (error) {
        // Uhvatite i obradite grešku ako se desi
        console.error('Došlo je do greške:', error);
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
            ref={emailRef}
            required
          />
          <input
            type="password"
            placeholder="Enter password"
            className="inpt"
            ref={passwordRef}
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
