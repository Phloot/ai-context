export function textElement(tag, text, className = "") {
  const element = document.createElement(tag);
  element.textContent = text;
  if (className) element.className = className;
  return element;
}

export function badge(label, style = "text-bg-secondary") {
  return textElement("span", label, `badge ${style}`);
}

export function appendDefinition(container, label, value) {
  container.append(
    textElement("dt", label, "col-sm-4"),
    textElement("dd", value || "None", "col-sm-8")
  );
}

export function announce(message, isError = false) {
  const target = document.getElementById(isError ? "error-message" : "status-message");
  target.textContent = message;
  target.className = `alert ${isError ? "alert-danger" : "alert-success"}`;
}
