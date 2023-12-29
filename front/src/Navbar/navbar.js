import "./navbar.css";

const NavBar = () => {
  return (
    <div id="app">
      <nav id="navigation-bar">
        <button class="controller" title="open navigation bar">
          <span class="material-symbols-outlined">menu</span>
        </button>
        <ul class="items-container">
          <li class="item" title="home">
            <a href="#home" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">home</span>
              </div>
              <span class="item-text">Home</span>
            </a>
          </li>
          <li class="item" title="book">
            <a href="#books" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">book</span>
              </div>
              <span class="item-text">Books</span>
            </a>
          </li>
          <li class="item">
            <a href="#saved" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">save</span>
              </div>
              <span class="item-text">Saved</span>
            </a>
          </li>
          <li class="item" title="shopping cart">
            <a href="#cart" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">shopping_cart</span>
              </div>
              <span class="item-text">Cart</span>
            </a>
          </li>
          <li class="item" title="profile">
            <a href="#profile" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">person</span>
              </div>
              <span class="item-text">Profile</span>
            </a>
          </li>
          <li class="item" title="settings">
            <a href="#setting" class="hyper-link">
              <div class="icon-wrapper">
                <span class="material-symbols-outlined">Settings</span>
              </div>
              <span class="item-text">Settings</span>
            </a>
          </li>
        </ul>
      </nav>
      <main id="main">
        <div class="container"></div>
      </main>
    </div>
  );
};

export default NavBar;
