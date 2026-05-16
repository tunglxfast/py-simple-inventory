function addStockLine() {
  const template = document.querySelector("#stock-line-template");
  const target = document.querySelector("#stock-lines");
  const addRow = document.querySelector("#add-stock-line-row");
  if (!template || !target) return;
  target.insertBefore(template.content.cloneNode(true), addRow || null);
}

function removeStockLine(button) {
  const row = button.closest("tr");
  if (row) row.remove();
}

document.addEventListener("submit", (event) => {
  const message = event.target.dataset.confirm;
  if (message && !window.confirm(message)) {
    event.preventDefault();
  }
});

function selectProductRow(row) {
  if (!row) return;
  document.querySelectorAll(".product-row").forEach((productRow) => {
    productRow.classList.toggle("table-primary", productRow === row);
  });

  const deleteForm = document.querySelector("#delete-selected-product");
  if (deleteForm) {
    deleteForm.action = row.dataset.deleteUrl;
    deleteForm.dataset.confirm = row.dataset.confirm;
  }

  const editForm = document.querySelector("#edit-product-form");
  if (editForm) {
    editForm.action = row.dataset.updateUrl;
    document.querySelector("#edit-product-code").value = row.dataset.code || "";
    document.querySelector("#edit-product-name").value = row.dataset.name || "";
    document.querySelector("#edit-product-unit").value = row.dataset.unit || "";
    document.querySelector("#edit-product-note").value = row.dataset.note || "";
    document.querySelector("#edit-product-active").checked = row.dataset.isActive === "true";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const editButton = document.querySelector("#edit-selected-product");
  const editModal = document.querySelector("#edit-product-modal");
  if (editButton && editModal) {
    editButton.addEventListener("click", () => {
      selectProductRow(document.querySelector(".product-row.table-primary"));
      bootstrap.Modal.getOrCreateInstance(editModal).show();
    });
  }

  document.querySelectorAll(".product-row").forEach((row) => {
    row.addEventListener("click", () => selectProductRow(row));
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectProductRow(row);
      }
    });
  });
});
