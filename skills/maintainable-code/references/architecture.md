# Architecture review

Use this reference for structural changes. Apply repository architecture before these defaults.

## Classify the architecture

- **Established:** Preserve documented boundaries and dependency rules.
- **Emerging:** Infer current responsibilities, then define only the boundary required by the change.
- **Greenfield:** Create the smallest structure that separates responsibilities introduced now.

A flat package is not automatically an intended architecture.

## Detect when structure must grow

Review package structure when one condition appears:

- A second route or feature group is added.
- Business behavior can run without its transport.
- Persistence or an external integration is introduced.
- An entry point begins to contain application behavior.
- A module gains a second reason to change.
- A framework model begins to control business behavior.

These conditions trigger review. They do not require new structure. Keep the current structure when the behavior has a clear owner and does not add a distinct responsibility or dependency boundary.

Create a package or file only when the current change gives it a concrete responsibility.

## Protect dependency direction

- Keep business decisions independent from transport and persistence details when a business domain exists.
- Point dependencies toward the more stable policy or domain code.
- Keep frameworks, databases, and external clients at boundaries when practical.
- Use separate boundary models when framework or storage models would leak details inward.
- Use an interface only for a real ownership, volatility, or test boundary.

Do not require canonical layers for simple behavior. Do not add an interface, adapter, or use-case class only to match a pattern.
