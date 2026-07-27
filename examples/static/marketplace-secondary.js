import { textElement } from "./marketplace-dom.js";

export function renderProfiles(container, profiles, pending, onApply) {
  container.replaceChildren();
  profiles.forEach((profile) => {
    const column = textElement("div", "", "col-12 col-md-6");
    const card = textElement("article", "", "card card-body h-100");
    card.append(
      textElement("h3", profile.name, "h5"),
      textElement("p", profile.description),
      textElement("p", `Version ${profile.version}`, "small text-body-secondary")
    );
    const changes = Object.entries(profile.component_states).map(
      ([id, enabled]) => `${id}: ${enabled ? "enabled" : "disabled"}`
    );
    const items = textElement("ul", "", "detail-list");
    changes.forEach((item) => items.append(textElement("li", item)));
    const button = textElement(
      "button",
      "Apply profile",
      "btn btn-outline-primary align-self-start"
    );
    button.type = "button";
    button.disabled = pending;
    button.addEventListener("click", () => onApply(profile, changes));
    card.append(items, button);
    column.append(card);
    container.append(column);
  });
}

export function renderActivityRows(body, emptyMessage, items) {
  body.replaceChildren();
  emptyMessage.classList.toggle("d-none", items.length !== 0);
  items.forEach((item) => {
    const row = document.createElement("tr");
    const values = [
      new Date(item.timestamp).toLocaleString(),
      item.operation,
      item.target_id || "—",
      [item.previous_version, item.new_version].filter(Boolean).join(" → ") || "—",
      item.result,
      String(item.conflict_count)
    ];
    values.forEach((value) => row.append(textElement("td", value)));
    body.append(row);
  });
}
