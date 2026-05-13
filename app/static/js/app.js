function addStockLine() {
  const template = document.querySelector("#stock-line-template");
  const target = document.querySelector("#stock-lines");
  if (!template || !target) return;
  target.appendChild(template.content.cloneNode(true));
}

function removeStockLine(button) {
  const row = button.closest("tr");
  if (row) row.remove();
}
