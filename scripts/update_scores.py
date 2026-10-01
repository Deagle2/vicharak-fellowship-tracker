"""Vicharak Fellowship scorer.
Reads fellows.csv + points.json + submissions/*.json
Writes allocations/<Fellow>.csv (screenshot layout), allocations/summary.csv, fellowship_scores.pdf
Idempotent, stdlib-only (reportlab optional for PDF).
Run: python scripts/update_scores.py (from repo root)
"""
import csv, json, re, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
FELLOWS_CSV = ROOT / "fellows.csv"
POINTS_JSON = ROOT / "points.json"
SUB_DIR = ROOT / "submissions"
ALLOC_DIR = ROOT / "allocations"
SUMMARY_CSV = ALLOC_DIR / "summary.csv"
PDF_OUT = ROOT / "fellowship_scores.pdf"
SCORES_MD = ROOT / "SCORES.md"
README_MD = ROOT / "README.md"
GITHUB_MAP_JSON = ROOT / "github_map.json"
GITHUB_OVERRIDES_JSON = ROOT / "github_overrides.json"

# Screenshot rows: keep exactly these 5 + Total. Project alias displays as Github.
SCREENSHOT_ROWS = ["Github", "Linkedin", "Blog", "X", "Workshop"]
CANONICAL_FOR_ROW = {"Github": "Project", "Linkedin": "Linkedin", "Blog": "Blog", "X": "X", "Workshop": "Workshop"}

def load_points():
    data = json.loads(POINTS_JSON.read_text(encoding="utf-8"))
    aliases = {k.lower(): v for k, v in data.get("_aliases", {}).items()}
    threshold = data.get("_threshold", 250)
    points = {k: v for k, v in data.items() if not k.startswith("_")}
    return points, aliases, threshold

def canon_type(raw, points, aliases):
    if not raw:
        return None
    r = raw.strip()
    if r in points:
        return r
    low = r.lower()
    if low in aliases:
        return aliases[low]
    if "github" in low or "project" in low:
        return "Project"
    if "linked" in low:
        return "Linkedin"
    if low in ("x", "twitter"):
        return "X"
    if "blog" in low:
        return "Blog"
    if "workshop" in low:
        return "Workshop"
    if "purchase" in low or "kit" in low or low == "proof":
        return "PurchaseProof"
    return None

def safe_name(n):
    s = re.sub(r"[^\w\-]+", "_", n.strip()).strip("_")
    return s or "Unknown"

def load_fellows():
    fellows = {}  # lower -> canonical display name
    meta = {}
    with open(FELLOWS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("Full name") or "").strip()
            if not name:
                continue
            key = re.sub(r"\s+", " ", name).lower()
            if key not in fellows:
                fellows[key] = re.sub(r"\s+", " ", name).strip()
                meta[key] = row
    return fellows, meta

def parse_github_usernames(raw):
    """Extract github.com usernames from a URL field (handles comma/space separated, www., /repo suffix)."""
    users = []
    for part in re.split(r"[,;\s]+", raw or ""):
        part = part.strip().strip("<>").rstrip("/")
        if not part:
            continue
        if part.startswith("@"):
            part = part[1:]
        m = re.search(r"github\.com/([A-Za-z0-9-]+)", part, re.IGNORECASE)
        if m:
            users.append(m.group(1).lower())
        elif re.fullmatch(r"[A-Za-z0-9-]{1,39}", part):
            users.append(part.lower())
    # de-dupe, preserve order
    seen, out = set(), []
    for u in users:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def load_github_map(meta, fellows):
    """Map github username (lower) -> fellow key. Base = fellows.csv Github column, overrides win."""
    gmap = {}
    for fkey, row in meta.items():
        for u in parse_github_usernames(row.get("Github") or ""):
            gmap.setdefault(u, fkey)
    try:
        ov = json.loads(GITHUB_OVERRIDES_JSON.read_text(encoding="utf-8"))
        for user, name in (ov or {}).items():
            if str(user).startswith("_") or str(user) == "example_user_do_not_use":
                continue
            key = re.sub(r"\s+", " ", str(name)).lower()
            if key not in fellows:
                print(f"WARNING: github_overrides.json name '{name}' not in fellows.csv - skipped", file=sys.stderr)
                continue
            gmap[str(user).strip().lstrip("@").lower()] = key
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"WARNING: ignoring bad github_overrides.json ({e})", file=sys.stderr)
    return gmap

