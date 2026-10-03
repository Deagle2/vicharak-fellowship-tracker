# Vicharak Campus Fellowship — Submission Tracker

Students submit via **Pull Request**. Maintainer **Merge = Accept** → GitHub Action auto-allocates links + points.

Source of truth for fellows: `fellows.csv` (synced from the `Batch 1` tab of the Fellowship sheet — 59 fellows: 61 rows minus 2 removed dupes, Lakshya split into normal + Team Jatayu rows, plus name fix for Aaditya Goswami).
Points: `points.json` — Blog/LinkedIn/X = 40, Documentation = 30, GitHub Project = 70, Workshop = 100, Video = 90, Community = 20, Bug = 25, Feature = 60, Referral = 30, Demo = 50. PurchaseProof = 0 (first-PR kit gate, flips Kit to YES). Threshold = 250.

## Join — purchase proof must be your first PR
1. Submit your screenshot in your submission file: copy `submissions/TEMPLATE.json` → `submissions/<Your-Name>_PurchaseProof_<YYYY-MM-DD>.json` and put your board / invoice photo link in it.
2. Open a PR with that link, titled `[PurchaseProof] Your Name`.
3. I check it. If it is valid purchase proof, I accept (merge) the PR and your Kit status in the live score list below flips to `YES`.

If your first PR is not the purchase proof, it will not be accepted. Do the proof first, then send regular submissions.

Full steps: [`docs/JOIN.md`](docs/JOIN.md).

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
- `Total` = sum. `summary.csv` adds threshold flag (>=250 ELIGIBLE).

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
_Updated 2026-10-01 10:55 UTC - Threshold 250 - 0/59 with points_

| Rank | Fellow | GitHub | Kit | Total | Status |
|---:|---|---|---|---:|---|
| 1 | Aaditya Goswami | @aadii02 | NO | **0** | BELOW |
| 2 | Abhishek Jain | @abhishek261007 | NO | **0** | BELOW |
| 3 | Adeep AG | @adeep13 | NO | **0** | BELOW |
| 4 | Aditya Nukala | @adikp98 | NO | **0** | BELOW |
| 5 | Aditya Reddy | @aditya-1020 | NO | **0** | BELOW |
| 6 | Amaan Pathan | @amaan9737 | NO | **0** | BELOW |
| 7 | Amrutha M | @amrutham-24 | NO | **0** | BELOW |
| 8 | Ankit raj | @ankitra-j | NO | **0** | BELOW |
| 9 | ANNESTIO PIETY CASTANHA | @apcetc | NO | **0** | BELOW |
| 10 | Anusheel Singh | @anusheelsingh12 | NO | **0** | BELOW |
| 11 | Arafat Babar | @arafatbabar | NO | **0** | BELOW |
| 12 | Arijit Ghosh | @ari-jit | NO | **0** | BELOW |
| 13 | Arjun A | @arjnchrn | NO | **0** | BELOW |
| 14 | Arush Dwivedi | @arushdwivedi11 | NO | **0** | BELOW |
| 15 | Ashish Kumar Pal | @jipal5212-wq | NO | **0** | BELOW |
| 16 | CHERALA ROHAN | @therohancherala | NO | **0** | BELOW |
| 17 | Gantla Venkata Sravan | @sravangantla007 | NO | **0** | BELOW |
| 18 | Hardik Kumar Sinha | @hksinha510 | NO | **0** | BELOW |
| 19 | Harshit Kumar Sharma | @harshit2387 | NO | **0** | BELOW |
| 20 | hruday duppalapudi | @hruday-inventory-03 | NO | **0** | BELOW |

_Showing top 20 of 59 - full list in [SCORES.md](SCORES.md)_
<!-- SCORES_END -->

Full table: [`SCORES.md`](SCORES.md) · Machine-readable: [`allocations/summary.csv`](allocations/summary.csv) · PDF: [`fellowship_scores.pdf`](fellowship_scores.pdf)
