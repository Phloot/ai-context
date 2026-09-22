# PostgreSQL production query guard

Version: 1.0.0. Built from the supplied work-item description on September 22, 2026.

This package adds a production query skill and a local Copilot pre-tool hook.
It includes Python code, configuration, an SDK adapter, tests, and integration guidance.
It does not connect to a database.

## What is implemented

- Exact interception of four named aliases for `postgres_db.run_query`.
- Silent pass-through for other tools and known non-production targets.
- Private target inventory with explicit production classification.
- PostgreSQL syntax review with the pinned `pglast` parser.
- Allow, deny, or review decisions with static, redacted reasons.
- A command hook for `~/.copilot/hooks` and an SDK callback adapter.
- Tests for SQL decisions, process output, target resolution, parser failure, and SDK deadlines.

See [the policy reference](skills/postgres-production-query/references/policy.md) for exact rules and limitations.

## Integration status

The Python behavior and subprocess adapters were tested locally.
No live Copilot session, IntelliJ client, MCP server, or production database was available.
The fixtures model documented payloads; they are not captured runtime payloads.

Your integration must verify three local facts:

1. The exact tool name that Copilot exposes for `postgres_db.run_query`.
2. The server's mapping from its `database` argument to the real host, port, and database.
3. The catalog manifest schema and installation conventions in your `ai-context` repository.

Run the [live verification procedure](docs/verification.md) before enabling production use.
Keep the existing username guard and read-only transaction enforcement.
The hook adds review before execution; it does not change the server.

## Package layout

| Path | Responsibility |
| --- | --- |
| `skills/postgres-production-query/` | Agent workflow and policy reference. |
| `hooks/postgres-query-hooks.json` | Native command-hook registration. |
| `hooks/scripts/postgres_query_hook.py` | Event parsing, scope, and JSON decisions. |
| `hooks/scripts/pg_query_policy/targets.py` | Private configuration and target resolution. |
| `hooks/scripts/pg_query_policy/sql_review.py` | SQL syntax policy. |
| `integrations/sdk_hook.py` | Async callback with a child-process deadline. |
| `config/postgres-query-policy.example.json` | Synthetic target inventory and default limits. |
| `tests/` | Unit, subprocess, and documented-contract tests. |
| `catalog/components/hooks/postgres-query-hooks.example.yaml` | Manifest mapping example for repository integration. |
| `docs/integration.md` | Codebase handoff and SDK integration. |
| `docs/verification.md` | Local and live acceptance checks. |
| `docs/sources.md` | Verified contracts, parser decision, and source links. |

## Install on macOS or Linux

Prerequisites: Python 3.10 or later, Copilot CLI, and an approved `postgres_db` MCP server.
The local tests used Python 3.12 on Linux.
Use your approved package index if public PyPI is unavailable.
The package does not install Python dependencies during a tool call.

Run these commands from the extracted package directory:

```bash
PG_HOOK_HOME="${COPILOT_HOME:-$HOME/.copilot}"
mkdir -p "$PG_HOOK_HOME/hooks/scripts/pg_query_policy" "$PG_HOOK_HOME/skills"
python3 -m venv "$PG_HOOK_HOME/hooks/postgres-query-venv"
"$PG_HOOK_HOME/hooks/postgres-query-venv/bin/python" -m pip install -r requirements.txt
cp hooks/scripts/postgres_query_hook.py "$PG_HOOK_HOME/hooks/scripts/"
cp hooks/scripts/pg_query_policy/*.py "$PG_HOOK_HOME/hooks/scripts/pg_query_policy/"
cp integrations/sdk_hook.py "$PG_HOOK_HOME/hooks/scripts/"
cp -R skills/postgres-production-query "$PG_HOOK_HOME/skills/"
```

Create the private policy file only if it does not exist:

```bash
if [ ! -e "$PG_HOOK_HOME/postgres-query-policy.json" ]; then
  (umask 077; cp config/postgres-query-policy.example.json "$PG_HOOK_HOME/postgres-query-policy.json")
fi
```

Replace every example target with a verified server mapping.
Include every production and non-production selector that this server supports.
Do not commit the resulting policy file or add credentials to it.
Keep `review_action` set to `deny` until interactive approval passes verification.

Run the local tests and synthetic checks before registration.
Then copy the separate hook configuration:

```bash
cp hooks/postgres-query-hooks.json "$PG_HOOK_HOME/hooks/"
```

The supplied command resolves the installation through `COPILOT_HOME`, or `~/.copilot` when that variable is unset.
It does not depend on the repository working directory.
For another policy location, set `POSTGRES_QUERY_POLICY` to an absolute path in the host environment.

The configuration intentionally receives every `preToolUse` event.
The script returns no output for unrelated tool names before loading configuration or the parser.
This avoids a second, potentially inconsistent tool-name filter in the registration file.
Malformed events without a valid tool name are denied because their scope cannot be established.
Events above the 256 KiB input limit are also denied before tool identification.

For Windows, adapt the command entry to PowerShell and use the virtual environment's `Scripts/python.exe` path.
The supplied registration and installation commands were not tested on Windows.

## Run tests

From the package directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
```

A synthetic production lookup can exercise the command boundary without a database:

```bash
POSTGRES_QUERY_POLICY="$PWD/config/postgres-query-policy.example.json" \
.venv/bin/python -I hooks/scripts/postgres_query_hook.py <<'JSON'
{"toolName":"postgres_db.run_query","toolArgs":{"database":"orders-prod","sql":"SELECT id FROM public.orders WHERE id = 42 LIMIT 20","max_rows":20}}
JSON
```

Expected result: one JSON object with `permissionDecision` set to `allow`, and exit status `0`.
The example policy is only a test fixture. Do not use its synthetic mappings for production.

## Enable confirmation

Set `review_action` to `ask` only after approval and rejection both work in the target host.
For the SDK adapter, also set `allow_ask=True` after that verification.
The host must present a real approval prompt for the exact pending call.
Do not use an automatic approval handler as the confirmation implementation.

## Important limits

The inventory is a trusted declaration, not live connection discovery.
A stale alias mapping can cause incorrect environment classification.
Refresh the inventory whenever MCP routing changes.

SQL limits restrict result size, not execution cost.
Views, extensions, overloaded operators, casts, and database privileges can change execution behavior.
Use database permissions, a trusted search path, and statement and lock timeouts.

A Copilot command-hook timeout can continue through the normal permission flow.
Missing or disabled hook registration also removes this review layer.
The SDK adapter denies on its own child-process timeout, but the host must still invoke and honor the callback.
Neither adapter covers alternate SQL tools or shell clients.

## Remove or update

To remove this registration, delete only `postgres-query-hooks.json` from the configured hook directory.
Remove the skill directory separately if it is no longer needed.
Leave unrelated hook configurations and scripts in place.

For updates, preserve the private policy and compare it with the new example schema.
Repeat local tests and live contract checks after a Copilot, SDK, parser, or MCP routing change.

Documentation was reviewed for ASD-STE100 alignment. The official dictionary was not available.
