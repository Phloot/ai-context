export function renderTypeFilters(container, types, selectedTypes, onToggle) {
  container.replaceChildren();
  types.forEach((type) => {
    const label = `${type.charAt(0).toUpperCase()}${type.slice(1)}s`;
    container.append(createFilter(type, label, selectedTypes.has(type), onToggle));
  });
}

function createFilter(type, label, selected, onToggle) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = `btn btn-sm ${selected ? "btn-primary" : "btn-outline-primary"}`;
  button.dataset.componentType = type;
  button.setAttribute("aria-pressed", String(selected));
  button.textContent = label;
  button.addEventListener("click", () => onToggle(type));
  return button;
}
