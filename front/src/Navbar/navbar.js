import React, { useEffect, useState } from "react";
import "./navbar.css"; // Uvezivanje CSS fajla
import axios from "axios";
import Product from "../Product/product";
import ProizvodUKorpi from "../ProizvodUKorpi/proizvodUKorpi";

const Navbar = ({
  productsForCard,
  akcijskiProizvodi,
  addToCart,
  usernameKorisnika,
}) => {
  const [showCart, setShowCart] = useState(false); // Stanje koje će kontrolisati prikazivanje korpe
  const [akcijski, setAkcijski] = useState(false);
  const [akcijskiProizvodi1, setakcijskiProizvodi] = useState([]);
  const [kategorije, setKategorije] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [proizvodiPoKategorijama, setProizvodiPoKategorijama] = useState([]);
  const [proizvodi, setProizvodi] = useState([]);

  useEffect(() => {
    const fetchAkcijskiProizvodi = async () => {
      try {
        const response = await axios.get(
          "http://localhost:5000/prikazi_akcijske_proizvode"
        );
        if (response.data) {
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

      console.log(
        "Proizvodi koji treba da se prikazu u korpi   ",
        productsForCard
      );
    };

    const fetctKategorije = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/vratiKategorije"
        );
        if (response.data) {
          setKategorije(response.data);
          console.log("Sve kategorije su : ", response.data);
        }
      } catch (error) {
        console.error(
          "Došlo je do greške prilikom dohvatanja kategorija proizvoda:",
          error
        );
      }
    };

    fetchAkcijskiProizvodi();
    fetctKategorije();
  }, []);

  const prikaziProizvodeUKorpi = async (emailKorisnika) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/prikaziProizvodeUKorpi",
        {
          korisnik_email: emailKorisnika,
        }
      );

      console.log(response.data);
      setProizvodi(response.data);
    } catch (error) {
      console.error("Greška prilikom dohvatanja proizvoda:", error);
    }
  };

  const kategorijaHandler = (kategorija) => {
    console.log(kategorija);

    ucitajProizvodePoKategoriji(kategorija);
  };

  const ucitajProizvodePoKategoriji = async (kategorija) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/products_by_category",
        {
          category: kategorija,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        console.log("Proizvodi po kategoriji:", response.data);
        setProizvodiPoKategorijama(response.data);

        // Ovde dalje možete manipulisati sa podacima koje dobijete
      } else {
        console.error(
          "Došlo je do greške prilikom dohvatanja proizvoda po kategoriji"
        );
      }
    } catch (error) {
      console.error(
        "Došlo je do greške prilikom dohvatanja proizvoda po kategoriji:",
        error
      );
    }
  };

  const akcijskiHandler = (event) => {
    event.preventDefault();
    console.log("petarr");
    console.log(akcijskiProizvodi1);
    setAkcijski(!akcijski);
  };

  const openCart = () => {
    setShowCart(true);

    prikaziProizvodeUKorpi(usernameKorisnika);
    console.log(proizvodi);
  };

  // Funkcija za zatvaranje korpe
  const closeCart = () => {
    setShowCart(false);
  };

  const KupiProizvodeHandler = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/kupi_proizvode",
        {
          korisnik_email: usernameKorisnika,
        }
      );

      console.log(response.data);

      // Obrada podataka
    } catch (error) {
      // Uhvatite grešku ako se desi
      console.error("Greška prilikom dohvatanja proizvoda:", error);
    }
  };

  return (
    <div>
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

              <li>
                <div class="dropdown">
                  <button class="dropbtn">Sortiranje proizvoda</button>
                  <div class="dropdown-content">
                    {/* Korišćenje kategorije.map() da se generišu linkovi */}
                    {kategorije.map((kategorija, index) => (
                      <a
                        href="#"
                        key={index}
                        onClick={() => kategorijaHandler(kategorija)}
                      >
                        {kategorija}
                      </a>
                    ))}
                  </div>
                </div>
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
              <h2 style={{ color: "black" }}>Proizvodi u korpi:</h2>

              {proizvodi.map((product, index) => (
                <ProizvodUKorpi
                  key={index}
                  product={product}
                  usernameKorisnika={usernameKorisnika}
                />
              ))}

              <button onClick={KupiProizvodeHandler}>Kupi proizvode </button>
              <button onClick={closeCart}>Zatvori</button>
            </div>
          </div>
        )}

        {/* Prikaz proizvoda po kategoriji */}
      </header>

      <div className="proizvodi-container">
        <div style={{ textAlign: "center", width: "100%" }}>
          <h1>Akcijski proizvodi</h1>
        </div>
        {akcijskiProizvodi1.map((proizvod, index) => (
          <div className="proizvod-wrapper" key={index}>
            <Product key={index} product={proizvod} addToCart={addToCart} />
            {/* Ostali detalji proizvoda */}
          </div>
        ))}
      </div>

      <div className="proizvodi-container">
        <div style={{ textAlign: "center", width: "100%" }}>
          <h1>Sortirani proizvodi</h1>
        </div>
        {proizvodiPoKategorijama.map((proizvod, index) => (
          <div className="proizvod-wrapper" key={index}>
            <Product key={index} product={proizvod} addToCart={addToCart} />
            {/* Ostali detalji proizvoda */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Navbar;
