# Project Instructions — Library Inventory System

This is the project-wide **instructions** file (`AGENTS.md`). Cursor injects it
for Agent automatically. The same standards are also in
`.cursor/rules/project.mdc` (`alwaysApply: true`) so they show under **Customize → Rules**.

## Standards (testable)

1. **Type hints + docstrings on every public function/method.**
   Any function or method that is not prefixed with `_` must have full
   parameter/return type hints and a one-to-three line docstring describing
   what it does. This can be checked by grep: no `def [a-zA-Z]` line lacking
   a docstring on the following line, and no missing `->` return arrow.

2. **Every new feature ships with a pytest test file.**
   Any new public function/method added to `src/` must have a matching
   `tests/test_<module>.py` (mirroring the source path) that covers:
   - at least one **success/happy-path** case, and
   - at least one **failure/error-path** case (an invalid input or a
     documented exception).
   A feature without a corresponding test file under `tests/` is incomplete.

3. **No bare `except:` and no silent failures.**
   Exceptions must name a specific exception class (e.g. `ValueError`,
   `KeyError`), and every `raise` must include a human-readable message
   explaining what went wrong and, where relevant, what value caused it.
   Never catch-and-pass without at least a comment explaining why it's safe.

4. **Consistent currency formatting.**
   Any money value shown to a user must be formatted as `₹{amount:.2f}`
   (matching `src/reports/formatter.py`) — never a bare float, never a
   different currency symbol.

## Applies to old code too (added after Task 4 review)

These standards are not just for code you're currently writing. When you
touch a file for any reason, bring the function(s) you're modifying or
sitting next to up to full compliance too — don't leave a `def` two lines
above your new code without a docstring just because you didn't write it.
If a folder rule (see `.cursor/rules/`) is added after code already exists
there, treat the next edit to that file as a chance to retrofit the
existing functions, not just the new one.

## Project conventions (context, not a hard rule)

- `src/models/` — data classes (`Book`, `Member`) with their own invariants.
- `src/services/` — business logic / state (`LibraryManager`).
- `src/reports/` — pure string-formatting functions only.
- Run tests with: `python -m pytest tests/ -v` from the project root.
