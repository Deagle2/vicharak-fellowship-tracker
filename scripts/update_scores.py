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
    # fuzzy: project repo -> Project, github -> Project
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

def main():
    points, aliases, threshold = load_points()
    fellows, meta = load_fellows()
    # fellow_key -> {canon_type -> [(link,title,date,srcfile)]}
    store = {k: {} for k in fellows}
    errors = []
    files = sorted(SUB_DIR.glob("*.json"))
    files = [p for p in files if p.name != "TEMPLATE.json"]
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
        # other types (outside screenshot rows) still count
        other_count = 0
        other_pts = 0
        for ctype, items in d.items():
            if ctype not in CANONICAL_FOR_ROW.values():
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
            w.writerow(["Total"] + [""] * max_n + [total])
        # summary
        def cnt(t):
            return len(d.get(t, []))
        summary_rows.append({
            "Fellow": display,
            "Github(Project)_count": cnt("Project"),
            "Linkedin_count": cnt("Linkedin"),
            "Blog_count": cnt("Blog"),
            "X_count": cnt("X"),
            "Workshop_count": cnt("Workshop"),
            "Other_count": other_count,
            "Total_Points": total,
            "Threshold_250": "ELIGIBLE" if total >= threshold else "BELOW",
        })

    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        fields = ["Fellow", "Github(Project)_count", "Linkedin_count", "Blog_count", "X_count", "Workshop_count", "Other_count", "Total_Points", "Threshold_250"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(summary_rows)

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
        data = [["Fellow", "GitHub", "LinkedIn", "Blog", "X", "Workshop", "Other", "Total", "Status"]]
        for r in summary_rows:
            data.append([r["Fellow"], r["Github(Project)_count"], r["Linkedin_count"], r["Blog_count"], r["X_count"], r["Workshop_count"], r["Other_count"], r["Total_Points"], r["Threshold_250"]])
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

    print(f"Fellows: {len(fellows)}, submission files: {len(files)}, allocations -> {ALLOC_DIR}")
    if errors:
        print("ERRORS (fix these files):")
        for e in errors:
            print(" -", e)
        # fail CI so bad PRs are visible, but still wrote what was valid
        sys.exit(2)

if __name__ == "__main__":
    main()
