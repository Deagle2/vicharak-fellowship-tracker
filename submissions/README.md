# Submissions — how to submit

1. Copy `TEMPLATE.json` to a new file named: `<Your-Full-Name-With-Underscores>_<Type>_<YYYY-MM-DD>.json`
   - Name must match `fellows.csv` (case-insensitive), e.g. `Arjun_A`.
   - Type must be one of: Blog, Linkedin, X, Project, Workshop, Documentation, Video, Community, Bug, Feature, Referral, Demo.
2. Fill all 5 fields. Link must start with http:// or https://.
3. Open a Pull Request. PR title format (important):
   `[Blog] Your Name — short title + link`
   Valid prefixes: `[Blog]` `[Linkedin]` `[X]` `[Project]` `[Workshop]` `[Documentation]` `[Video]` `[Community]` `[Bug]` `[Feature]` `[Referral]` `[Demo]`
4. One submission = one JSON file = one PR (easier to accept/reject). Do not bundle multiple links in one file.
5. If maintainer merges, points auto-allocate. If closed, no points.

## Single-name listing (auto-generated)
- [`INDEX.md`](INDEX.md) — all accepted submissions grouped under a single fellow name (`## Name - N submission(s), P pts` + bullet per link). Start here to browse.
- [`INDEX.json`](INDEX.json) — same data, machine-readable (`{ "Fellow Name": [{type, points, title, link, date, file}] }`).
- Both regenerate on every merge. Do not hand-edit (overwritten). Ignored as input by the scorer.

Example file: `Arjun_A_Blog_2026-09-28.json`
```json
{
  "fellow": "Arjun A",
  "type": "Blog",
  "title": "My Axon Lite build log",
  "link": "https://medium.com/@arjun/my-axon-build",
  "date": "2026-09-28"
}
```
