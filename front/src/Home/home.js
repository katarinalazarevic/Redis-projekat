import React, { useEffect, useState } from "react";
import './home.css';
import axios from 'axios';
import Product from "../Product/product";


const Home = () => {
  const [proizvodi, setProizvodi] = useState([]);
  const [novih10,setNovih10]= useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showButton, setShowButton] = useState(true); // Postavite početno stanje flag-a na true ili false u zavisnosti od potrebe

  let brojStranice=1;

  useEffect(() => {
    const fetchProizvodi = async () => {
      try {
        const response = await axios.get('http://localhost:5000/prvih_deset_proizvoda');
        setProizvodi(response.data.proizvodi);
      } catch (error) {
        console.error('Došlo je do greške prilikom dohvatanja podataka:', error);
      }
    };

    fetchProizvodi();
  }, []);

  useEffect(() => {
    // Ovde možete pozvati funkciju ili izvršiti određenu logiku nakon što se komponenta učita
    console.log('Ucita li smo novih 10 proizvoda.');
    console.log(novih10);
    brojStranice++;
  }, [novih10]);

  useEffect(() => {
    // Ovde možete pozvati funkciju ili izvršiti određenu logiku nakon što se komponenta učita
    console.log('Komponenta se upravo učitala.');
    console.log(proizvodi);
  }, [proizvodi]);


  const ucitajNova10= async ()=>
  {
    brojStranice++;
    console.log(`ulazimo u ucitajNova10 i poziva fja za vrednost: ${brojStranice}`)
    try {
        const response = await axios.post('http://localhost:5000/ucitaj_narednih_10',
        {
          stranica: brojStranice
        });
        if (response.data.proizvodi.length > 0) {
          setNovih10(prevProducts => [...prevProducts, ...response.data.proizvodi]);
          //setNovih10(response.data.proizvodi);
          setCurrentPage(prevPage => prevPage + 1);
          brojStranice++;
        } else {
          console.log('Server je vratio praznu listu proizvoda.');
          setShowButton(false);
          // Možete ovde dodati logiku ili obaveštenje ako želite da se uradi nešto specifično
        }
      } catch (error) {
        console.error('Došlo je do greške prilikom dohvatanja podataka:', error);
      }
  }

  return (
    <section className="sg-products">
      {/* ... */}
      <div className="product-grid">
      {[...proizvodi, ...novih10].map(([productId, product]) => (
      <Product key={productId} product={product} className="product-item" />
    ))}
  </div>
  {showButton && ( // Provera da li treba prikazati dugme na osnovu vrednosti flag-a
      <div className="dugmeVidiJos btn-primary">
        <button onClick={ucitajNova10}>Vidi Još</button>
      </div>
    )}
    </section>

    
  );
}

export default Home;
