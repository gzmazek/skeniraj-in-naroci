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

  // Functions
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
          popupContent.innerHTML = `<p>Details for Table ID: ${tableId}</p>`;
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

  document.querySelectorAll(".mark-order-finished").forEach((button) => {
      button.addEventListener("click", function () {
          const orderId = this.getAttribute("data-order-id");
          fetch(`/mark_order_finished/${orderId}/`, {
              method: "POST",
              headers: {
                  "X-CSRFToken": getCookie("csrftoken"),
              },
          })
          .then((response) => response.json())
          .then((data) => {
              if (data.status === "success") {
                  console.log(`Order marked as finished: ${orderId}`); // Debugging line
                  location.reload();  // Reload the page to update the order status
              } else {
                  console.error("Error marking order as finished");
              }
          });
      });
  });
});
