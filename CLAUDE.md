# CLAUDE.md

## Project

College basketball analysis for the 2025-26 season. Marimo notebook (`notebooks/cbb_analysis.py`) with data in `data/`. Focus on Big East and A-10 conferences.

## Marimo Notebook Rules

- **Variable names must be unique across all cells.** Marimo enforces this at startup. Even loop variables (`for row in ...`, `for col in ...`) count as cell-level definitions.
- **Prefix cell-local variables with `_`** (e.g., `_row`, `_col`, `_vals`) to make them private to that cell. This is the fix for the multiple-definitions error.
- **Cell function signatures are auto-managed.** Marimo's linter rewrites `def _(...)` params and `return` statements to match what the cell reads/writes. Don't fight it — just make sure your variable names don't collide.
- **Imports inside cells are fine**, but if another cell needs the import, it must be returned and listed in that cell's signature.
- Run the notebook with: `uv run marimo edit notebooks/cbb_analysis.py --watch`
