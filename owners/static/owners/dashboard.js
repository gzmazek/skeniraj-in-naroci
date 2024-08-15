document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event fired."); // Debugging line

  const tableContainer = document.getElementById("tableContainer");
  const editModeToggle = document.getElementById("editModeToggle");
  const addTable = document.getElementById("addTable");
  const popup = document.getElementById('popup');
  const closePopup = document.getElementById('closePopup');
  const popupContent = document.getElementById('popupContent');
  const restaurantId = tableContainer.getAttribute("data-restaurant-id");

  let isEditMode = false;

  console.log("Dashboard JS loaded."); // Debugging line

  // Place the tables on dashboard and determine their properties
  tables.forEach(function(table_orders) {
    var table = table_orders.table
    var orders = table_orders.orders

    // Create the div element for the table item
    var tableItem = document.createElement("div");
    tableItem.classList.add("table-item");

    // Add classes based on the table's order status
    if (orders.length > 0) {
        if (orders[0].status === "PREPARED") {
            tableItem.classList.add("prepared");
        } else {
            tableItem.classList.add("not-prepared");
        }
    } else {
        tableItem.classList.add("no-order");
    }

    // Set the data-table-id attribute
    tableItem.setAttribute("data-table-id", table.id);

    // Set the position styles
    tableItem.style.left = table.position_x + "px";
    tableItem.style.top = table.position_y + "px";

    // Create the span element for the table ID
    var tableSpan = document.createElement("span");
    tableSpan.textContent = table.id;

    // Append the span to the table item div
    tableItem.appendChild(tableSpan);

    // Append the table item div to the container
    tableContainer.appendChild(tableItem);
});

  // Event Listeners
  editModeToggle.addEventListener("click", toggleEditMode);
  addTable.addEventListener("click", addNewTable);
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

  const tableItems = document.querySelectorAll(".table-item");
  console.log(`Found ${tableItems.length} table items.`); // Debugging line
  tableItems.forEach(item => {
      console.log(`Attaching click listener to table ${item.dataset.tableId}`); // Debugging line
      item.addEventListener('click', showPopup);
      makeDraggable(item);
  });

  attachDynamicEventListeners()

  // Functions
  function formatDate(rawDate) {
    const date = new Date(rawDate * 1000);
    return `${date.toLocaleString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}, ${date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`;
  }

  function toggleEditMode() {
      isEditMode = !isEditMode;
      console.log(`Edit mode: ${isEditMode}`); // Debugging line
      editModeToggle.textContent = isEditMode ? "Save" : "Move Tables";
      tableContainer.classList.toggle("edit-mode", isEditMode);

      if (!isEditMode) {
          // Save positions
          document.querySelectorAll(".table-item").forEach((table) => {
              const id = table.dataset.tableId;
              const position = {
                  x: table.style.left.replace("px", ""),
                  y: table.style.top.replace("px", ""),
              };
              saveTablePosition(id, position);
          });
      }
  }

  function makeDraggable(element) {
      let offsetX, offsetY;

      element.addEventListener("mousedown", function (e) {
          if (!isEditMode) return;

          offsetX = e.clientX - parseInt(element.style.left);
          offsetY = e.clientY - parseInt(element.style.top);

          function onMouseMove(e) {
              element.style.left = e.clientX - offsetX + "px";
              element.style.top = e.clientY - offsetY + "px";
          }

          document.addEventListener("mousemove", onMouseMove);

          element.addEventListener("mouseup", function () {
              document.removeEventListener("mousemove", onMouseMove);
          });

          element.addEventListener("mouseleave", function () {
              document.removeEventListener("mousemove", onMouseMove);
          });
      });
  }

  function showPopup(event) {
    console.log("showPopup function called."); // Debugging line
    if (!isEditMode) {
        const tableId = event.currentTarget.dataset.tableId;
        console.log(`Table clicked: ${tableId}`); // Debugging line

        // Find the table entry with the specific ID
        const tableEntry = tables.find(table_orders => table_orders.table.id === Number(tableId));
        if (!tableEntry) {
            console.log("No orders found for this table.");
            return;
        }

        const orders = tableEntry.orders;
        let orderDetailsHtml = `<p>Details for Table ID: ${tableId}</p>`;

        orders.forEach((order) => {
            orderDetailsHtml += `
                <div class="w-100 mt-3 mb-3 d-flex justify-content-between">
                    <div>Date: ${formatDate(order.date)}</div>
                    <div>Status: ${order.status}</div>
                </div>
                <ul id="order-items-list-${order.id}" class="order-items-list">`;

            // Fetch items for this order
            fetch(`get_items/${order.id}/`)
                .then(response => response.json())
                .then(data => {
                    console.log('Fetches items', data)
                    if (data.items) {
                        let itemsHtml = '';
                        data.items.forEach(item => {
                            itemsHtml += `
                                <li>
                                    ${item.quantity}x ${item.name} - ${item.status} - Quantity: 
                                    <button class="btn btn-sm btn-primary mark-item-prepared" data-item-id="${item.item_id}" data-table-id="${tableId}">Mark as Prepared</button>
                                </li>`;
                        });
                        document.getElementById(`order-items-list-${order.id}`).innerHTML = itemsHtml;
                        attachDynamicEventListeners();
                    }
                })
                .catch(error => console.error('Error fetching items:', error));

            orderDetailsHtml += `</ul>`;
        });

        // Add QR code and Delete table buttons
        orderDetailsHtml += `
            <button class="qr-code-table btn btn-primary" data-table-id="${tableId}">QR code</button>
            <button class="delete-table btn btn-secondary" data-table-id="${tableId}">Delete table</button>
        `;

        // Add buttons for marking orders as prepared and delivered
        orderDetailsHtml += `
            <button class="btn btn-success mark-order-prepared" data-table-id="${tableId}">Mark Order as Prepared</button>
            <button class="btn btn-secondary mark-order-delivered" data-table-id="${tableId}">Mark Order as Delivered</button>
        `;

        popupContent.innerHTML = orderDetailsHtml;
        popup.style.display = 'block';
    }
}



  function saveTablePosition(id, position) {
      fetch(`/restaurant/${restaurantId}/save_table_position/${id}/`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify(position),
      })
      .then((response) => response.json())
      .then((data) => {
          if (data.status === "success") {
              console.log("Position saved!"); // Debugging line
          } else {
              console.error("Error saving position");
          }
      });
  }

  function addNewTable() {
      fetch(`/restaurant/${restaurantId}/add_table/`, {
          method: "POST",
          headers: {
              "X-CSRFToken": getCookie("csrftoken"),
          },
      })
      .then((response) => response.json())
      .then((data) => {
          if (data.status === "success") {
              const newTable = document.createElement("div");
              newTable.id = `table-${data.table_id}`;
              newTable.className = "table-item no-order";
              newTable.style.left = "0px";
              newTable.style.top = "0px";
              newTable.dataset.tableId = data.table_id;
              newTable.textContent = data.table_id;
              tableContainer.appendChild(newTable);
              makeDraggable(newTable);
              newTable.addEventListener('click', showPopup);
              console.log(`New table added: ${data.table_id}`); // Debugging line
          } else {
              console.error("Error adding table");
          }
      });
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

  function attachDynamicEventListeners() {
    document.querySelectorAll(".delete-table").forEach((button) => {
        button.addEventListener("click", function () {
            const tableId = this.getAttribute("data-table-id");
            fetch(`/restaurant/${restaurantId}/delete_table/${tableId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    document.getElementById(`table-${tableId}`).remove();
                    console.log(`Table deleted: ${tableId}`); // Debugging line
                    location.reload(); // Reload the page so that changes appear
                } else {
                    console.error("Error deleting table");
                }
            });
        });
    });

    document.querySelectorAll(".qr-code-table").forEach((button) => {
        button.addEventListener("click", function () {
            const tableId = this.getAttribute("data-table-id");
            console.log(`Generating QR code for table: ${tableId}`); // Debugging line
            window.location.href = `/restaurant/generate_qr_code/${tableId}/`;
        });
    });

    document.querySelectorAll(".mark-item-prepared").forEach(button => {
        button.addEventListener("click", function () {
            const itemId = this.getAttribute("data-item-id");
            const tableId = this.getAttribute("data-table-id");
            fetch(`/mark_item_prepared/${itemId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Item marked as prepared: ${itemId}`); // Debugging line
                    showPopup({ currentTarget: document.querySelector(`[data-table-id="${tableId}"]`) });
                } else {
                    console.error("Error marking item as prepared");
                }
            });
        });
    });

    // Additional event listeners for mark-order-prepared and mark-order-delivered buttons
    document.querySelectorAll(".mark-order-prepared").forEach((button) => {
        button.addEventListener("click", function () {
            const tableId = this.getAttribute("data-table-id");
            fetch(`/mark_order_prepared/${tableId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    console.log(`Order marked as prepared for table: ${tableId}`); // Debugging line
                    showPopup({ currentTarget: document.querySelector(`[data-table-id="${tableId}"]`) });
                } else {
                    console.error("Error marking order as prepared");
                }
            });
        });
    });

    document.querySelectorAll(".mark-order-delivered").forEach((button) => {
        button.addEventListener("click", function () {
            const tableId = this.getAttribute("data-table-id");
            fetch(`/mark_order_delivered/${tableId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    console.log(`Order marked as delivered for table: ${tableId}`); // Debugging line
                    location.reload();  // Reload the page to update the order status
                } else {
                    console.error("Error marking order as delivered");
                }
            });
        });
    });
}


});
