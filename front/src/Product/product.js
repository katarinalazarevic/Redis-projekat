import React from "react";
import "./product.css";
import  slikaajax  from '../Slike/ajax.jpg'  



const Product = ({ product, addToCart }) => {
  return (
    <div className="product">
      <div class="title">{product.producerName}</div>
      <div>
     
      <img src={'../../Slike/' + product.picture}
       style={{ width: '200px', height: '200px'}}  />
 <p> {product.productDescription}</p>
      
      

      </div>
      <p> {product.category}</p>
      <div class="product-info">
        {product.novacena && <p>Akcijska cena:{product.novacena} </p>}

        {/* <p> {product.quantity}</p>
      <p> {product.discount}</p> */}
      </div>
      <div class="cta">
        <div className="price">
          {product.novacena ? (
            <>
              <p>Stara cena: {product.price} rsd</p>
              
            </>
          ) : (
            <p>Cena: {product.price} rsd</p>
          )}
        </div>

        {/* <button class="btn" onClick={addToCard}>Add to cart<span class="bg"></span></button> */}
        <button className="btn" onClick={() => addToCart(product.id)}>
          Add to cart
        </button>
      </div>
    </div>
  );
};

export default Product;
