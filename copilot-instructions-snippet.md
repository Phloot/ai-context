## Maintainability workflow

For each task that plans, writes, modifies, refactors, or reviews code or
executable configuration, invoke the `/maintainable-code` skill before
implementation.

Apply the skill to application code, libraries, scripts, build logic,
deployment logic, infrastructure code, migrations, and test code.

Apply the checks proportionally. Test code can use repository-approved
exceptions for fixtures, parameterization, and setup code.

Do not invoke the skill for documentation-only changes or exploration that
does not modify files. Do not analyze generated or vendored code unless the
task explicitly concerns that code.

Continue to apply the skill after each coherent implementation slice and
before completion.

If you delegate applicable changes, instruct each delegated agent to apply the
`/maintainable-code` skill throughout its task.
