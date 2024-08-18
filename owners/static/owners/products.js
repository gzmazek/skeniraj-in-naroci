document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event fired."); // Debugging line

  const menuContainer = document.getElementById("menuContainer");
  const addItem = document.getElementById('addItem');
  const addItemBtn = document.getElementById('add_item_btn');
  const removeItems = document.getElementById('removeItems');
  const popup = document.getElementById('popup');
  const closePopup = document.getElementById('closePopup');
  const restaurantId = menuContainer.getAttribute("data-restaurant-id");

  let isRemoveMode = false;

  console.log("Dashboard JS loaded."); // Debugging line

  updateTable();

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
  removeItems.addEventListener("click", toggleRemoveMode);
  addItemBtn.addEventListener('click', addItemToRestaurantMenu);

  // Functions
  function formatDate(rawDate) {
    const date = new Date(rawDate * 1000);
    return `${date.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}, ${date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`;
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

  function showPopup(event) {
    console.log("showPopup function called."); // Debugging line
    popup.style.display = 'block';
  }

  function toggleRemoveMode(){
    isRemoveMode = !isRemoveMode;
    updateTable();
  }
  function updateTable() {
    // Generate the table with or without the additional column
    menuContainer.innerHTML = `
        <table class="table table-striped mb-0 table-custom">
            <thead>
                <tr>
                    <th style="width: 75%;">Name</th>
                    <th>Price</th>
                    ${isRemoveMode ? '<th>Action</th>' : ''}
                </tr>
            </thead>
            <tbody>
                ${menu.map((item, menuIndex) => `
                <tr>
                    <td>${item.name}</td>
                    <td>${item.value} €</td>
                    ${isRemoveMode ? `<td><input type="checkbox" id="remove-${menuIndex}" name="options" data-index="${item.id}"></td>` : ''}
                </tr>
                `).join('')}
            </tbody>
        </table>
        ${isRemoveMode ? `
            <div class="d-flex justify-content-end mt-2 mb-2">
            <button id="removeButton" class="btn btn-primary">Remove selected items</button>
            </div>
            ` : ''}
    `;

    // Attach the event listener to the remove button if in remove mode
    if (isRemoveMode) {
        document.getElementById('removeButton').addEventListener('click', removeSelectedItems);
    }
}

function removeSelectedItems() {
    // Get all checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="remove-"]');
    
    const indicesToRemove = [];
    // Iterate over checkboxes and remove selected items
    for (let i = checkboxes.length - 1; i >= 0; i--) {
        if (checkboxes[i].checked) {
            const index = parseInt(checkboxes[i].getAttribute('data-index'));
            indicesToRemove.push(index);
        }
    }
    console.log(indicesToRemove);
    fetch(`/restaurant/${restaurantId}/removeMenuItems/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(indicesToRemove),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            console.log("Items removed!"); // Debugging line
            location.reload();
        } else {
            console.error("Error removing menu items");
        }
    });
    //location.reload();
}

function addItemToRestaurantMenu(){
    // Get the value of the name input field
    const name = document.getElementById('name').value;

    // Get the value of the price input field
    const value = document.getElementById('value').value;
    const price = parseFloat(value);

    let context = {
        'name': name,
        'value': price,
    };

    fetch(`/restaurant/${restaurantId}/addMenuItem/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(context),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data.success)
        if (data.success) {
            console.log("Item added!"); // Debugging line
            location.reload();
        } else {
            console.error("Error adding item");
        }
    });
}
});
