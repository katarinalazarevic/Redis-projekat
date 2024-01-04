import React from 'react';
import './product.css';


const Product = ({ product , addToCart }) => {

 

 
  return (
    <div className="product">
     

      <div class='title'>
      {product.producerName}
      </div>
      <div>
        <img src={product.picture}></img>
      </div>
      <p> {product.category}</p>
      <div class="product-info">
       {product.novacena && (  <p>Akcijska cena:{product.novacena} </p>)}
       
      {/* <p> {product.quantity}</p>
      <p> {product.discount}</p> */}
      </div>
      <div class="cta">

            <div class="price"> {product.novacena  && (<p>Stara cena: </p> )} { product.price} rsd  </div>
            {/* <button class="btn" onClick={addToCard}>Add to cart<span class="bg"></span></button> */}
            <button className="btn" onClick={() => addToCart(product.id)}>Add to cart</button>
        </div>

    </div>
  );
};

export default Product;
