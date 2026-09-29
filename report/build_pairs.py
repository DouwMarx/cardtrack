#!/usr/bin/env python3
"""Build version-to-version text diffs for every tracked document.

Reads the DB snapshot (data/docs.sqlite.snapshot) but the extracted text files live in
the cardtrack repo (data/text/<hash>.txt), so the repo path is required. Writes
pairs/diffs/<slug>-v<version>.diff, pairs/version_pairs.json (manifest) and
pairs/batches/batch_<i>.json (balanced batches for classification sub-agents).
Only pairs without an existing classification are put into batches, so re-running on a
grown database classifies just the new pairs.
"""
import argparse
import difflib
import json
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--batches", type=int, default=9)
    args = ap.parse_args()
    db = os.path.join(HERE, "data", "docs.sqlite.snapshot")
    out = os.path.join(HERE, "pairs")
    os.makedirs(os.path.join(out, "diffs"), exist_ok=True)
    os.makedirs(os.path.join(out, "batches"), exist_ok=True)
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row

    def q(s, *a):
        return [dict(r) for r in c.execute(s, a)]

    def read(path):
        if not path:
            return []
        p = path if os.path.isabs(path) else os.path.join(args.repo, path)
        return open(p, errors="replace").read().splitlines() if os.path.exists(p) else []

    manifest = []
    for d in q("SELECT id, slug, publisher, doc_type, title, canonical_url, status FROM documents"):
        vs = q("SELECT id, fetched_at, content_type, byte_size, text_path, change_summary "
               "FROM document_versions WHERE document_id=? ORDER BY fetched_at, id", d["id"])
        for a, b in zip(vs, vs[1:]):
            ta, tb = read(a["text_path"]), read(b["text_path"])
            diff = list(difflib.unified_diff(ta, tb, lineterm="", n=2))
            added = sum(1 for line in diff[2:] if line.startswith("+"))
            removed = sum(1 for line in diff[2:] if line.startswith("-"))
            p = os.path.join(out, "diffs", f"{d['slug']}-v{b['id']}.diff")
            with open(p, "w") as fh:
                fh.write("\n".join(diff))
            manifest.append(dict(
                slug=d["slug"], publisher=d["publisher"], doc_type=d["doc_type"],
                title=d["title"], url=d["canonical_url"], content_type=b["content_type"],
                prev_version=a["id"], version=b["id"], prev_fetched=a["fetched_at"],
                fetched=b["fetched_at"], prev_lines=len(ta), lines=len(tb), added=added,
                removed=removed, diff_lines=len(diff), diff_path=p,
                change_summary=b["change_summary"]))
    manifest.sort(key=lambda m: (m["slug"], m["version"]))
    json.dump(manifest, open(os.path.join(out, "version_pairs.json"), "w"), indent=1)

    # Existing classifications -> only batch the unclassified pairs.
    done = set()
    cdir = os.path.join(HERE, "classifications")
    for f in sorted(os.listdir(cdir)) if os.path.isdir(cdir) else []:
        if f.endswith(".json"):
            for r in json.load(open(os.path.join(cdir, f))):
                done.add((r["slug"], r["version"]))
    todo = [m for m in manifest if (m["slug"], m["version"]) not in done]
    groups: dict[str, list] = {}
    for m in todo:
        groups.setdefault(m["slug"], []).append(m)
    n = max(1, min(args.batches, len(groups)))
    batches: list[list] = [[] for _ in range(n)]
    load = [0] * n
    for _slug, ms in sorted(groups.items(), key=lambda kv: -sum(x["diff_lines"] for x in kv[1])):
        i = load.index(min(load))
        batches[i].extend(ms)
        load[i] += sum(min(x["diff_lines"], 1500) for x in ms)
    for f in os.listdir(os.path.join(out, "batches")):
        os.remove(os.path.join(out, "batches", f))
    for i, b in enumerate(batches):
        if b:
            json.dump(b, open(os.path.join(out, "batches", f"batch_{i}.json"), "w"), indent=1)
    print(f"pairs: {len(manifest)}  already classified: {len(manifest) - len(todo)}  "
          f"to classify: {len(todo)} in {sum(1 for b in batches if b)} batches")


if __name__ == "__main__":
    main()
