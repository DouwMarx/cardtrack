"""Derived layer: rebuilding text and fingerprints from the raw store, and the guard
that stops the monitor from minting junk when the layer is stale."""

from __future__ import annotations

import pytest
import yaml

from cardtrack.db import connect
from cardtrack.derived import (
    DerivedLayerStale,
    check_derived_layer,
    recompute_fingerprints,
    reextract_all,
)
from cardtrack.monitor import run_monitor
from cardtrack.propose import process_proposal
from cardtrack.repo import Repo

from .conftest import make_proposal


def seed(repo, server, path, body, **overrides):
    server.set_html(path, body)
    result = process_proposal(repo, make_proposal(server, path=path, **overrides), "seed")
    assert result.status == "written"
    return result


def versions_of(repo, document_id):
    conn = connect(repo.db_path)
    try:
        return conn.execute(
            "SELECT id, content_fingerprint, text_path FROM document_versions "
            "WHERE document_id=? ORDER BY id", (document_id,)).fetchall()
    finally:
        conn.close()


def set_ignore_patterns(repo, patterns):
    path = repo.root / "config" / "settings.yaml"
    settings = yaml.safe_load(path.read_text())
    settings["fingerprint"] = {"ignore_line_patterns": patterns}
    path.write_text(yaml.safe_dump(settings))
    return Repo.locate(repo.root)


def test_reextract_dry_run_writes_nothing_and_apply_rewrites_text(repo, http_server):
    added = seed(repo, http_server, "/doc", "Original body of the document.",
                 model_names=["ReextractModel"])
    (v,) = versions_of(repo, added.document_id)
    text_file = repo.root / v["text_path"]
    good = text_file.read_text()
    text_file.write_text("corrupted derived text")  # a stale or broken extraction

    dry = reextract_all(repo, apply=False)
    assert dry["status"] == "dry_run"
    assert dry["text_changed"] == 1 and dry["changed_version_ids"] == [v["id"]]
    assert text_file.read_text() == "corrupted derived text"

    applied = reextract_all(repo, apply=True)
    assert applied["text_changed"] == 1
    assert text_file.read_text() == good
    assert applied["fingerprints"]["status"] == "applied"
    (v2,) = versions_of(repo, added.document_id)
    assert v2["content_fingerprint"] == v["content_fingerprint"]


def test_stale_derived_layer_blocks_monitor_until_recomputed(repo, http_server):
    added = seed(repo, http_server, "/doc", "Stable body.</p><p>Downloads last month 12",
                 model_names=["GuardModel"])
    run_monitor(repo, "r0")  # bootstraps the derived-layer stamp on a fresh DB
    http_server.set_html("/doc", "Stable body.</p><p>Downloads last month 99")
    run_monitor(repo, "r1")
    assert len(versions_of(repo, added.document_id)) == 2  # counter churn minted a version

    stale_repo = set_ignore_patterns(repo, ["^Downloads last month"])
    with pytest.raises(DerivedLayerStale):
        run_monitor(stale_repo, "r2")
    conn = connect(stale_repo.db_path)
    try:
        with pytest.raises(DerivedLayerStale):
            check_derived_layer(conn, stale_repo)
    finally:
        conn.close()

    summary = recompute_fingerprints(stale_repo, apply=True)
    assert summary["pruned"] == 1
    assert len(versions_of(repo, added.document_id)) == 1  # the churn version is gone
    summary = run_monitor(stale_repo, "r3")  # runs again, and the counter no longer mints
    assert summary["new_versions"] == 0
