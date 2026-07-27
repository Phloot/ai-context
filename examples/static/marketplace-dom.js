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
  window.clearTimeout(announce.dismissTimer);
  ["status-message", "error-message"].forEach((id) => {
    const messageElement = document.getElementById(id);
    messageElement.textContent = "";
    messageElement.className = "visually-hidden";
  });
  const target = document.getElementById(isError ? "error-message" : "status-message");
  target.textContent = `${message.charAt(0).toUpperCase()}${message.slice(1)}`;
  target.className = `alert ${isError ? "alert-danger" : "alert-success"}`;
  announce.dismissTimer = window.setTimeout(() => {
    target.textContent = "";
    target.className = "visually-hidden";
  }, 7000);
}

announce.dismissTimer = 0;
