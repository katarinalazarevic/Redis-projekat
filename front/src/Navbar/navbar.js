import React, { useEffect, useState } from "react";
import "./navbar.css"; // Uvezivanje CSS fajla
import axios from "axios";
import Product from "../Product/product";

const Navbar = ({ productsForCard, akcijskiProizvodi }) => {
  const [showCart, setShowCart] = useState(false); // Stanje koje će kontrolisati prikazivanje korpe
  const [akcijski, setAkcijski] = useState(false);
  const [akcijskiProizvodi1,setakcijskiProizvodi]=useState([]);

  useEffect(() => {
    const fetchAkcijskiProizvodi = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/prikazi_akcijske_proizvode"
        );
        if (response.data ) {
          //setAkcijski(response.data.proizvodi);
          setakcijskiProizvodi(response.data);
          console.log("Akcijski proizvodi:", response.data);
        } else {
                 
          console.error(
            "Podaci o akcijskim proizvodima nisu u očekivanom formatu."
          );
        }
      } catch (error) {
        console.error(
          "Došlo je do greške prilikom dohvatanja akcijskih proizvoda:",
          error
        );
      }
    };

    fetchAkcijskiProizvodi();
  }, []);

  const productsArray = Array.isArray(productsForCard)
    ? productsForCard
    : productsForCard
    ? Object.values(productsForCard)
    : [];

  const akcijskiHandler = (event) => {
    event.preventDefault();
    console.log("petarr")
    console.log(akcijskiProizvodi1)
    setAkcijski(!akcijski);
  };

  const openCart = () => {
    setShowCart(true);
  };

  // Funkcija za zatvaranje korpe
  const closeCart = () => {
    setShowCart(false);
  };

  return (
    <header className="header" id="header">
      <nav className="nav container">
        <div className="nav__menu" id="nav-menu">
          <ul className="nav__list">
            <li className="nav__item">
              <a className="nav__link" href="#">
                Profil
              </a>
            </li>

            <li className="nav__item">
              <a className="nav__link" href="#" onClick={akcijskiHandler}>
                Akcijski proizvodi
              </a>
            </li>
            <li className="nav__item">
              <a className="nav__link" href="#">
                {" "}
                Najpopularniji proizvodi
              </a>
            </li>
            <li className="nav__item">
              <a className="nav__link" href="#">
                Search
              </a>
            </li>
            <li className="nav__item">
              <a className="nav__link" href="#" onClick={openCart}>
                Korpa
              </a>
            </li>
          </ul>
          {/* Close button */}
          <div class="nav__close" id="nav-close">
            <i className="ri-close-line"></i>
          </div>
        </div>

        <div className="nav__actions">
          {/* Search button */}
          <i className="ri-search-line nav__search" id="search-btn"></i>
          {/* Login button */}
          <i className="ri-user-line nav__login" id="login-btn"></i>
          {/* Toggle button */}
          <div className="nav__toggle" id="nav-toggle">
            <i className="ri-menu-line"></i>
          </div>
        </div>
      </nav>
      {showCart && (
        <div className="cart-popup">
          <div className="cart-content">
            <h2>Proizvodi u korpi:</h2>
            <ul>
              {productsArray.map((productId, product) => (
                <li style={{ color: 'black' }} key={product}>
               <Product
                key={productId}
                product={product}
              
              />
              </li>
              
              ))}
            </ul>
            <button onClick={closeCart}>Zatvori</button>
          </div>
        </div>
      )}

      {akcijskiProizvodi1  && akcijskiProizvodi1.length > 0 ? (
        <div className="akcijski-proizvodi">
          <h2>Akcijski proizvodi:</h2>
          <ul>
            {akcijskiProizvodi1.map((proizvod, index) => (
              <li key={index}>Proizvod {proizvod.producerName}</li>
              
            ))}
          </ul>
        </div>
      ) : akcijski ? (
        <div className="akcijski-proizvodi">
          <p>Nema akcijskih proizvoda.</p>
        </div>
      ) : null}
    </header>
  );
};

export default Navbar;
