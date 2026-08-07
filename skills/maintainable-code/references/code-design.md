# Code design review

Use this reference when adding behavior or changing code with unclear ownership. It is especially important in new or AI-heavy areas, where locally reasonable additions can accumulate into an incoherent design.

## Establish ownership

For each changed behavior, identify:

- the component that owns the decision;
- the boundary that supplies or consumes data;
- the state that the behavior reads or changes.

If ownership is unclear, resolve it before adding another helper or branch.

## Review the design

Check the completed slice for these failure modes:

- one function or class coordinates work and implements unrelated policy;
- domain decisions depend directly on transport, persistence, or framework details;
- similar concepts use competing models, names, or flows;
- behavior is distributed across helpers with no clear owner;
- a generic utility hides domain behavior;
- an abstraction has only speculative consumers or pass-through implementations;
- branching or mutable state makes the behavior difficult to explain or test;
- a local shortcut creates a second architectural pattern.
- the same business decision has more than one implementation.

Refactor when the problem is present. Do not extract code solely because a threshold was crossed.

## Choose the smallest corrective change

Prefer, in order:

1. simplify control flow;
2. move behavior to its existing owner;
3. introduce a focused collaborator for a distinct responsibility;
4. introduce an interface only at a real ownership, volatility, or integration boundary.

When no owner exists, create one and name it for its responsibility. Avoid catch-all services, managers, processors, and utility modules.

Consolidate duplicate domain decisions even when their names or syntax differ. Do not abstract syntax that has different ownership or reasons to change.
