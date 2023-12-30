import { useEffect, useState } from "react";
import axios from "axios";
import Product from "../Product/product";

const ShoppingCart = ({ indeksi }) => {
  const [proizvodi, setProizvodi] = useState([]);

  useEffect(() => {
    const fetchProizvodi = async () => {
      try {
        const response = await axios.get('http://localhost:5000/vratiProizvode');
        // Provjerite strukturu podataka koje dobijete sa servera
        if (response.data && response.data.proizvodi && Array.isArray(response.data.proizvodi)) {
          setProizvodi(response.data.proizvodi);
        } else {
          console.error("Struktura podataka sa servera nije ispravna.");
        }
      } catch (error) {
        console.error("Greška prilikom dohvatanja proizvoda:", error);
      }
    };

    fetchProizvodi();
  }, [indeksi]);

  return (
    <div className="shopping-cart">
      <h1>Shopping Cart</h1>
      {/* Prikaz informacija o proizvodima iz niza proizvodi */}
      {proizvodi.map((product) => (
       <Product product={product}> </Product>
      ))}
    </div>
  );
};

export default ShoppingCart;
