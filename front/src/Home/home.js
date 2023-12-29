import React, { useEffect, useState } from "react";
import './home.css';
import axios from 'axios';
import Product from "../Product/product";


const Home = ( {data}) => {
  const [proizvodi, setProizvodi] = useState([]);
  const [novih10,setNovih10]= useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showButton, setShowButton] = useState(true); // Postavite početno stanje flag-a na true ili false u zavisnosti od potrebe
  const [brojStranice,setBrojStranice]=useState(1);

  let productsForCard=[];

  //let brojStranice=1;

  useEffect(() => {
    const fetchProizvodi = async () => {
      try {
        const response = await axios.get('http://localhost:5000/prvih_deset_proizvoda');
        setProizvodi(response.data.proizvodi);
      } catch (error) {
        console.error('Došlo je do greške prilikom dohvatanja podataka:', error);
      }
    };
    console.log(data)
    fetchProizvodi();
  }, []);

  useEffect(() => {
    // Ovde možete pozvati funkciju ili izvršiti određenu logiku nakon što se komponenta učita
    console.log('Ucita li smo novih 10 proizvoda.');
    //console.log(novih10);
    console.log(brojStranice);
  }, [novih10]);

  useEffect(() => {
    // Ovde možete pozvati funkciju ili izvršiti određenu logiku nakon što se komponenta učita
    console.log('Komponenta se upravo učitala.');
    //console.log(proizvodi);
  }, [proizvodi]);


  const ucitajNova10= async ()=>
  {
    //brojStranice++;
    console.log(`ulazimo u ucitajNova10 i poziva fja za vrednost: ${brojStranice}`)
    try {
        const response = await axios.post('http://localhost:5000/ucitaj_narednih_10',
        {
          stranica:brojStranice + 1
        });
        if (response.data.proizvodi.length > 0) {
          setNovih10(prevProducts => [...prevProducts, ...response.data.proizvodi]);
          //setNovih10(response.data.proizvodi);
          setBrojStranice(prevBrojStranice => prevBrojStranice + 1);
          setCurrentPage(prevPage => prevPage + 1);
          //brojStranice++;
        } else {
          console.log('Server je vratio praznu listu proizvoda.');
          setShowButton(false);
          // Možete ovde dodati logiku ili obaveštenje ako želite da se uradi nešto specifično
        }
      } catch (error) {
        console.error('Došlo je do greške prilikom dohvatanja podataka:', error);
      }
  }
  const addToCart = (productId) => {
   
    console.log('Dodat proizvod u korpu sa ID-om:', productId); 
    productsForCard.push(productId);
    console.log(productsForCard);
    //ovde ce da se zove metoda sa backa 
    // Implementirajte logiku za dodavanje proizvoda u korpu
  };

  const mergedProducts = [...proizvodi, ...novih10];

// Filtriranje proizvoda na osnovu jedinstvenog identifikatora
const uniqueProducts = mergedProducts.reduce((acc, [productId, product]) => {
  const existingProductIds = acc.map(([id, _]) => id);
  if (!existingProductIds.includes(productId)) {
    return [...acc, [productId, product]];
  }
  return acc;
}, []);


  return (
    
    <div class="akcijskiProizvodi">
      <h1>Akcijski proizvodi</h1>
  <section className="sg-products">
    {/* ... */}
    <div className="product-grid">
      {[...proizvodi, ...novih10].map(([productId, product]) => (
        <Product key={productId} product={product} addToCart={addToCart} />
      ))}
    </div>
    {showButton && ( // Provera da li treba prikazati dugme na osnovu vrednosti flag-a
      <div className="dugmeVidiJos btn-primary">
        <button onClick={ucitajNova10}>Vidi Još</button>
      </div>
    )}
  </section>
</div>



    
  );
}

export default Home;
