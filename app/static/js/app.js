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
