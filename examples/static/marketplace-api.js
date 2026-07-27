export const API = "/api/context-marketplace";

const knownErrors = {
  CATALOG_INVALID: "The current catalog is invalid. Sync to recover the last valid catalog.",
  COMPONENT_NOT_FOUND: "That component is no longer in the catalog.",
  DEPENDENCY_IN_USE: "Disable the enabled dependents first.",
  COMPONENT_INCOMPATIBLE: "This component is incompatible with the current environment.",
  EXTERNAL_DEPENDENCY_UNAVAILABLE: "Configure the required external dependency outside the marketplace.",
  LOCAL_MODIFICATION_CONFLICT: "Local changes were preserved. Resolve them before retrying.",
  UNMANAGED_FILE_CONFLICT: "An unmanaged destination file was preserved.",
  MARKETPLACE_BUSY: "Another marketplace operation is still running. Try again shortly."
};

export async function request(path, options = {}) {
  const response = await fetch(path, { headers: { Accept: "application/json" }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = body.error || {};
    throw new Error(knownErrors[error.code] || "The marketplace request failed. Check Flightplan logs for details.");
  }
  return body;
}
