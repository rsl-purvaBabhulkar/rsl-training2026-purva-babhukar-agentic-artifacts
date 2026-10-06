# AI Coding Assistant Artifacts — Assignment Write-up

Tool used: **Cursor Agent** (`AGENTS.md` = project-wide instructions;
`.cursor/rules/*.mdc` with `globs` = folder-scoped rules;
`.cursor/skills/<name>/SKILL.md` = a skill).

---

## Task 1 — Project-wide instructions

**Artifact:** [`AGENTS.md`](./AGENTS.md) — 4 testable standards:
1. Type hints + docstring on every public function/method.
2. Every new feature ships with a pytest test file (happy path + failure path).
3. No bare `except:`; exceptions are specific classes with descriptive messages.
4. Currency values formatted as `₹{amount:.2f}`.

**Prompt used (standards NOT repeated):**
> "Add a feature that lets a member renew a borrowed book, extending the due date by 7 days — but only if the book isn't already overdue."

**Result:** `Book.renew()` + `LibraryManager.renew_book()`, with
`tests/models/test_book.py` and `tests/services/test_library_manager.py`
(happy + failure paths for each). All 4 standards were followed
automatically.

---

## Task 2 — Folder-scoped rule

**Artifacts:**
- [`.cursor/rules/services.mdc`](./.cursor/rules/services.mdc)
  (`globs: src/services/**`) — stricter: validate inputs first,
  document `Side effects:` explicitly, never format/print for a human.
- [`.cursor/rules/reports.mdc`](./.cursor/rules/reports.mdc)
  (`globs: src/reports/**`) — different standard: pure functions, never
  raise, no business logic, fixed report shape.

**Same-kind prompt applied to both folders:**
> "Add a way to identify overdue books and report on them."

- In `src/services/library_manager.py` → `get_overdue_loans()`: validates via
  existing dict lookups, documents `Side effects: none`, returns raw
  `Book`/`Member` data — no printing, no currency formatting.
- In `src/reports/formatter.py` → `generate_overdue_report()`: pure (never
  mutates its arguments — proven by `test_generate_overdue_report_is_pure`),
  never raises on an empty list, follows the existing title/`"="*24` shape,
  and does **not** import from `src/services/`.

Both are tested. This shows the same request produces
structurally different code depending on which folder it lands in — in Cursor,
the matching `.mdc` rule is attached when the active files match its `globs`.

---

## Task 3 — Skill

**Artifact:** [`.cursor/skills/new-report-formatter/SKILL.md`](./.cursor/skills/new-report-formatter/SKILL.md)
— a repeatable procedure for adding any new report: naming convention,
required shape, purity/no-raise requirements, and a matching-test step,
plus a fill-in-the-blank template. Discoverable as a project skill (Agent
picks it up from the description when you ask to add a report).

**Prompt used (skill triggers on the phrase "add a report", no format rules repeated):**
> "Add a report showing each member's current loan count."

**Result:** `generate_member_loan_counts_report()` — same title +
`"=" * 24` shape, same "nothing to report" pattern, same pure/no-raise
guarantees, plus `tests/reports/test_formatter.py` additions for the happy
path and the empty-input path.

---

## Task 4 — Diagnose and refine

Reviewing Tasks 1–3 against the artifacts turned up three real gaps:

### Gap 1 — Inconsistent currency formatting (standard 4)
- **Found:** `library_manager.py` raised
  `PermissionError("Cannot borrow books with outstanding fines over 250₹.")`
  — symbol on the wrong side, no `.2f`, and a hardcoded `250` disconnected
  from the actual threshold value.
- **Diagnosis:** this string predates `AGENTS.md` (it shipped
  in the starter repo). Standard 4 only gets applied by the assistant when
  it's actively writing new code near that string — nothing forces a sweep
  of pre-existing strings, so it was inherited silently.
- **Fix:** reworded to `f"...over ₹{self.max_outstanding_fine:.2f}."` using
  a named `max_outstanding_fine` attribute instead of a bare literal, added
  a regression test (`test_checkout_blocked_by_fines_uses_consistent_currency_format`).

### Gap 2 — Missing "Side effects:" line on `renew_book()` (folder rule)
- **Found:** `renew_book()` (Task 1) had no `Side effects:` line, breaking
  `services.mdc` rule #2.
- **Diagnosis:** `renew_book()` was written in Task 1, *before* the
  `src/services/` folder rule existed (added in Task 2). Folder rules apply
  going forward, not retroactively — nothing re-checks already-committed
  code when a new rule is added.
- **Fix:** added the missing `Side effects:` line, and added a clause to
  `AGENTS.md` ("Applies to old code too") instructing the
  assistant to bring existing functions up to standard whenever it next
  touches that file or folder.

### Gap 3 — Missing docstrings/type-hint compliance on pre-existing methods
- **Found:** `add_book`, `register_member`, `checkout_book`,
  `process_return`, `search_books_by_author` (all pre-existing,
  `src/services/`) and `main()` (`src/main.py`) had no docstrings —
  breaking root standard #1.
- **Diagnosis:** same root cause as Gap 2 — standard 1's original wording
  didn't say whether it covered legacy code, so it was read as "new code
  only" and legacy methods were skipped during Tasks 1–3.
- **Fix:** added docstrings (with `Side effects:` lines for the
  `services/` ones, per that folder's rule) to all five methods and to
  `main()`, plus clarified `AGENTS.md` as described in Gap 2's fix.

### Re-run confirmation
After the fixes, the full suite (13 tests, all standards) passes:

```
$ python -m pytest tests/ -v
...
13 passed in 0.02s
```


---
