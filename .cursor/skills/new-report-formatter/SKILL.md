---
name: new-report-formatter
description: >-
  Adds a new report formatter for the library system. Use when the user asks
  to add a report, a new formatter, or a new way to display/print library
  data (e.g. "add a report of...", "show a summary of...", "print a list of...").
  Generates a function in src/reports/formatter.py plus matching pytest coverage.
---

# Skill: New Report Formatter

## When to use this
Trigger whenever a new report/summary/printout is requested for the
library system. Do not use this for business-logic changes — if the
request needs new data or a new decision (e.g. "who *should* pay a fine"),
that belongs in `src/services/`, not here.

## Procedure

1. **Name the function** `generate_<subject>_report`, taking whatever
   plain data it needs as arguments (already-computed lists/dicts — never
   call into `src/services/` from inside the function).
2. **Follow the exact report shape** already used in
   `src/reports/formatter.py`:
   ```
   Title Line
   ========================   <- "=" * 24
   one line per record
   ------------------------   <- "-" * 24, ONLY if there's a total/summary
   Total line                 <- ONLY if there's a total/summary
   ```
3. **Write the function to satisfy `.cursor/rules/reports.mdc`:**
   - pure (never mutate an argument)
   - never raises (empty input -> a "nothing to report" line, not an error)
   - full type hints + docstring, matching the root `AGENTS.md` standard
4. **Add the function** to `src/reports/formatter.py`.
5. **Create a matching test file** `tests/reports/test_<name>.py` (or add
   to the existing `tests/reports/test_formatter.py`) with:
   - one test for the happy path (non-empty input renders correctly)
   - one test for the empty-input case (proves it doesn't raise)
6. **Run `python -m pytest tests/reports/ -v`** and confirm all pass before
   reporting completion.

## Template

```python
def generate_<subject>_report(<data>: List[<Type>]) -> str:
    """<One-line description of what this reports on>.

    Args:
        <data>: <what it contains and where it typically comes from>.

    Returns:
        A formatted report string. Never raises; empty input produces a
        "nothing to report" message instead of an error.
    """
    lines = ["<Title>", "=" * 24]

    if not <data>:
        lines.append("<No-data message>.")
        return "\n".join(lines)

    for item in <data>:
        lines.append(f"<one line per record>")

    return "\n".join(lines)
```
