# Joining the repo (purchase proof gate)

Public repo, but **edit access is gated**: only Fellows with a Vicharak kit get in.

## Student (join)
1. Issues → New → `Request repo access (purchase proof)` (or click: Issues → New Issue → Join).
2. Fill:
   - Full name = exact `fellows.csv` name (e.g. `Arjun A`)
   - GitHub username = account opening the issue (invite goes to issue author only - anti-impersonation)
   - Email, College, Board + Order ID
   - Proof: **rename first** as `<Full-Name>_proof.png/jpg/pdf`, then drag-drop board photo / invoice screenshot / unboxing pic. Multiple OK.
3. Submit. Bot comments within ~30s:
   - `join-valid` = name found + proof seen → wait for admin
   - `join-invalid` = fix (usually name mismatch or missing image) → Edit issue, bot re-checks.
4. Admin adds `approved` label → bot invites you (`push` access). Accept invite via email / bell icon.

One issue per person. Do not open PRs to join.

## Admin (accept / reject)
- Triage `join-request` issues. Check: name in `fellows.csv`? Proof opens and looks genuine? Filename has their name?
- Accept: add label `approved` (bot re-validates, then invites issue author).
  - Needs repo secret `ONBOARD_PAT` (classic PAT, `repo` scope, from an admin) for full-auto invite. Without it, bot posts the one-line manual command - run it, then close issue as completed:
    ```
    gh api -X PUT repos/nilangwork17/vicharak-fellowship-tracker/collaborators/USERNAME -f permission=push
    ```
- Reject: close as not planned with reason (no proof / name not in list). No invite happens.
- Remove/revoke later: `gh api -X DELETE repos/.../collaborators/USERNAME` or Settings → Collaborators → Remove.

## Files
- Form: `.github/ISSUE_TEMPLATE/join-request.yml`
- Validator: `scripts/validate_join.py` (`--body BODY.md --fellows fellows.csv --author LOGIN`)
- Workflow: `.github/workflows/onboard.yml` (validate on open/edit, invite on `approved`)
- Test locally: `python scripts/validate_join.py --body /tmp/body.md --author testuser`
