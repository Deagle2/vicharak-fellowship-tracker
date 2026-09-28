"""Validate a join-request issue body against fellows.csv.
Usage: python scripts/validate_join.py --body BODY.md --fellows fellows.csv --author ISSUE_AUTHOR_LOGIN
Prints JSON to stdout + human markdown to STDOUT? Writes outputs for Actions.
Exit 0 always (result encoded in JSON), unless fatal.
"""
import argparse, csv, json, re, sys
from pathlib import Path

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def parse_fields(body):
    # GitHub issue forms render as "### Field\n\nvalue\n\n"
    fields = {}
    # split on ### headers
    parts = re.split(r"^###\s+(.+)\s*$", body, flags=re.MULTILINE)
    # parts[0] preamble, then pairs header,value
    for i in range(1, len(parts), 2):
        h = parts[i].strip().lower()
        v = parts[i+1].strip() if i+1 < len(parts) else ""
        # strip HTML comments / "_No response_" placeholders
        if v == "_No response_":
            v = ""
        fields[h] = v
    return fields

def find_field(fields, *keys):
    for k in keys:
        for h, v in fields.items():
            if k in h:
                return v
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--body", required=True)
    ap.add_argument("--fellows", default="fellows.csv")
    ap.add_argument("--author", default="")
    args = ap.parse_args()
    body = Path(args.body).read_text(encoding="utf-8-sig", errors="ignore")
    fields = parse_fields(body)
    full_name = find_field(fields, "full name")
    gh_user = find_field(fields, "github username")
    email = find_field(fields, "email")
    proof = find_field(fields, "purchase proof")
    # load fellows
    fellows = {}
    try:
        with open(args.fellows, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                n = (row.get("Full name") or "").strip()
                if n:
                    fellows[norm(n)] = re.sub(r"\s+", " ", n).strip()
    except FileNotFoundError:
        print(json.dumps({"ok": False, "reason": "fellows.csv missing"}))
        return
    checks = {}
    # 1. name exists
    key = norm(full_name)
    checks["name_present"] = bool(full_name)
    checks["name_in_list"] = key in fellows if key else False
    # 2. proof attached? look for image markdown or user-attachments or file exts
    has_img_md = bool(re.search(r"!\[.*?\]\(.*?\)", body))
    has_attach = "user-attachments" in body or "github.com/user-attachments" in body
    has_file_ext = bool(re.search(r"\.(png|jpe?g|pdf|webp|heic)(\?.*?)?(\)|\s|$)", body, re.IGNORECASE))
    checks["proof_attached"] = bool(has_img_md or has_attach or (has_file_ext and len(proof) > 10))
    # 3. filename contains name? best-effort: look for alt-text / filenames with name tokens
    tokens = [t for t in re.split(r"\W+", full_name.lower()) if len(t) >= 3]
    proof_blob = (proof + "\n" + body).lower()
    checks["filename_matches"] = any(t in proof_blob for t in tokens) if tokens else False
    # 4. author matches declared username?
    checks["author_matches"] = (args.author.lower() == gh_user.strip().lower().lstrip("@")) if gh_user and args.author else None
    ok = bool(checks["name_in_list"] and checks["proof_attached"])
    # build comment
    status = "VALID - ready for admin review" if ok else "NEEDS FIX"
    lines = [f"### Join check: {status}", "",
             f"- Full name: `{full_name or '(missing)'}` - in fellows.csv: **{'YES' if checks['name_in_list'] else 'NO'}**",
             f"- Purchase proof attached: **{'YES' if checks['proof_attached'] else 'NO'}** (need board photo / invoice renamed `<Name>_proof.png`)"]
    if tokens:
        lines.append(f"- Filename contains name: **{'YES' if checks['filename_matches'] else 'NO - please rename before re-upload'}**")
    if checks["author_matches"] is False:
        lines.append(f"- WARNING: issue author `@{args.author}` != declared username `{gh_user}` - will invite issue author only.")
    if email:
        lines.append(f"- Email: `{email}`")
    if not checks["name_in_list"]:
        lines.append("- Fix: use exact name from `fellows.csv` / Fellowship program sheet. Admin cannot approve unknown names.")
    if not checks["proof_attached"]:
        lines.append("- Fix: edit this issue and drag-drop your proof image into the Purchase proof field.")
    if ok:
        lines += ["", "Admin: add label `approved` to invite, or comment `/approve`. Close as not planned to reject."]
    else:
        lines += ["", "Bot labels: `join-invalid`. Edit the issue to fix - bot re-checks on edit."]
    print(json.dumps({"ok": ok, "full_name": full_name, "gh_user": gh_user, "author": args.author, "checks": checks, "comment": "\n".join(lines)}))

if __name__ == "__main__":
    main()
