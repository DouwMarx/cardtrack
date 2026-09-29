#!/usr/bin/env python3
"""Build the public dataset files for the R2 bucket (scripts/backup.sh uploads them):

    <out>/manifest.json               every version: document, date, sha256, download URL
    <out>/urls.txt                    one download URL per line (`wget -i urls.txt`)
    <out>/withheld.txt                file names kept off the public bucket (for rclone)
    <out>/cardtrack-dataset.tar.gz    docs.sqlite + data/text/ + manifest.json + README.txt

The originals themselves are uploaded file by file under raw/, not in the tarball:
they change rarely, and a daily 0.5 GB archive would be re-uploaded for nothing.
"""

from __future__ import annotations

import argparse
import io
import json
import sqlite3
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.archive import manifest, withheld_hashes  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402

README = """cardtrack dataset ({site}), snapshot {ts}

docs.sqlite     the database: documents, versions, changelog, link checks
text/           extracted text per stored version (data/text/ in the repo)
manifest.json   every stored version with its sha256 and the URL of the original

Originals: {base}/raw/<sha256>.<ext>, listed in manifest.json and urls.txt.
Bulk download:  wget -i {base}/urls.txt
Verify a file:  sha256sum <file>   (must equal its "sha256" in manifest.json)

Originals are archived copies of publicly released documents, kept so that edits
and removals stay verifiable. Rights remain with their publishers. Removal
requests: {contact}. Code and data model: https://github.com/{repo}
"""


def build(repo: Repo, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    # Read-only, from a consistent copy: cardtrack.db.connect() rewrites views on
    # open, which left the committed docs.sqlite dirty after every backup, and a
    # dirty checkout makes deploy_update.sh refuse the next code update.
    snapshot = out / "docs.sqlite"
    src = sqlite3.connect(f"file:{repo.db_path}?mode=ro", uri=True)
    dst = sqlite3.connect(snapshot)
    try:
        src.backup(dst)
    finally:
        src.close()
        dst.close()
    conn = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        man = manifest(repo, conn)
    finally:
        conn.close()
    man_bytes = json.dumps(man, indent=1, ensure_ascii=False).encode()
    (out / "manifest.json").write_bytes(man_bytes)
    (out / "urls.txt").write_text(
        "".join(sorted({v["url"] + "\n" for v in man["versions"] if v["url"]})), encoding="utf-8")
    withheld = withheld_hashes(repo)
    (out / "withheld.txt").write_text(
        "".join(sorted({Path(v["file"]).name + "\n" for v in man["versions"]
                        if v["file"] and v["sha256"].lower() in withheld})), encoding="utf-8")

    readme = README.format(site=repo.setting("site.title", "cardtrack"),
                           ts=man["generated_at"], base=man["base_url"] or "<not published>",
                           contact=repo.setting("archive.contact", "the repository's issues"),
                           repo=repo.setting("github.repo", "")).encode()
    tar_path = out / "cardtrack-dataset.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(snapshot, arcname="cardtrack-dataset/docs.sqlite")
        if repo.text_dir.is_dir():
            tar.add(repo.text_dir, arcname="cardtrack-dataset/text")
        for name, data in (("manifest.json", man_bytes), ("README.txt", readme)):
            info = tarfile.TarInfo(f"cardtrack-dataset/{name}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return {"versions": man["counts"]["versions"], "withheld": man["counts"]["withheld"],
            "tarball_bytes": tar_path.stat().st_size}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--root")
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args(argv)
    print(json.dumps(build(Repo.locate(a.root), a.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
