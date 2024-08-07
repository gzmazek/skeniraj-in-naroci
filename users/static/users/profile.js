document.addEventListener('DOMContentLoaded', () => {
    const mainContent = document.getElementById('content');

    function formatDate(rawDate) {
        const date = new Date(rawDate * 1000);
        return `${date.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}, ${date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`;
    }
    let content = `
        <h3 class="my-4">Popular restaurants</h1>
        <div class="row">
        ${popularRestaurants.slice(0,8).map((rest, restaurantIndex) => `
            <div class="col-xl-3 col-lg-4 col-md-6 col-sm-12 py-2 px-2">
            <div class="border rounded-3 p-3 h-100 popularRestaurant" data-value="${restaurantIndex}">
                <h5>${rest.name}</h4>
                <p class="mb-0">Address: ${rest.location}</p>
            </div>
            </div>
        `).join('')}
        </div>

        <h3 class="my-4">Recent Orders</h1>
        <div class="row">
        ${orders.slice(0,8).map((order, orderIndex) => `
            <div class="col-xl-3 col-lg-4 col-md-6 col-sm-12 py-2 px-2">
            <div class="border rounded-3 p-3 h-100 orderTicket" data-value="${orderIndex}">
                <h5>Order from ${order.restaurant}</h4>
                <div class="row">
                    <div class="col-6">
                        <p><strong>Product</strong></p>
                    </div>
                    <div class="col-3">
                        <p><strong>Quantity</strong></p>
                    </div>
                    <div class="col-3">
                        <p><strong>Price</strong></p>
                    </div>
                </div>
                ${order.items.length > 3 ? `
                    <div class="gradient-text">
                    ${order.items.slice(0, 3).map((item, itemIndex) => `
                        <div class="row">
                            <div class="col-6">
                                <p>${item}</p>
                            </div>
                            <div class="col-3">
                                <p>${order.item_quantities[itemIndex]}</p>
                            </div>
                            <div class="col-3">
                                <p>${order.item_values[itemIndex]}</p>
                            </div>
                        </div>
                    `).join('')}
                    </div>
                ` : `
                    <div>
                    ${order.items.map((item, itemIndex) => `
                        <div class="row">
                            <div class="col-6">
                                <p>${item}</p>
                            </div>
                            <div class="col-3">
                                <p>${order.item_quantities[itemIndex]}</p>
                            </div>
                            <div class="col-3">
                                <p>${order.item_values[itemIndex]}</p>
                            </div>
                        </div>
                    `).join('')}
                    </div>
                `}
                <p><strong>Total price:</strong> ${order.total_value}</p>
                <p><strong>Date:</strong> ${formatDate(order.date)}</p>
            </div>
            </div>
        `).join('')}
        </div>
    `;

    mainContent.innerHTML = content;

    const addRestaurantBtns = document.querySelectorAll('.orderTicket');
    const popupTicket = document.getElementById('popupTicket');
    const popupContent = document.getElementById('popupContent');
    const closeBtn = document.querySelector('.close');

    addRestaurantBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const value = btn.getAttribute('data-value');

            const orderData = orders[value];
            
            popupContent.innerHTML = `
            <div class="order-card p-3 h-100" >
            <p><strong>Restaurant: ${orderData['restaurant']}</strong></p>
            <div class="row">
                <div class="col-6">
                <p><strong>Product</strong></p>
                </div>
                <div class="col-3">
                <p><strong>Quantity</strong></p>
                </div>
                <div class="col-3">
                <p><strong>Price</strong></p>
                </div>
            </div>
            <div>
                ${orderData['items'].map((item, index) => `
                <div class="row">
                    <div class="col-6">
                        <p>${item}</p>
                    </div>
                    <div class="col-3">
                        <p>${orderData['item_quantities'][index]}</p>
                    </div>
                    <div class="col-3">
                        <p>${orderData['item_values'][index]}</p>
                    </div>
                </div>
                `).join('')}
            </div>
            <p><strong>Total price:</strong> ${orderData['total_value']}</p>
            <p><strong>Date:</strong> ${formatDate(orderData['date'])}</p>
            </div>
            `;

            popupTicket.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', () => {
        popupTicket.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === popupTicket) {
            popupTicket.style.display = 'none';
        }
    });
});