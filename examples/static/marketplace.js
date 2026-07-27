import { API, request } from "./marketplace-api.js";
import { announce, appendDefinition, badge, textElement } from "./marketplace-dom.js";
import { renderTypeFilters } from "./marketplace-filters.js";
import { renderActivityRows, renderProfiles } from "./marketplace-secondary.js";

(() => {
  "use strict";

  const state = { data: null, selectedId: null, selectedTypes: new Set(), view: "marketplace", pending: false };
  const byId = (id) => document.getElementById(id);

  async function loadMarketplace({ preserveFocus = false } = {}) {
    const focusedId = preserveFocus ? document.activeElement?.id : null;
    state.data = await request(API);
    if (!state.selectedId || !state.data.components.some((item) => item.id === state.selectedId)) {
      state.selectedId = state.data.components[0]?.id || null;
    }
    render();
    if (focusedId) byId(focusedId)?.focus();
  }

  function visibleComponents() {
    const query = byId("component-search").value.trim().toLowerCase();
    return state.data.components.filter((component) => {
      const searchable = [component.name, component.description, component.id, component.type, ...component.tags].join(" ").toLowerCase();
      const viewMatches = state.view === "enabled" ? component.enabled : state.view === "updates" ? component.update_available : true;
      const typeMatches = state.selectedTypes.size === 0 || state.selectedTypes.has(component.type);
      return viewMatches && typeMatches && searchable.includes(query);
    });
  }

  function render() {
    const data = state.data;
    byId("catalog-status").textContent = `Catalog ${data.catalog_version} · ${data.last_synchronized_at ? `last synced ${new Date(data.last_synchronized_at).toLocaleString()}` : "not yet synchronized"}`;
    byId("enabled-count").textContent = data.summary.enabled;
    byId("update-count").textContent = data.summary.updates;
    byId("conflict-count").textContent = data.summary.conflicts;
    byId("migration-panel").classList.toggle("d-none", !data.migration.required);
    byId("sync-button").disabled = state.pending;
    byId("migrate-button").disabled = state.pending;
    renderTabs();
    renderTypeFilters(byId("type-filters"), data.available_component_types, state.selectedTypes, toggleType);
    renderComponents();
    renderProfiles(byId("profile-list"), data.profiles, state.pending, applyProfile);
    byId("component-view").classList.toggle("d-none", ["profiles", "activity"].includes(state.view));
    byId("profiles-view").classList.toggle("d-none", state.view !== "profiles");
    byId("activity-view").classList.toggle("d-none", state.view !== "activity");
  }

  function renderTabs() {
    document.querySelectorAll("[data-view]").forEach((button) => {
      const selected = button.dataset.view === state.view;
      button.classList.toggle("active", selected);
      button.setAttribute("aria-current", selected ? "page" : "false");
    });
  }

  function toggleType(type) {
    if (state.selectedTypes.has(type)) state.selectedTypes.delete(type);
    else state.selectedTypes.add(type);
    render();
  }

  function renderComponents() {
    const list = byId("component-list");
    const components = visibleComponents();
    if (!components.some((item) => item.id === state.selectedId)) state.selectedId = components[0]?.id || null;
    list.replaceChildren();
    byId("component-empty").classList.toggle("d-none", components.length !== 0);
    components.forEach((component) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `list-group-item list-group-item-action ${component.id === state.selectedId ? "active" : ""}`;
      button.setAttribute("aria-pressed", String(component.id === state.selectedId));
      button.addEventListener("click", () => { state.selectedId = component.id; renderComponents(); });
      button.append(textElement("span", component.name, "fw-semibold d-block"));
      button.append(textElement("span", component.description, component.id === state.selectedId ? "small" : "small text-body-secondary"));
      const badges = textElement("span", "", "status-badges mt-2");
      badges.append(badge(component.type, "text-bg-light"));
      badges.append(badge(component.enabled ? "Enabled" : "Available", component.enabled ? "text-bg-success" : "text-bg-secondary"));
      if (component.update_available) badges.append(badge("Update", "text-bg-info"));
      if (component.conflicts.length) badges.append(badge("Conflict", "text-bg-danger"));
      if (!component.compatibility.compatible) badges.append(badge("Incompatible", "text-bg-warning"));
      button.append(badges);
      list.append(button);
    });
    const selected = state.data.components.find((item) => item.id === state.selectedId);
    renderDetail(selected);
  }

  function renderDetail(component) {
    const detail = byId("component-detail");
    detail.replaceChildren();
    if (!component) {
      detail.append(textElement("h2", "Select a component", "h5"));
      return;
    }
    detail.append(textElement("h2", component.name, "h4"), textElement("p", component.description));
    const definitions = textElement("dl", "", "row");
    appendDefinition(definitions, "Component ID", component.id);
    appendDefinition(definitions, "Type", component.type);
    appendDefinition(definitions, "Available version", component.available_version);
    appendDefinition(definitions, "Applied version", component.applied_version);
    appendDefinition(definitions, "Dependencies", component.dependencies.join(", "));
    appendDefinition(definitions, "Dependents", component.dependents.join(", "));
    appendDefinition(definitions, "Tags", component.tags.join(", "));
    appendDefinition(definitions, "Compatibility", component.compatibility.compatible ? "Compatible" : component.compatibility.reason);
    detail.append(definitions, textElement("h3", "Release notes", "h6"), textElement("p", component.release_summary));
    if (component.external_dependencies.length) {
      detail.append(textElement("h3", "External dependencies", "h6"));
      const dependencies = textElement("ul", "", "detail-list");
      component.external_dependencies.forEach((item) => dependencies.append(textElement("li", `${item.name} (${item.type}) — ${item.availability}`)));
      detail.append(dependencies);
    }
    if (component.conflicts.length) {
      component.conflicts.forEach((item) => detail.append(textElement("p", `${item.title}: ${item.explanation} ${item.next_action}`, "alert alert-danger")));
    }
    const actions = textElement("div", "", "d-flex flex-wrap gap-2 mt-3");
    const primary = textElement("button", component.enabled ? "Disable" : "Enable", `btn ${component.enabled ? "btn-outline-danger" : "btn-primary"}`);
    primary.type = "button";
    primary.disabled = state.pending || !state.data.catalog_validation.valid || !component.compatibility.compatible;
    primary.addEventListener("click", () => mutateComponent(component, component.enabled ? "disable" : "enable"));
    actions.append(primary);
    if (component.update_available) {
      const update = textElement("button", "Update", "btn btn-info");
      update.type = "button";
      update.disabled = state.pending;
      update.addEventListener("click", () => mutateComponent(component, "update"));
      actions.append(update);
    }
    detail.append(actions);
  }

  async function mutateComponent(component, operation) {
    if (operation === "enable") {
      const missing = component.dependencies.filter((id) => !state.data.components.find((item) => item.id === id)?.enabled);
      const unknown = component.external_dependencies.filter((item) => item.availability === "unknown");
      const notes = [];
      if (missing.length) notes.push(`Dependencies also enabled: ${missing.join(", ")}.`);
      if (unknown.length) notes.push("Some external dependency availability is unknown.");
      if (notes.length && !window.confirm(`${notes.join(" ")} Continue?`)) return;
    }
    await mutate(`${API}/components/${encodeURIComponent(component.id)}/${operation}`, `${operation} ${component.name}`);
  }

  async function mutate(path, label) {
    state.pending = true;
    render();
    try {
      await request(path, { method: "POST" });
      await loadMarketplace({ preserveFocus: true });
      announce(`${label} succeeded.`);
    } catch (error) {
      announce(error.message, true);
    } finally {
      state.pending = false;
      render();
    }
  }

  async function applyProfile(profile, changes) {
    if (window.confirm(`Apply ${profile.name}? This merges ${changes.join(", ")} and does not lock later changes.`)) {
      await mutate(`${API}/profiles/${encodeURIComponent(profile.id)}/apply`, `Apply ${profile.name}`);
    }
  }

  async function renderActivity() {
    try {
      const data = await request(`${API}/activity?limit=50`);
      renderActivityRows(byId("activity-list"), byId("activity-empty"), data.items);
    } catch (error) { announce(error.message, true); }
  }

  function selectView(view) {
    state.view = view;
    const url = new URL(window.location.href);
    url.searchParams.set("view", view);
    window.history.replaceState({}, "", url);
    render();
    if (view === "activity") renderActivity();
  }

  document.addEventListener("DOMContentLoaded", async () => {
    const requestedView = new URL(window.location.href).searchParams.get("view");
    if (["marketplace", "enabled", "updates", "profiles", "activity"].includes(requestedView)) state.view = requestedView;
    byId("component-search").addEventListener("input", renderComponents);
    document.querySelectorAll("[data-view]").forEach((button) => button.addEventListener("click", () => selectView(button.dataset.view)));
    byId("sync-button").addEventListener("click", () => mutate(`${API}/sync`, "Catalog sync"));
    byId("migrate-button").addEventListener("click", () => mutate(`${API}/migrate`, "Migration"));
    try {
      await loadMarketplace();
      if (state.view === "activity") await renderActivity();
    } catch (error) { announce(error.message, true); }
  });
})();
