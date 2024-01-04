import React, { useEffect, useState, useContext } from "react";
import "./home.css";
import axios from "axios";
import Product from "../Product/product";
import Cart from "../Cart/cart";
import ShoppingCart from "../Cart/cart";

// Prilagodite putanju do vašeg UserContext fajla
import { useAuth } from "../UserContext/UserContext";

import Navbar from "../Navbar/navbar";

const Home = ({ data }) => {
  const { username } = useAuth(); // prima podatke iz login

  const [proizvodi, setProizvodi] = useState([]);
  const [novih10, setNovih10] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showButton, setShowButton] = useState(true); // Postavite početno stanje flag-a na true ili false u zavisnosti od potrebe
  const [brojStranice, setBrojStranice] = useState(1);
  const [prikaziKorpu, setPrikaziKorpu] = useState(false);
  const [akcijski, setAkcijski] = useState(false);


  let [productsForCard, setProductsForCard] = useState([]);

  console.log("Email korisnika:", username);

  useEffect(() => {
    console.log('Niz proizvoda za korpu:', productsForCard);
    
  }, [productsForCard]);

  const KorpaHandler = () => {
    setPrikaziKorpu(!prikaziKorpu);
  };

  const dohvatiProizvodeNaStranici = async () => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:5000/ucitavajPo10Proizvoda/${brojStranice}`
      );
      // const response = await axios.get('http://127.0.0.1:5000/ucitavajPo10Proizvoda');
      const novih10 = response.data.proizvodi;

      // Ažuriranje stanja proizvoda
      setProizvodi((prevProizvodi) => [...prevProizvodi, ...novih10]);

      console.log("Odgovor od servera:", response.data);
      // Ovdje možete obraditi odgovor od servera
    } catch (error) {
      console.error("Došlo je do greške prilikom dohvaćanja proizvoda:", error);
    }
  };

  const handleClick = async () => {
    try {
      // Ovdje možete manipulirati ili prikazati odgovor dobiven od servera
      setShowButton(false);
      setBrojStranice((prevStranica) => prevStranica + 1);
      console.log("Broj stranice je ", brojStranice);
      const response = await dohvatiProizvodeNaStranici();
      console.log("Odgovor od servera:", response);
    } catch (error) {
      // Uhvatite grešku ako dođe do problema prilikom poziva
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
      return; // Prekida se izvršavanje funkcije jer proizvod već postoji u korpi
    }
    productsForCard=[...productsForCard, productId];
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
        setPrikaziKorpu(true);
        // Dodatna logika nakon uspešnog dodavanja u korpu
      } else {
        console.log("Greška prilikom dodavanja proizvoda u korpu");
        window.confirm("Greška prilikom dodavanja proizvoda u korpu");
      }
    } catch (error) {
      // Uhvatite i obradite grešku ako se desi, ovo se odnosi na greške koje nisu vezane za statusni kod odgovora (npr. problem sa mrežom, itd.)
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
        <Navbar productsForCard={[1, 2, 3]} akcijskiProizvodi={akcijski} />
        <h1>Akcijski proizvodi</h1>
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
            {prikaziKorpu && (
              <Cart usernameKorisnika={username}>
                {" "}
                ocistiKorpu={ocistiKorpu}{" "}
              </Cart>
            )}
          </div>
          <button onClick={ocistiKorpu}> Ocisti korpu </button>
          <button onClick={KorpaHandler}> Prikazi Korpu</button>
          {showButton ? ( // Provera da li treba prikazati dugme na osnovu vrednosti flag-a
            <div className="dugmeVidiJos btn-primary">
              <button onClick={handleClick}>Prikaži proizvode</button>
            </div>
          ) : (
            <div className="dugmeVidiJos btn-primary">
              <button onClick={handleClick}>Vidi Još</button>
            </div>
          )}

          {/* {prikaziKorpu && <ShoppingCart indeksi={productsForCard} />} */}
        </section>
      </div>
    </>
  );
};

export default Home;
