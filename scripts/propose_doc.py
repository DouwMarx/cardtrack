#!/usr/bin/env python3
"""THE write path: validate + upsert. The only mutation route, for agent
and human alike. Prints one JSON result line; exit 0 = proposal processed (see
"status" field for the outcome), exit 2 = invocation error.

Usage:
  propose_doc.py --json -              # proposal record on stdin
  propose_doc.py --json proposal.json
  propose_doc.py --action add --url https://… --title … --publisher anthropic \
      --doc-type system_card --model "Claude Fable 5" --publication-date 2026-08-01 \
      --justification "…" --evidence-url https://… --source-of-lead manual \
      --attest primary_source --attest about_a_specific_model_or_eval
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cardtrack.propose import process_proposal  # noqa: E402
from cardtrack.repo import Repo  # noqa: E402


def default_run_id() -> str:
    return "manual-" + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", help="repo root (default: auto-detected)")
    p.add_argument("--run-id", default=None,
                   help="run id for changelog grouping (default: $CARDTRACK_RUN_ID, "
                        "else a timestamp). Caps do NOT depend on it: they are "
                        "enforced over a rolling window inside the validator.")
    p.add_argument("--actor", default=None,
                   help="who is proposing (default: $CARDTRACK_ACTOR, else 'human')")
    p.add_argument("--json", dest="json_src",
                   help="proposal record as JSON: a file path, or '-' for stdin")
    # flag-based construction
    p.add_argument("--action", choices=["add", "new_version", "status_change",
                                        "field_update", "annotate_version"])
    p.add_argument("--url")
    p.add_argument("--title")
    p.add_argument("--publisher")
    p.add_argument("--doc-type", dest="doc_type")
    p.add_argument("--model", action="append", default=[], dest="models",
                   help="repeatable: model name covered by the document")
    p.add_argument("--publication-date", dest="publication_date")
    p.add_argument("--justification")
    p.add_argument("--evidence-url", action="append", default=[], dest="evidence_urls")
    p.add_argument("--source-of-lead", dest="source_of_lead", default="manual")
    p.add_argument("--notes")
    p.add_argument("--attest", action="append", default=[], dest="attested",
                   help="repeatable: agent_attested criterion asserted true")
    p.add_argument("--safety-evals", dest="safety_evals", choices=["yes", "no"],
                   help="required for adds: whether the document contains safety "
                        "or dangerous-capability evals")
    p.add_argument("--openness", help="restricted | closed | open_weight_restrictive "
                                      "| open_weight_permissive")
    p.add_argument("--risk-domain", action="append", default=[], dest="risk_domains",
                   help="repeatable: risk domain tag (see config/criteria.yaml)")
    p.add_argument("--version-id", dest="version_id", type=int,
                   help="target version (annotate_version)")
    p.add_argument("--summary", help="what changed vs the previous version "
                                     "(annotate_version; plain text, <=500 chars)")
    p.add_argument("--content-file",
                   help="operator-supplied document bytes for bot-walled/offline "
                        "sources; recorded as transport=manual_upload. Human use "
                        "only — refused inside the agent sandbox.")
    p.add_argument("--content-type", help="content type hint for --content-file")
    p.add_argument("--override-duplicate-review", action="store_true",
                   help="operator adjudication of a needs-review issue: admit an add "
                        "that would otherwise file a content/logical-duplicate issue "
                        "(e.g. a co-published copy, or a distinct doc with a similar "
                        "title). Human use only — refused inside the agent sandbox.")
    p.add_argument("--slug", help="target document (status_change / field_update)")
    p.add_argument("--field", help="field to update (field_update)")
    p.add_argument("--old", help="expected current value (field_update, JSON or string)")
    p.add_argument("--new", help="new value (status_change: status; field_update: JSON or string)")
    return p


def _parse_json_or_string(value: str):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def proposal_from_args(args: argparse.Namespace) -> dict:
    if not args.action:
        raise SystemExit("either --json or --action is required (see --help)")
    proposal: dict = {"action": args.action}
    if args.url:
        proposal["url"] = args.url
    if args.title:
        proposal["title"] = args.title
    if args.publisher:
        proposal["publisher"] = args.publisher
    if args.doc_type:
        proposal["doc_type"] = args.doc_type
    if args.action == "add":
        proposal["model_names"] = args.models
        proposal["publication_date"] = args.publication_date
        proposal["criteria"] = {k: True for k in args.attested}
        if args.safety_evals:
            proposal["soft"] = {"has_safety_evals": args.safety_evals == "yes"}
        if args.openness:
            proposal["openness"] = args.openness
        if args.risk_domains:
            proposal["risk_domains"] = args.risk_domains
    if args.action == "annotate_version":
        proposal["version_id"] = args.version_id
        proposal["summary"] = args.summary
    if args.notes:
        proposal["notes"] = args.notes
    if args.slug:
        proposal["slug"] = args.slug
    if args.field:
        proposal["field"] = args.field
    if args.old is not None:
        proposal["old"] = _parse_json_or_string(args.old)
    if args.new is not None:
        proposal["new"] = _parse_json_or_string(args.new)
    proposal["justification"] = args.justification or ""
    proposal["evidence_urls"] = args.evidence_urls
    proposal["source_of_lead"] = args.source_of_lead
    return proposal


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.json_src:
        raw = sys.stdin.read() if args.json_src == "-" else Path(args.json_src).read_text()
        try:
            proposal = json.loads(raw)
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "reason": f"invalid JSON: {e}"}))
            return 2
    else:
        try:
            proposal = proposal_from_args(args)
        except SystemExit as e:
            print(json.dumps({"status": "error", "reason": str(e)}))
            return 2

    repo = Repo.locate(args.root)
    run_id = args.run_id or os.environ.get("CARDTRACK_RUN_ID") or default_run_id()
    actor = args.actor or os.environ.get("CARDTRACK_ACTOR") or "human"
    local_content = local_content_type = None
    if args.content_file:
        if os.environ.get("CARDTRACK_SANDBOX") or actor == "agent":
            print(json.dumps({"status": "error",
                              "reason": "content-file ingestion is human-only "
                                        "(refused for sandboxed/agent callers)"}))
            return 2
        local_content = Path(args.content_file).read_bytes()
        local_content_type = args.content_type
    if args.override_duplicate_review and (os.environ.get("CARDTRACK_SANDBOX")
                                           or actor == "agent"):
        print(json.dumps({"status": "error",
                          "reason": "override-duplicate-review is human-only "
                                    "(refused for sandboxed/agent callers)"}))
        return 2
    result = process_proposal(repo, proposal, run_id=run_id, actor=actor,
                              local_content=local_content,
                              local_content_type=local_content_type,
                              override_review=args.override_duplicate_review)
    print(json.dumps(result.to_dict(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
