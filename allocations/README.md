# Allocations (auto-generated — do not edit by hand)

- `allocations/<Fellow_Name>.csv` — one file per fellow, layout matches screenshot:
  `,Submission 1..5,Points` rows: Names, Github, Linkedin, Blog, X, Workshop, Total.
  Note: canonical categories are Github(=Project), Linkedin, Blog, X, Workshop. Other types (Documentation/Video/etc.) count toward Total and appear in `summary.csv` + PDF, but per-screenshot CSV keeps the 5 requested rows for readability.
- `summary.csv` — one row per fellow: counts + points + threshold flag.
- `../fellowship_scores.pdf` — human-readable scorecard.

Regenerated on every merge to `main` by GitHub Action. To regenerate locally: `python scripts/update_scores.py`.
