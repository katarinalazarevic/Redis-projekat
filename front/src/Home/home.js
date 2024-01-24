import React, { useEffect, useState, useContext, useReducer } from "react";
import "./home.css";
import axios from "axios";
import Product from "../Product/product";
import Button from '@mui/material/Button';



import { useAuth } from "../UserContext/UserContext";

import Navbar from "../Navbar/navbar";

const Home = ({ data }) => {
  const { username } = useAuth(); 

  const [proizvodi, setProizvodi] = useState([]);
  const [novih10, setNovih10] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showButton, setShowButton] = useState(true); 
  const [brojStranice, setBrojStranice] = useState(1);
  const [prikaziKorpu, setPrikaziKorpu] = useState(false);
  const [akcijski, setAkcijski] = useState(false);
  const [pomocna,setPomocna]= useState(1);


  const [prikaziNajpopularnijeProizvode, setprikaziNajpopularnijeProizvode]= useState(false);
  const [najpopularnijiProizvodi,setnajpopularnijiProizvodi ]= useState([]);



  const [prikaziNajaktivnije, setprikaziNajaktivnije]= useState(false);
  const [najaktivnijiKupci, setNajaktivnijeKupce]= useState([]);

  const [reducerValue,forceUpdate]=useReducer(x=>x+1,0);


  let [productsForCard, setProductsForCard] = useState([]);

  console.log("Email korisnika:", username);

  const prikaziNajaktivnijeHandler= ()=>
  {
      setprikaziNajaktivnije(!prikaziNajaktivnije);

      console.log("Prikazi najaktivnije korisnike je ",prikaziNajaktivnije);
  };


  const prikaziNajpopularnijeProizvodeHandler= ()=>
  {
      setprikaziNajpopularnijeProizvode(!prikaziNajpopularnijeProizvode);

     
  };



  const pribaviNajaktivnijeKupce = async ()=>
  {
    try {
      const response = await axios.get(
        `http://localhost:5000/ucitajNajaktivnijeKorisnike`
      );
     
      

      setNajaktivnijeKupce(response.data);
      

      console.log("Odgovor od servera:", response.data);
      
    } catch (error) {
      console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
    }
  };
  

  const pribaviNajpopularnijeProizvode = async ()=>
  {
    try {
      const response = await axios.get(
        `http://localhost:5000/vratiNajpopularnijeproizvode`
      );
     
      

     setnajpopularnijiProizvodi(response.data);
      

      console.log("Odgovor od servera:", response.data);
      
    } catch (error) {
      console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
    }
  };



  useEffect(() => {
    console.log('Niz proizvoda za korpu:', productsForCard);
    setPrikaziKorpu(true);
    pribaviNajaktivnijeKupce();
    pribaviNajpopularnijeProizvode();

  }, [productsForCard]);

  const KorpaHandler = () => {
    setPrikaziKorpu(!prikaziKorpu);
  };

  const dohvatiProizvodeNaStranici = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/ucitavajPo10Proizvoda/${brojStranice}`
      );
     
      const novih10 = response.data.proizvodi;

     
      setProizvodi((prevProizvodi) => [...prevProizvodi, ...novih10]);

      console.log("Odgovor od servera:", response.data);
      
    } catch (error) {
      console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
    }
  };

  const handleClick = async () => {
    try {
      
      setShowButton(false);
      setBrojStranice((prevStranica) => prevStranica + 1);
      console.log("Broj stranice je ", brojStranice);
      const response = await dohvatiProizvodeNaStranici();
      console.log("Odgovor od servera:", response);
    } catch (error) {
      
      console.error("Greška prilikom dohvaćanja podataka:", error);
    }
  };

  

  const ocistiKorpu = () => {
    setProductsForCard([]);
   
    console.log(productsForCard);
  };

  const addToCart = async (productId) => {
    if (productsForCard.includes(productId)) {
      window.confirm("Proizvod je vec u korpi!");
      return; 
    }
    productsForCard=[...productsForCard, productId];
    setProductsForCard(productsForCard);
   const p= productId+"";
   console.log(p);
   

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/dodaj_u_korpu",
        {
          korisnik_email: username,
          proizvodi_id: p
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response);

      if (response.status === 200) {
        console.log("Proizvodi uspešno dodati u korpu");
        setPomocna(0); 
        setPrikaziKorpu(true);
       
       
      } else {
        console.log("Greška prilikom dodavanja proizvoda u korpu");
        window.confirm("Greška prilikom dodavanja proizvoda u korpu");
      }
    } catch (error) {
      
      console.error(
        "Došlo je do greške prilikom dodavanja proizvoda u korpu:",
        error
      );
      window.confirm("Greška prilikom dodavanja proizvoda u korpu");
    }
  };

  return (
    <>
      <div class="akcijskiProizvodi">
        {(pomocna===1  || pomocna ===0 ) &&  (
          <Navbar productsForCard={productsForCard} akcijskiProizvodi={akcijski} addToCart={addToCart} usernameKorisnika={username} 
          prikaziNajaktivnijeHandler={prikaziNajaktivnijeHandler}  prikaziNajpopularnijeProizvodeHandler={prikaziNajpopularnijeProizvodeHandler}/>

        )}

{prikaziNajaktivnije && (
  <div>
    <div style={{ textAlign: 'center'}}> <h1> NAJAKTIVNIJI KUPCI</h1> </div>
    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
      <thead>
        <tr>
          <th style={{ backgroundColor: '#f2f2f2', color:'red', padding: '10px', textAlign: 'center' }}>Ime</th>
          <th style={{ backgroundColor: '#f2f2f2', color:'red', padding: '10px', textAlign: 'center' }}>Prezime</th>
          <th style={{ backgroundColor: '#f2f2f2',color:'red', padding: '10px', textAlign: 'center' }}>Bodovi</th>
        </tr>
      </thead>
      <tbody>
        {najaktivnijiKupci.map((kupac, index) => (
          <tr key={index}>
            <td style={{ border: '1px solid #dddddd',color:'black', padding: '10px' }}>{kupac.ime}</td>
            <td style={{ border: '1px solid #dddddd',color:'black', padding: '10px' }}>{kupac.prezime}</td>
            <td style={{ border: '1px solid #dddddd',color:'black', padding: '10px' }}>{kupac.bodovi}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)}

{prikaziNajpopularnijeProizvode && (
  <div>
    <div style={{ textAlign: 'center' }}>
      <h1 style={{color:'red'}}> NAJPOPULARNIJI PROIZVODI </h1>
    </div>
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      {najpopularnijiProizvodi.map((product) => (
        <Product
          key={product.id}
          product={product}
          addToCart={addToCart}
        />
      ))}
    </div>
  </div>
)}



        <h1>Svi proizvodi</h1>
        <section className="sg-products">
          {/* ... */}
          <div className="product-grid">
            {[...proizvodi, ...novih10].map(([productId, product]) => (
              <Product
                key={productId}
                product={product}
                addToCart={addToCart}
              />
            ))}
            
          </div>
          
          {showButton ? ( 
            <div className="dugmeVidiJos btn-primary">
             
              <Button variant="contained" onClick={handleClick} >Prikazi proizvode</Button>
            </div>
          ) : (
            <div className="dugmeVidiJos btn-primary">
           
              <Button variant="contained" onClick={handleClick} >Vidi Jos</Button>

              
            </div>
          )}

          {/* {prikaziKorpu && <ShoppingCart indeksi={productsForCard} />} */}
        </section>
      </div>
    </>
  );
};

export default Home;
