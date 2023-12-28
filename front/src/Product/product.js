import React from 'react';
import './product.css';

const Product = ({ product }) => {
  return (
    <div className="product">
     

      <div class='title'>
      {product.producerName}
      </div>
      <div>
        <img src={product.picture}></img>
      </div>
      <p>Category: {product.category}</p>
      <div class="product-info">
      <p>Quantity: {product.quantity}</p>
      <p>Discount: {product.discount}</p>
      </div>
      <div class="cta">
            <div class="price">{product.price} rsd  </div>
            <button class="btn">Add to cart<span class="bg"></span></button>
        </div>

    </div>

    
  );
};

export default Product;
