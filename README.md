# Vicharak Campus Fellowship - Submission Tracker

Think of this repo as your fellowship marksheet.

You do work outside (blog, video, LinkedIn post, project), you send us the link here, I press Accept, and a robot automatically gives you points and updates the score list below.

You need 250 points to become ELIGIBLE.

Points list (from `points.json`):
Blog = 40, Linkedin = 40, X = 40, Project (GitHub) = 70, Workshop = 100, Documentation = 30, Video = 90, Community = 20, Bug = 25, Feature = 60, Referral = 30, Demo = 50. PurchaseProof = 0 points, but it unlocks you.

Student list comes from `fellows.csv` (59 fellows).

## Step 0 - Join first: purchase proof must be your first PR

You cannot submit anything until I know you have the kit. So your very first submission must be your kit proof.

1. Upload your kit photo somewhere public. Take a photo of your board / invoice, upload it to Google Drive / Imgur / LinkedIn post (set to Anyone can view), and copy that `https://...` link.
2. Fill the form: copy `submissions/TEMPLATE.json` to a new file named `submissions/<Your-Name>_PurchaseProof_<YYYY-MM-DD>.json`. Example: `submissions/Arjun_A_PurchaseProof_2026-09-28.json`. Paste your photo link in the `link` field.
3. Send it for checking: open a PR titled `[PurchaseProof] Your Name`, and paste the same link in the PR description too.
4. I check it. I open your link and see if it is really your board / bill. If yes, I press Merge (Accept) and your Kit in the score list below changes to `YES`. If no, I close it and you fix and resend.

Rule: If your first PR is not the purchase proof, I will close it. Do proof first, then do the rest.

Full steps with pictures in words: [`docs/JOIN.md`](docs/JOIN.md).

## Step 1 - How to send your regular work (after proof is accepted)

Only after your PurchaseProof is accepted, do this for Blog, Linkedin, X, Project, etc.

1. Make your draft viewable first - do NOT post on social media yet. Put your draft in a Google Doc (or similar) with `Anyone with link can view`, and copy that `https://...` link. This is what you send for review. Only after I approve the PR, post it on the dedicated platform - Medium for Blog, x.com for X, LinkedIn for Linkedin, GitHub for Project, YouTube for Video.
2. Fill the form: copy `submissions/TEMPLATE.json` to `submissions/<Your-Name>_<Type>_<YYYY-MM-DD>.json`. Example: `submissions/Arjun_A_Blog_2026-09-28.json`.
   - `fellow`: your exact name from `fellows.csv`, example `Arjun A`
   - `type`: one word - Blog, Linkedin, X, Project, Workshop, Documentation, Video, Community, Bug, Feature, Referral, Demo
   - `title`: short name of your work
   - `link`: paste your Google Doc draft link here for review (must start with `https://` and open without login). After approval you will post the final link on the dedicated platform.
   - `date`: today in `YYYY-MM-DD`
3. Send it: open a PR titled `[Type] Your Name`. Example: `[Blog] Arjun A`. Paste the same Google Doc link in the PR description so I can click fast.
4. One file = one PR. Do not put 5 links in one file. Send 5 PRs.

## Step 2 - How I check and give points

I am the checker, the robot is the calculator.

1. You tell me what it is: your `type` + PR title says `[Blog]` or `[X]`, etc.
2. Robot checks only format: is the name correct? Does link start with `https://`? Is type valid?
3. I click and verify by eye: I open your Google Doc draft, check it matches the claimed `type` (`[Blog]` = blog draft, `[X]` = X post text, etc). If good, I press Merge = Accept. You then post the final version on the dedicated social platform. If not good, I press Close = Reject and you get 0, fix and resend.
4. After Merge, the robot runs automatically (`.github/workflows/score.yml` + `scripts/update_scores.py`):
   - collects all accepted links
   - groups them by person and type
   - rewrites your marksheet files and updates the live score list below

So: your title is your claim, my Merge is the approval.

## Step 3 - Where to see your points

