import { useEffect, useReducer, useState } from "react";
import axios from "axios";
import Product from "../Product/product";
import ProizvodUKorpi from "../ProizvodUKorpi/proizvodUKorpi";

const ShoppingCart = ({ usernameKorisnika,ocistiKorpu ,productsForCard}) => {
  const [proizvodi, setProizvodi] = useState([]);
 

  useEffect( ()=>
  {
    console.log('Promena u proizvodima za korpu:', productsForCard);
  },[productsForCard]);

  useEffect(() => {
   // Poziv metode za prikaz proizvoda u korpi
const prikaziProizvodeUKorpi = async (emailKorisnika) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/prikaziProizvodeUKorpi', {
      
        korisnik_email: emailKorisnika
      
    });

    // Ovdje možete manipulisati odgovorom (response) kako je potrebno
    console.log(response.data);
    setProizvodi(response.data);

    // Obrada podataka
  } catch (error) {
    // Uhvatite grešku ako se desi
    console.error("Greška prilikom dohvatanja proizvoda:", error);
  }
};

// Poziv funkcije sa odgovarajućim emailom korisnika
prikaziProizvodeUKorpi(usernameKorisnika); // Ovdje umjesto 'kaca@gmail.com' možete proslijediti stvarni email korisnika


  }, [usernameKorisnika]);

  const KupiProizvodeHandler=  async ()=>
  {

    try {
      const response = await axios.post('http://127.0.0.1:5000/kupi_proizvode', {
        
          korisnik_email: usernameKorisnika
        
      });
  
     
      console.log(response.data);
      ocistiKorpu();
      
  
      // Obrada podataka
    } catch (error) {
      // Uhvatite grešku ako se desi
      console.error("Greška prilikom dohvatanja proizvoda:", error);
    }
  };
  
  const obrisiProizvod=(index)=>
  {

  }

  return (
    <div className="shopping-cart">
      <h1>Shopping Cart</h1>
      
      <div>
      {
  proizvodi.map((product, index) => (
    <div key={index}>
      <ProizvodUKorpi product={product}  usernameKorisnika={usernameKorisnika}/>
      
    </div>
  ))
}

        
      </div>
      <button onClick={KupiProizvodeHandler}> Kupi proizvode </button>
    </div>
  );
};

export default ShoppingCart;
