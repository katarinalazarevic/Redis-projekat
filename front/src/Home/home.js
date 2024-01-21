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
  const [reducerValue,forceUpdate]=useReducer(x=>x+1,0);


  let [productsForCard, setProductsForCard] = useState([]);

  console.log("Email korisnika:", username);

  useEffect(() => {
    console.log('Niz proizvoda za korpu:', productsForCard);
    setPrikaziKorpu(true);
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
          <Navbar productsForCard={productsForCard} akcijskiProizvodi={akcijski} addToCart={addToCart} usernameKorisnika={username} />

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
              <button onClick={handleClick}>Prikaži proizvode</button>
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
