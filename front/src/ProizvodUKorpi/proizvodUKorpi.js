import React, { useEffect } from "react";
import "../Product/product.css";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

const ProizvodUKorpi = ({ product, addToCart, usernameKorisnika }) => {


  useEffect( ()=>
  {
    console.log(product);
  },[])
  const ObrisiProizvod = async (productId) => {
    console.log(productId);
    const id = productId + "";
    console.log(usernameKorisnika);

    try {
      const response = await axios.delete(
        "http://127.0.0.1:5000/obrisiProizvodIzKorpe",
        {
          headers: {
            "Content-Type": "application/json",
          },
          data: {
            korisnik_email: usernameKorisnika,
            proizvod_id: id,
          },
        }
      );

      console.log(response);

      if (response.status === 200) {
        console.log("Proizvod uspešno obrisan iz korpe");
        // Dodatna logika nakon uspešnog brisanja iz korpe
      } else {
        console.log("Greška prilikom brisanja proizvoda iz korpe");
        window.confirm("Greška prilikom brisanja proizvoda iz korpe");
      }
    } catch (error) {
      console.error(
        "Došlo je do greške prilikom brisanja proizvoda iz korpe:",
        error
      );
      window.confirm("Greška prilikom brisanja proizvoda iz korpe");
    }
  };

  return (
    <div className="product">
      <div class="title">{product.producerName}</div>
      <div>
        <img src={product.picture}></img>
      </div>
      
      <p> {product.picture}</p>
      <div class="product-info">
         <p> {product.quantity}</p>
     
      </div>
      <div class="cta">
        <div class="price" >{product.price}  rsd </div>
        
        <IconButton aria-label="delete" onClick={() => ObrisiProizvod(product.id)} > 
        <DeleteIcon />
      </IconButton>
      </div>
    </div>
  );
};

export default ProizvodUKorpi;
