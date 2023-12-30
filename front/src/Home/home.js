import React, { useEffect, useState,useContext} from "react";
import './home.css';
import axios from 'axios';
import Product from "../Product/product";
import ShoppingCart from "../Cart/cart";

 // Prilagodite putanju do vašeg UserContext fajla
import { useAuth } from '../UserContext/UserContext';




const Home = ( {data}) => {
  const { username } = useAuth();  // prima podatke iz login

  const [proizvodi, setProizvodi] = useState([]);
  const [novih10,setNovih10]= useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showButton, setShowButton] = useState(true); // Postavite početno stanje flag-a na true ili false u zavisnosti od potrebe
  const [brojStranice,setBrojStranice]=useState(2);
  const [prikaziKorpu,setPrikaziKorpu]=useState(false);

  const [productsForCard, setProductsForCard] = useState([]);

  //let brojStranice=1;
  console.log('Email korisnika:', username);
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
    console.log('Ucitali smo novih 10 proizvoda.');
    //console.log(novih10);
    console.log(brojStranice);
  }, [novih10]);

  useEffect(() => {
    // Ovde možete pozvati funkciju ili izvršiti određenu logiku nakon što se komponenta učita
    console.log('Komponenta se upravo učitala.');
    //console.log(proizvodi);
  }, [proizvodi]);

  const KorpaHandler= ()=>
  {
    setPrikaziKorpu(!prikaziKorpu);
  }

  const ucitajNova10 = async () => {
   
    console.log(`ulazimo u ucitajNova10 i poziva fja za vrednost: ${brojStranice}`);
    try {
      const response = await axios.post('http://localhost:5000/ucitaj_narednih_10', {
        stranica: 3 // Koristi trenutnu vrednost brojStranice kao argument
      }, {
        headers: {
          'Content-Type': 'application/json',
          // Dodajte dodatne zaglavlja ovde ako su potrebna
        }
      });
      if (response.data.proizvodi.length > 0) {
        setNovih10(prevProducts => [...prevProducts, ...response.data.proizvodi]);
        setBrojStranice(prevBrojStranice => prevBrojStranice + 1);
        setCurrentPage(prevPage => prevPage + 1);
      } else {
        console.log('Server je vratio praznu listu proizvoda.');
        setShowButton(false);
      }
    } catch (error) {
      console.error('Došlo je do greške prilikom dohvatanja podataka:', error);
    }
  };
  


  const addToCart = (productId) => {
   
    if (productsForCard.includes(productId)) {
      console.log('Proizvod je već u korpi!');
      // Ovde možete prikazati poruku korisniku da je proizvod već dodat u korpu
      return; // Prekida se izvršavanje funkcije jer proizvod već postoji u korpi
    }
    
    const updatedProducts = [...productsForCard, productId];
    setProductsForCard(updatedProducts);
    console.log('Niz proizvoda za korpu:', updatedProducts);
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
    <button onClick={KorpaHandler}> Prikazi Korpu</button>
    {showButton && ( // Provera da li treba prikazati dugme na osnovu vrednosti flag-a
      <div className="dugmeVidiJos btn-primary">
        <button onClick={ucitajNova10}>Vidi Još</button>
      </div>
    )}
     {prikaziKorpu && <ShoppingCart indeksi={productsForCard} />}

  </section>
</div>



    
  );
}

export default Home;
