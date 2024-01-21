import React, { useEffect } from "react";
import "../Product/product.css";
import axios from "axios";
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

const ProizvodUKorpi = ({ product, addToCart, usernameKorisnika,ObrisiProizvod }) => {


  useEffect( ()=>
  {
    console.log(product);
  },[])
 

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
