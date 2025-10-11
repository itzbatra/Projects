function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
  }
  
  const products = [
    { name: "HYPERX Cloud III Wireless Gaming Headset", price: 209.99, img: "HyperXHeadphones.jpg", category: "Peripherals" },
  { name: "STEELSERIES Apex 7 Mechanical Gaming Keyboard", price: 199.99, img: "keyboard1.jpg", category: "Peripherals" },
  { name: "RAZER Basilisk V3 X HyperSpeed Customizable Wireless Gaming Mouse", price: 99.99, img: "mouse1.jpg", category: "Peripherals" },
  { name: "GARMIN Venu 2S GPS Smartwatch", price: 519.99, img: "smartwatch.jpg", category: "Wearables" },
  { name: "HTC VIVE Focus Vision VR Headset", price: 1849.00, img: "vrheadset.jpg", category: "Gaming" },
  { name: "JBL Go 4 Portable Waterproof Bluetooth Speaker", price: 69.99, img: "speaker1.jpg", category: "Audio" },
  { name: "iCAN Gaming Laptop Cooler", price: 32.99, img: "laptopcooler.jpg", category: "Accessories" },
  { name: "Anker 4-Port USB-C Hub", price: 29.99, img: "usbchub.jpg", category: "Accessories" },
  { name: "Seagate Portable Drive 2TB External Hard Drive", price: 119.99, img: "hdd1.jpg", category: "Storage" },
  { name: "BLUE Yeti USB Microphone", price: 179.99, img: "mic1.jpg", category: "Audio" },
  { name: "ASUS ROG Strix G17 Gaming Laptop 17.3", price: 2299.00, img: "ROGG17.jpg", category: "Laptops" },
  { name: "ASUS TUF Gaming GeForce RTX 5070 Ti 16GB GDDR7 OC Edition", price: 1449.00, img: "ASUS5070Ti.jpg", category: "Graphics Cards" },
  { name: "ASUS ROG Cetra True Wireless Gaming Bluetooth Earbuds", price: 149.99, img: "headphones1.jpg", category: "Audio" },
  { name: "27in TUF 4K UHD Gaming Monitor", price: 530.90, img: "monitor1.jpg", category: "Peripherals" },
  { name: "RAZER Viper V2 Pro Wireless Gaming Mouse", price: 219.99, img: "mouse2.jpg", category: "Peripherals" },
  { name: "65in Skyworth 4K UHD Google TV", price: 699.99, img: "tv1.jpg", category: "Home Entertainment" },
  { name: "iCAN 5000mAh 20W Magnetic Power Bank", price: 39.99, img: "powerbank1.jpg", category: "Accessories" },
  { name: "iPhone 13 Pro", price: 1005.99, img: "iphone13.jpg", category: "Phones" },
  { name: "Samsung Galaxy A16", price: 269.99, img: "samsung1.jpg", category: "Phones" },
  { name: "Google Nest Thermostat", price: 179.99, img: "thermostat.jpg", category: "Home Automation" },
  { name: "DJI Mini 3 Pro Drone and Remote Control", price: 999.00, img: "drone1.jpg", category: "Photography" },
  { name: "Intel i9-11900K", price: 599.99, img: "intel9.jpg", category: "Processors" },
  { name: "AMD Ryzen 9 5900X", price: 749.99, img: "AMD9.jpg", category: "Processors" },
  { name: "Intel Core i7-10700K", price: 359.99, img: "intel7.jpg", category: "Processors" },
  { name: "AMD Ryzen 7 5800X", price: 499.99, img: "AMD7.jpg", category: "Processors" }

];
  
  let cart = JSON.parse(localStorage.getItem('cart')) || [];
  
  window.onload = () => {
    displayProducts(products);
    displayCart();
  };
  
  function displayProducts(productList) {
    const container = document.getElementById('product-container');
    container.innerHTML = "";
    productList.forEach(p => {
      const div = document.createElement('div');
      div.classList.add('product');
      div.innerHTML = `
        <img src="${p.img}" alt="${p.name}" />
        <h3>${p.name}</h3>
        <p>$${p.price.toFixed(2)}</p>
        <button onclick="addToCart('${p.name}', ${p.price})">Add to Cart</button>
      `;
      container.appendChild(div);
    });
  }
  
  function addToCart(name, price) {
    cart.push({ name, price });
    localStorage.setItem('cart', JSON.stringify(cart));
    alert(`${name} added to cart.`);
    displayCart();
  }
  
  function displayCart() {
    const cartItems = document.getElementById('cart-items');
    if (!cartItems) return;
    cartItems.innerHTML = "";
    if (cart.length === 0) {
      cartItems.innerHTML = "<p>Your cart is empty.</p>";
      return;
    }
    cart.forEach(item => {
      const div = document.createElement('div');
      div.textContent = `${item.name} - $${item.price.toFixed(2)}`;
      cartItems.appendChild(div);
    });
  }
  
  function submitOrder() {
    if (cart.length === 0) {
      alert("Your cart is empty.");
      return;
    }
    alert("Order submitted!");
    cart = [];
    localStorage.removeItem('cart');
    displayCart();
  }
  
  function filterProducts(category) {
    const productContainer = document.getElementById("product-container");
    productContainer.innerHTML = '';
  
    const filteredProducts = products.filter(product => product.category === category || category === 'All');
    if (filteredProducts.length === 0) {
      productContainer.innerHTML = "<p>No products found in this category.</p>";
    } else {
      filteredProducts.forEach(product => {
        const productElement = document.createElement("div");
        productElement.classList.add("product");
        productElement.innerHTML = `
          <img src="${product.img}" alt="${product.name}" />
          <h3>${product.name}</h3>
          <p>$${product.price.toFixed(2)}</p>
          <button onclick="addToCart('${product.name}', ${product.price})">Add to Cart</button>
        `;
        productContainer.appendChild(productElement);
      });
    }
  
    // Optionally scroll to the product section
    window.scrollTo({
      top: productContainer.offsetTop,
      behavior: 'smooth',
    });
  }
  