- Live table below in this README (top 20, auto-updated on every Merge, do not edit it)
- Full table: [`SCORES.md`](SCORES.md)
- Computer file: [`allocations/summary.csv`](allocations/summary.csv)
- PDF marksheet: [`fellowship_scores.pdf`](fellowship_scores.pdf)
- Per-person file: `allocations/<Your-Name>.csv` looks like this:

```
,Submission 1,Submission 2,Submission 3,Submission 4,Submission 5,Points
Names,Your Name,,,,,
Github,<link>,<link>,,,, <pts>
Linkedin,<link>,...,,, <pts>
Blog,...
X,...
Workshop,...
Total,,,,,,<total>
```

Points = number of accepted links x points for that type. Total = sum of all. 250+ = ELIGIBLE, below = BELOW.

## What is inside this repo (simple map)

- `fellows.csv` - class list. Do not edit by hand.
- `points.json` - points rule book. If I change points here, robot follows it.
- `submissions/` - your filled forms only (JSON files). This is the only folder you touch.
- `allocations/` - auto-made marksheets. Do not edit, robot overwrites them.
- `scripts/update_scores.py` - robot brain. Run `python scripts/update_scores.py` to test locally.
- `fellowship_scores.pdf` - auto-made PDF of all scores.

## For Admin (me)

- Repo: https://github.com/nilangwork17/vicharak-fellowship-tracker
- Keep `main` protected - only via PR, no direct push.
- To update students: re-export `Fellowship program.xlsx` to `fellows.csv`.

## Live Score List (auto-updated on every merge, do not edit below)
<!-- SCORES_START -->
_Updated 2026-10-09 19:30 UTC - Threshold 250 - 2/60 with points_

| Rank | Fellow | GitHub | Kit | Total | Status |
|---:|---|---|---|---:|---|
| 1 | Saksham Sud | @geneticscrol | YES | **70** | BELOW |
| 2 | Harshit Kumar Sharma | @harshit2387 | YES | **40** | BELOW |
| 3 | Aaditya Goswami | @aadii02 | NO | **0** | BELOW |
| 4 | Abhishek Jain | @abhishek261007 | NO | **0** | BELOW |
| 5 | Adeep AG | @adeep13 | YES | **0** | BELOW |
| 6 | Aditya Nukala | @adikp98 | NO | **0** | BELOW |
| 7 | Aditya Reddy | @aditya-1020 | NO | **0** | BELOW |
| 8 | Amaan Pathan | @amaan9737 | YES | **0** | BELOW |
| 9 | Amrutha M | @amrutham-24 | NO | **0** | BELOW |
| 10 | Anandu Rajan | @anandurajan1209 | NO | **0** | BELOW |
| 11 | Ankit raj | @ankitra-j | NO | **0** | BELOW |
| 12 | ANNESTIO PIETY CASTANHA | @apcetc | YES | **0** | BELOW |
| 13 | Anusheel Singh | @anusheelsingh12 | NO | **0** | BELOW |
| 14 | Arafat Babar | @arafatbabar | NO | **0** | BELOW |
| 15 | Arijit Ghosh | @ari-jit | NO | **0** | BELOW |
| 16 | Arjun A | @arjnchrn | NO | **0** | BELOW |
| 17 | Arush Dwivedi | @arushdwivedi11 | NO | **0** | BELOW |
| 18 | Ashish Kumar Pal | @jipal5212-wq | NO | **0** | BELOW |
| 19 | CHERALA ROHAN | @therohancherala | NO | **0** | BELOW |
| 20 | Gantla Venkata Sravan | @sravangantla007 | YES | **0** | BELOW |

_Showing top 20 of 60 - full list in [SCORES.md](SCORES.md)_
<!-- SCORES_END -->

Full table: [`SCORES.md`](SCORES.md) · Machine-readable: [`allocations/summary.csv`](allocations/summary.csv) · PDF: [`fellowship_scores.pdf`](fellowship_scores.pdf)
