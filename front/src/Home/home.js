import React, { useEffect, useState } from "react";
import './home.css';
import axios from 'axios';
import Product from "../Product/product";


const Home = () => {
  const [proizvodi, setProizvodi] = useState([]);
  const [novih10,setNovih10]= useState([]);
  const [currentPage, setCurrentPage] = useState(1);
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
          stranica: currentPage
        });
        console.log(brojStranice);
        setNovih10(prevProducts => [...prevProducts, ...response.data.proizvodi]);
        setCurrentPage(prevPage => prevPage + 1);
        brojStranice = brojStranice + 1;
        console.log(brojStranice)
       //  brojStranice=brojStranice+1;
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
  <div class="dugmeVidiJos btn-primary" > 
    <button onClick={ucitajNova10}> Vidi Jos </button>
  </div>
    </section>

    
  );
}

export default Home;
