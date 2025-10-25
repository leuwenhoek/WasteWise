let cart = [];
const cartItemsContainer = document.getElementById('cart-items');
const totalPriceSpan = document.getElementById('total-price');
const checkoutBtn = document.getElementById('checkout-btn');
const checkoutFormContainer = document.getElementById('checkout-form-container');
const checkoutForm = document.getElementById('checkout-form');

/**
 * Updates the visual representation of the cart and the total price.
 */
function renderCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<li class="empty-cart-message" style="color:#777; text-align:center; font-style:italic;">Your cart is empty.</li>';
        totalPriceSpan.textContent = '$0.00';
        checkoutBtn.disabled = true;
        toggleCheckout(false); // Hide the form if the cart is cleared
        return;
    }

    cart.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>${item.name} (x${item.quantity})</span>
            <span>$${(item.price * item.quantity).toFixed(2)}</span>
        `;
        cartItemsContainer.appendChild(li);
        total += item.price * item.quantity;
    });

    totalPriceSpan.textContent = `$${total.toFixed(2)}`;
    checkoutBtn.disabled = false;
}

/**
 * Adds a product to the cart or increments its quantity if it already exists.
 * @param {string} name - The product name.
 * @param {number} price - The product price.
 */
function addToCart(name, price) {
    const existingItem = cart.find(item => item.name === name);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ name, price, quantity: 1 });
    }

    renderCart();
    // Optional: provide visual feedback
    alert(`${name} added to cart! Current items: ${cart.length}`);
}

/**
 * Toggles the visibility of the checkout form.
 * @param {boolean} show - True to show the form, False to hide it.
 */
function toggleCheckout(show) {
    if (show && cart.length > 0) {
        checkoutFormContainer.style.display = 'block';
        checkoutBtn.style.display = 'none';
    } else {
        checkoutFormContainer.style.display = 'none';
        checkoutBtn.style.display = 'block';
    }
}

// Handle checkout form submission
checkoutForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Stop the default form submission

    // Get input values
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const mobile = document.getElementById('mobile').value;

    let orderSummary = "Order Details:\n";
    cart.forEach(item => {
        orderSummary += `- ${item.name} x${item.quantity} ($${(item.price * item.quantity).toFixed(2)})\n`;
    });
    
    const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    orderSummary += `\nFinal Total: $${total.toFixed(2)}\n`;

    // Confirmation Message (as there is no backend for processing)
    const confirmationMessage = `
        ✅ Order Placed Successfully! ✅
        
        Thank you, ${name}!
        We have received your order.
        
        Shipping Address: ${address}
        Contact No.: ${mobile}

        ${orderSummary}
        
        Your cart has been cleared.
    `;

    alert(confirmationMessage);
    
    // Clear the cart and reset the form/view
    cart = [];
    renderCart();
    checkoutForm.reset();
    toggleCheckout(false);
});

// Initial render when the page loads
document.addEventListener('DOMContentLoaded', renderCart);