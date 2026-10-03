# Joining the repo (purchase proof = first PR)

Public to view. To submit, your **first PR must be your purchase proof**.

## Student (join)
1. Fork this repo.
2. Copy `submissions/TEMPLATE.json` → `submissions/<Your-Name>_PurchaseProof_<YYYY-MM-DD>.json`
   - Example: `submissions/Arjun_A_PurchaseProof_2026-09-28.json`
3. Fill:
   - `fellow` = exact `fellows.csv` name (e.g. `Arjun A`)
   - `github` = your GitHub username / profile URL (must map to the fellow above)
   - `type` = `PurchaseProof`
   - `title` = e.g. `Axon Lite kit proof`
   - `link` = `https://...` to your board photo / invoice / unboxing pic (must start with http:// or https://)
   - `date` = `YYYY-MM-DD`
4. Open a PR titled `[PurchaseProof] Your Name`. PR body must contain the link.
5. Maintainer merges → your Kit flips to `YES`. Close without merge = reject (fix and resubmit).

## After proof is accepted
Only after your PurchaseProof PR is merged will regular submissions be accepted:
- Blog / Linkedin / X / Project / Workshop / Documentation / Video / Community / Bug / Feature / Referral / Demo
- One submission = one JSON file = one PR, e.g. `submissions/Arjun_A_Blog_2026-09-28.json` with PR title `[Blog] Arjun A — https://...`

> If your first PR is not the purchase proof, it will be closed / not accepted. Submit the PurchaseProof PR first, then resubmit the others.

## Admin (accept / reject)
- Triage `PurchaseProof` PRs first. Check: `fellow` in `fellows.csv`? `link` opens and looks genuine (board / invoice / unboxing)?
- Accept: merge the PurchaseProof PR → Kit flips to `YES` via scorer. Then regular PRs from that fellow can be reviewed / merged.
- Reject: close with reason (no proof / name not in list / bad link). No points. If a fellow opens a non-proof PR before proof is merged, close it as not accepted and ask for PurchaseProof first.
