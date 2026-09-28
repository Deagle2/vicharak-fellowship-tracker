# Vicharak Campus Fellowship — Submission Tracker

Students submit via **Pull Request**. Maintainer **Merge = Accept** → GitHub Action auto-allocates links + points.

Source of truth for fellows: `fellows.csv` (fetched from `Fellowship program.xlsx` on PC — 78 unique fellows, de-duplicated).
Points: `points.json` — Blog/LinkedIn/X = 40, Documentation = 30, GitHub Project = 70, Workshop = 100, Video = 90, Community = 20, Bug = 25, Feature = 60, Referral = 30, Demo = 50. Threshold = 600.

## Flow
1. Student: copy `submissions/TEMPLATE.json` → `submissions/<Your-Name>_<Type>_<YYYY-MM-DD>.json`
   Example: `submissions/Arjun_A_Blog_2026-09-28.json`
2. Fill: `fellow` (exact name from fellows.csv), `type` (Blog/Linkedin/X/Project/Workshop/Documentation/Video/Community/Bug/Feature/Referral/Demo), `title`, `link`, `date`.
3. Open PR with title: `[Blog] Arjun A — https://...` (or [Linkedin]/[X]/[Project]/[Workshop]).
   PR body must contain the link.
4. Maintainer reviews → **Merge = accept**, Close without merge = reject (no points).
5. On push to `main`, `.github/workflows/score.yml` runs `scripts/update_scores.py`:
   - validates all `submissions/*.json`
   - groups by fellow + category
   - rewrites `allocations/<Fellow>.csv` in screenshot layout + `allocations/summary.csv` + `fellowship_scores.pdf`
   - auto-commits back to `main` if changed.

## Screenshot layout (per-fellow CSV)
Matches your reference image:
```
,Submission 1,Submission 2,Submission 3,Submission 4,Submission 5,Points
Names,<Fellow Name>,,,,,
Github,<link>,<link>,,,, <pts>
Linkedin,<link>,...,,, <pts>
Blog,...
X,...
Workshop,...
Total,,,,,,<total>
```
- 5 link columns minimum (extends if >5 in any category).
- Points = count × per-type points.
- `Total` = sum. `summary.csv` adds threshold flag (>=600 ELIGIBLE).

## Repo map
- `fellows.csv` — canonical list (do not edit manually, re-export from xlsx if needed)
- `points.json` — edit points here, Action picks it up
- `submissions/` — student JSONs only
- `allocations/` — generated, do not hand-edit (overwritten)
- `scripts/update_scores.py` — scoring logic, also runnable locally: `python scripts/update_scores.py`
- `fellowship_scores.pdf` — generated human-readable scorecard (links + points)

## Local test
```
python scripts/update_scores.py
```

## Admin
- Repo: https://github.com/nilangwork17/vicharak-fellowship-tracker
- Invite students as collaborators with `Triage`/`Write` (PR only, protect `main` → require PR, no direct push).
- To re-fetch fellows: re-run `extract_fellows.py` on updated `Fellowship program.xlsx` → overwrite `fellows.csv`.

## Admin — Live Score List (auto-updated on every merge, do not edit below)
<!-- SCORES_START -->
_Updated 2026-09-28 06:53 UTC - Threshold 600 - 1/78 with points_

| Rank | Fellow | Total | Status |
|---:|---|---:|---|
| 1 | Arjun A | **595** | BELOW |
| 2 | Abhishek Jain | **0** | BELOW |
| 3 | Adeep AG | **0** | BELOW |
| 4 | Aditya Nukala | **0** | BELOW |
| 5 | Aditya Reddy | **0** | BELOW |
| 6 | Amaan Pathan | **0** | BELOW |
| 7 | Amrutha M | **0** | BELOW |
| 8 | Anandu Rajan | **0** | BELOW |
| 9 | Ankit Choudhury | **0** | BELOW |
| 10 | Ankit raj | **0** | BELOW |
| 11 | ANNESTIO PIETY CASTANHA | **0** | BELOW |
| 12 | Anusheel Singh | **0** | BELOW |
| 13 | Appu Raj | **0** | BELOW |
| 14 | Arafat Babar | **0** | BELOW |
| 15 | Arijit Ghosh | **0** | BELOW |
| 16 | Arjav Sanjaybhai Khunt | **0** | BELOW |
| 17 | Arjun Rajesh | **0** | BELOW |
| 18 | Arush Dwivedi | **0** | BELOW |
| 19 | Ashish Kumar Pal | **0** | BELOW |
| 20 | Ashutosh Mishra | **0** | BELOW |

_Showing top 20 of 78 - full list in [SCORES.md](SCORES.md)_
<!-- SCORES_END -->

Full table: [`SCORES.md`](SCORES.md) · Machine-readable: [`allocations/summary.csv`](allocations/summary.csv) · PDF: [`fellowship_scores.pdf`](fellowship_scores.pdf)
