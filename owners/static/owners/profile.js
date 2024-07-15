document.addEventListener('DOMContentLoaded', () => {
    const addRestaurantBtn = document.getElementById('addRestaurantBtn');
    const popupForm = document.getElementById('popupForm');
    const closeBtn = document.querySelector('.close');

    addRestaurantBtn.addEventListener('click', () => {
        popupForm.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        popupForm.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === popupForm) {
            popupForm.style.display = 'none';
        }
    });
});