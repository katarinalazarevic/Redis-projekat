//import "./login.css";
import { useRef, useState, useEffect, useContext } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import axios from "axios";
import React from "react";
import ErrorModal from "../Error/ErrorModal";
import UserContext from '../UserContext/UserContext';
import Failure from "../images/cancel.png";
import Succes1 from "../images/check.png";
import { AuthContext } from "../UserContext/UserContext";
import "./login.css"


import "../api/axios";

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  
  const authCtx = useContext(AuthContext); //sluzi za prosledjivanje 


  const [error, setError] = useState(false);
  const [errMsg, setErrMsg] = useState("");
  const [success, setSuccess] = useState(false);

  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const handleRegisterClick = () => {

    navigate("/Register");
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const errorHandler = () => {
    setError(null);
  };

  const LoginHandler = async (event) => {
    event.preventDefault();
    
    const emailValue = emailRef.current.value;
    const passwordValue = passwordRef.current.value;

    setEmail(emailValue);
    setPassword(passwordValue);

    const kupacId = 1;

    // Poziv funkcije koja šalje GET zahtev na server
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/login",
        {
          email: email,
          password: password,
        },
        {
          headers: {
            "Content-Type": "application/json",
            
          },
        }
      );

      console.log(response);

      if (response.status === 200) {
        if (response.data.message === "SUCCESS") {
          console.log("Poruka o uspešnoj prijavi:", response.data.message);
         
          authCtx.login('dummy-token', email);
          return navigate("/Home");
        } else {
          console.log(
            "Neuspešna prijava! Status kod 200, ali prijava neuspešna."
          );
          window.confirm("Neuspešna prijava!");
         
        }
      } else {
        console.log("Neuspešna prijava! Status kod nije 200.");
        window.confirm("Neuspešna prijava!");
       
      }
    } catch (error) {
      
      console.error("Došlo je do greške prilikom prijave:", error);
      window.confirm("Neuspešna prijava!");
    
    }
    
  };

  const stampajVrednosti = (event) => {
    event.preventDefault();
    console.log("Email:", email);
    console.log("Password:", password);
  };

  return (
    
    <div>
      {error && (
        <ErrorModal
          title={error.title}
          message={error.message}
          slika={error.slika}
          ugasiProzor={errorHandler}
        />
      )}
      <div id="algn">
        <div id="containerLogin">
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
    </div>
  
  );
};

export default Login;
