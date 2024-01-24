import { Navigate, useNavigate } from 'react-router-dom';
import  './register.css'
import { useState } from 'react';
import axios from 'axios';
const  Register = () =>
{

  const navigate = useNavigate();
  const [ime, setIme] = useState("");
  const [prezime, setprezime] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [grad, setGrad] = useState("");
  const [ulica, setulica] = useState("");
  const [broj, setBroj] = useState("");

  const RegisterHandler= async (event)=>
  {
    event.preventDefault();
    console.log(ime,prezime,email,password,grad,ulica,broj);
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/register",
        {
          email: email,
          password: password,
          ime:ime,
          prezime:prezime,
          grad:grad,
          ulica:ulica,
          broj:broj
        },
        {
          headers: {
            "Content-Type": "application/json",
            
          },
        }
      );

      console.log(response);

      if (response.status === 201) {
        if (response.data.message === "SUCCESS") {
          console.log("Poruka o uspešnoj prijavi:", response.data.message);
          navigate("/");
          return response.data;
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
  }
  const handleEmailChange = (event) => {
   
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };


  const handleImelChange = (event) => {
    setIme(event.target.value);
  };

  const handlePrezimeChange = (event) => {
    setprezime(event.target.value);
  };
  const handleGradChange = (event) => {
    setGrad(event.target.value);
  };

  const handleUlicaChange = (event) => {
    setulica(event.target.value);
  };
  const handleBrojChange = (event) => {
    setBroj(event.target.value);
  };


   const LoginHandler= ()=>
  {
    navigate('/');
  };


    return (
<div id="algn">
        <div id="containerregister">
          <p className="head">Register</p>
          <form action="/" className="input-container">
            <input type="text" placeholder="Ime" className="inpt" onChange={handleImelChange} required />
            <input type="text" placeholder="Prezime" className="inpt" onChange={handlePrezimeChange} required />
            <input type="email" placeholder="Enter email" className="inpt" onChange={handleEmailChange} required />
            <input type="password" placeholder="Enter password" className="inpt" onChange={handlePasswordChange} required />
            <input type="text" placeholder="Ulica" className="inpt" required  onChange={handleUlicaChange}/>
            <input type="text" placeholder="Grad" className="inpt" required onChange={handleGradChange} />
            <input type="text" placeholder="Broj" className="inpt" onChange={handleBrojChange} required />

            
            <button  className="btn" onClick={RegisterHandler}>Register</button>
          </form>
          <p className="footer" onClick={LoginHandler}>Vec imate akaunt?  <a href="#">Login</a></p>
        </div>
      </div>
    );

}

export default Register;