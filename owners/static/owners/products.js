document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event fired."); // Debugging line

  const menuContainer = document.getElementById("menuContainer");
  const addItem = document.getElementById('addItem');
  const popup = document.getElementById('popup');
  const closePopup = document.getElementById('closePopup');
  const restaurantId = menuContainer.getAttribute("data-restaurant-id");

  console.log("Dashboard JS loaded."); // Debugging line

  menuContainer.innerHTML = `
  <table class="table table-striped mb-0">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                ${menu.map((item, menuIndex) => `
                <tr>
                    <td>${item.name}</td>
                    <td>${item.value} €</td>
                </tr>
                `).join('')}
            </tbody>
        </table>
  `

  addItem.addEventListener("click", showPopup);
  closePopup.addEventListener("click", () => {
      console.log("Close popup clicked."); // Debugging line
      popup.style.display = 'none';
  });
  window.addEventListener("click", (event) => {
      if (event.target == popup) {
          console.log("Outside popup clicked."); // Debugging line
          popup.style.display = 'none';
      }
  });

  // Functions
  function formatDate(rawDate) {
    const date = new Date(rawDate * 1000);
    return `${date.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}, ${date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`;
  }

  function showPopup(event) {
    console.log("showPopup function called."); // Debugging line
    popup.style.display = 'block';
}
});