def main():
    points, aliases, threshold = load_points()
    thresh_col = f"Threshold_{threshold}"
    fellows, meta = load_fellows()
    gmap = load_github_map(meta, fellows)  # github username -> fellow key (sheet + overrides)
    observed = {k: set() for k in fellows}  # github usernames seen in accepted submissions
    unmapped = {}  # github username -> set of files (not in sheet/overrides yet)
    # fellow_key -> {canon_type -> [(link,title,date,srcfile)]}
    store = {k: {} for k in fellows}
    errors = []
    files = sorted(SUB_DIR.glob("*.json"))
    files = [p for p in files if p.name not in ("TEMPLATE.json", "INDEX.json")]
    for p in files:
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{p.name}: invalid JSON ({e})")
            continue
        fellow_raw = str(obj.get("fellow", "")).strip()
        type_raw = str(obj.get("type", "")).strip()
        link = str(obj.get("link", "")).strip()
        title = str(obj.get("title", "")).strip()
        date = str(obj.get("date", "")).strip()
        if not fellow_raw:
            errors.append(f"{p.name}: missing fellow")
            continue
        fkey = re.sub(r"\s+", " ", fellow_raw).lower()
        if fkey not in fellows:
            errors.append(f"{p.name}: fellow '{fellow_raw}' not in fellows.csv")
            continue
        ctype = canon_type(type_raw, points, aliases)
        if not ctype:
            errors.append(f"{p.name}: unknown type '{type_raw}'")
            continue
        if not (link.startswith("http://") or link.startswith("https://")):
            errors.append(f"{p.name}: link must start with http(s)://")
            continue
        # attribution: optional `github` field (username or URL) must belong to the same fellow;
        # points always go to `fellow` (the associated name), never to the raw GitHub account.
        gh_users = parse_github_usernames(str(obj.get("github", "") or ""))
        bad = next((u for u in gh_users if gmap.get(u) is not None and gmap[u] != fkey), None)
        if bad is not None:
            errors.append(f"{p.name}: github @{bad} belongs to '{fellows[gmap[bad]]}' but fellow is '{fellows[fkey]}' - points go to the `fellow` name")
            continue
        for u in gh_users:
            if u in gmap:
                observed[fkey].add(u)
            else:
                unmapped.setdefault(u, set()).add(p.name)
        store[fkey].setdefault(ctype, []).append({"link": link, "title": title, "date": date, "file": p.name})

    # de-dupe links per fellow+type (keep first)
    for fkey, d in store.items():
        for ctype, items in d.items():
            seen = set()
            uniq = []
            for it in sorted(items, key=lambda x: (x["date"], x["file"])):
                if it["link"] not in seen:
                    seen.add(it["link"])
                    uniq.append(it)
            d[ctype] = uniq

    ALLOC_DIR.mkdir(exist_ok=True)
    # Determine max submissions in screenshot categories for column width (min 5 to match screenshot)
    max_n = 5
    for d in store.values():
        for row_label, ctype in CANONICAL_FOR_ROW.items():
            max_n = max(max_n, len(d.get(ctype, [])))
    headers = [""] + [f"Submission {i+1}" for i in range(max_n)] + ["Points"]

    # display accounts per fellow: sheet usernames + ones seen in accepted submissions
    base_users = {}
    for fkey, row in meta.items():
        base_users[fkey] = parse_github_usernames(row.get("Github") or "")
    gh_display = {}
    for fkey in fellows:
        combo, seen = [], set()
        for u in base_users.get(fkey, []) + sorted(observed.get(fkey, set())):
            if u not in seen:
                seen.add(u)
                combo.append("@" + u)
        gh_display[fkey] = " ".join(combo) if combo else "-"
    # persist resolved map (username -> Fellow) for the PR-attribution workflow + admin review
    GITHUB_MAP_JSON.write_text(json.dumps({u: fellows[k] for u, k in sorted(gmap.items())}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # drop orphan per-fellow sheets left from removed fellows
    valid_safe = {safe_name(v) for v in fellows.values()}
    for p in ALLOC_DIR.glob("*.csv"):
        if p.stem not in valid_safe and p.name != "summary.csv":
            p.unlink()
            print(f"removed orphan allocation: {p.name}")

    summary_rows = []
    for fkey in sorted(store, key=lambda k: fellows[k].lower()):
        display = fellows[fkey]
        d = store[fkey]
        total = 0
        per_row_points = {}
        for row_label, ctype in CANONICAL_FOR_ROW.items():
            items = d.get(ctype, [])
            pts = len(items) * points.get(ctype, 0)
            per_row_points[row_label] = (items, pts)
            total += pts
        # other types (outside screenshot rows) still count (PurchaseProof is a 0-pt gate, tracked separately)
        other_count = 0
        other_pts = 0
        for ctype, items in d.items():
            if ctype not in CANONICAL_FOR_ROW.values() and ctype != "PurchaseProof":
                other_count += len(items)
                p = len(items) * points.get(ctype, 0)
                other_pts += p
                total += p
        # write per-fellow csv (screenshot layout)
        out = ALLOC_DIR / f"{safe_name(display)}.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerow(["Names", display] + [""] * (max_n - 1) + [""])
            for row_label in SCREENSHOT_ROWS:
                items, pts = per_row_points[row_label]
                links = [it["link"] for it in items]
                links += [""] * (max_n - len(links))
                w.writerow([row_label] + links + [pts])
            proofs = d.get("PurchaseProof", [])
            plinks = [it["link"] for it in proofs][:max_n]
            plinks += [""] * (max_n - len(plinks))
            w.writerow(["KitProof"] + plinks + ["SUBMITTED" if proofs else "-"])
            w.writerow(["Total"] + [""] * max_n + [total])
        # summary
        def cnt(t):
            return len(d.get(t, []))
        summary_rows.append({
            "Fellow": display,
            "Github": gh_display[fkey],
            "PurchaseProof": "YES" if d.get("PurchaseProof") else "NO",
            "Github(Project)_count": cnt("Project"),
            "Linkedin_count": cnt("Linkedin"),
            "Blog_count": cnt("Blog"),
            "X_count": cnt("X"),
            "Workshop_count": cnt("Workshop"),
            "Other_count": other_count,
            "Total_Points": total,
            thresh_col: "ELIGIBLE" if total >= threshold else "BELOW",
        })

    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        fields = ["Fellow", "Github", "PurchaseProof", "Github(Project)_count", "Linkedin_count", "Blog_count", "X_count", "Workshop_count", "Other_count", "Total_Points", thresh_col]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary_rows)

    # SCORES.md + README leaderboard block (below Admin) — sorted by Total desc
    ranked = sorted(summary_rows, key=lambda r: (-r["Total_Points"], r["Fellow"].lower()))
    lines = [f"# Fellowship Scores - {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC",
             "", f"Threshold: {threshold} (ELIGIBLE >= {threshold})",
             "", "| Rank | Fellow | GitHub | Kit | Project | LinkedIn | Blog | X | Workshop | Other | Total | Status |",
             "|---:|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(ranked, 1):
        # only show non-zero OR top 30 to keep README readable? show all with points, collapse zeros
        lines.append(f"| {i} | {r['Fellow']} | {r['Github']} | {r['PurchaseProof']} | {r['Github(Project)_count']} | {r['Linkedin_count']} | {r['Blog_count']} | {r['X_count']} | {r['Workshop_count']} | {r['Other_count']} | **{r['Total_Points']}** | {r[thresh_col]} |")
    lines += ["", f"_Source: allocations/summary.csv - {len(ranked)} fellows - Points: " + ", ".join(f"{k}={v}" for k, v in points.items())]
    SCORES_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Patch README block between SCORES_START/END (show top 20 + link to full)
    try:
        top = ranked[:20]
        table = ["| Rank | Fellow | GitHub | Kit | Total | Status |", "|---:|---|---|---|---:|---|"]
        for i, r in enumerate(top, 1):
            table.append(f"| {i} | {r['Fellow']} | {r['Github']} | {r['PurchaseProof']} | **{r['Total_Points']}** | {r[thresh_col]} |")
        block = (f"_Updated {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC - Threshold {threshold} - {len([r for r in ranked if r['Total_Points']>0])}/{len(ranked)} with points_\n\n"
                 + "\n".join(table) + f"\n\n_Showing top 20 of {len(ranked)} - full list in [SCORES.md](SCORES.md)_")
        txt = README_MD.read_text(encoding="utf-8")
        pat = re.compile(r"<!-- SCORES_START -->.*?<!-- SCORES_END -->", re.DOTALL)
        repl = f"<!-- SCORES_START -->\n{block}\n<!-- SCORES_END -->"
        if "<!-- SCORES_START -->" in txt:
            txt = pat.sub(repl, txt)
            README_MD.write_text(txt, encoding="utf-8")
            print(f"README leaderboard updated: {README_MD}")
        print(f"SCORES.md written: {len(ranked)} fellows")
    except Exception as e:
        print(f"Leaderboard update failed: {e}", file=sys.stderr)

    # submissions/INDEX.json + INDEX.md — all submissions grouped under a single fellow name
    try:
        index = {}
        for fkey in sorted(store, key=lambda k: fellows[k].lower()):
            d = store[fkey]
            items = []
            for ctype in sorted(d):
                for it in sorted(d[ctype], key=lambda x: (x["date"], x["file"])):
                    items.append({"type": ctype,
                                  "points": points.get(ctype, 0),
                                  "title": it["title"],
                                  "link": it["link"],
                                  "date": it["date"],
                                  "file": it["file"]})
            if items:
                index[fellows[fkey]] = items
        (SUB_DIR / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        md = [f"# Submissions by Fellow - {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC", "",
              f"_Total: {sum(len(v) for v in index.values())} accepted submissions across {len(index)}/{len(fellows)} fellows_"]
        if not index:
            md += ["", "_No accepted submissions yet. Submit via PR (see README in this folder)._"]
        for name in sorted(index, key=str.lower):
            items = index[name]
            total_pts = sum(i["points"] for i in items)
            md += ["", f"## {name} - {len(items)} submission(s), {total_pts} pts"]
            for it in items:
                md.append(f"- [{it['type']}] {it['title']} ({it['date']}) - {it['link']} - {it['points']} pts - `{it['file']}`")
        (SUB_DIR / "INDEX.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"submissions/INDEX.json + INDEX.md written: {len(index)} fellows with submissions")
    except Exception as e:
        print(f"INDEX generation failed: {e}", file=sys.stderr)

    # PDF (optional reportlab, else simple text-based fallback skipped)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(str(PDF_OUT), pagesize=A4, title="Vicharak Fellowship Scores")
        els = [Paragraph("Vicharak Campus Fellowship — Scores & Accepted Links", styles["Title"]),
               Paragraph(f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | Threshold {threshold} | Points: " +
                         ", ".join(f"{k}={v}" for k, v in points.items()), styles["Normal"]), Spacer(1, 12)]
        # summary table
        data = [["Fellow (GitHub)", "Kit", "GitHub", "LinkedIn", "Blog", "X", "Workshop", "Other", "Total", "Status"]]
        for r in summary_rows:
            who = r["Fellow"] + (f" ({r['Github']})" if r["Github"] != "-" else "")
            data.append([who, r["PurchaseProof"], r["Github(Project)_count"], r["Linkedin_count"], r["Blog_count"], r["X_count"], r["Workshop_count"], r["Other_count"], r["Total_Points"], r[thresh_col]])
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                               ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                               ("FONTSIZE", (0, 0), (-1, -1), 7)]))
        els += [t, Spacer(1, 12), Paragraph("Accepted links per fellow (from merged PRs):", styles["Heading2"])]
        for fkey in sorted(store, key=lambda k: fellows[k].lower()):
            d = store[fkey]
            if not any(d.values()):
                continue
            els.append(Paragraph(f"<b>{fellows[fkey]}</b>", styles["Heading3"]))
            rows = [["Type", "Title", "Link", "Pts"]]
            for ctype in sorted(d):
                for it in d[ctype]:
                    rows.append([ctype, it["title"][:60], it["link"][:80], points.get(ctype, 0)])
            lt = Table(rows, repeatRows=1, colWidths=[60, 140, 220, 30])
            lt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2ff")),
                                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                                    ("FONTSIZE", (0, 0), (-1, -1), 7)]))
            els += [lt, Spacer(1, 8)]
        doc.build(els)
        print(f"PDF written: {PDF_OUT}")
    except ImportError:
        print("reportlab not installed — skipping PDF (pip install reportlab to enable).", file=sys.stderr)
    except Exception as e:
        print(f"PDF generation failed: {e}", file=sys.stderr)

    print(f"Fellows: {len(fellows)}, submission files: {len(files)}, github accounts mapped: {len(gmap)}, allocations -> {ALLOC_DIR}")
    if unmapped:
        print("UNMAPPED github accounts (add to github_overrides.json if valid):")
        for u in sorted(unmapped):
            print(f" - @{u} in {', '.join(sorted(unmapped[u]))}")
    if errors:
        print("ERRORS (fix these files):")
        for e in errors:
            print(" -", e)
        # fail CI so bad PRs are visible, but still wrote what was valid
        sys.exit(2)

if __name__ == "__main__":
    main()
