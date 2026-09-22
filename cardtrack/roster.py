"""Roster sync: keep the publisher allowlist covering the labs that carry real
traffic, using OpenRouter's daily rankings dataset as the signal.

Design constraints (see config/roster.yaml for the policy knobs):
- ADDITIVE ONLY. Writes config/sources.generated.yaml, an overlay merged under
  the curated config/sources.yaml by Repo.sources. Base wins on collision; an
  author dropping out of the rankings never removes a publisher (removal is a
  human edit: `deny`, or `enabled: false`).
- FAIL CLOSED. Any fetch/schema/sanity failure leaves the previous overlay
  byte-identical and returns status "kept_previous". The daily run never blocks
  on this step.
- DETERMINISTIC. No LLM. The only judgement is the policy file.
"""

from __future__ import annotations

import collections
import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import requests
import yaml

from .repo import Repo, utcnow

OVERLAY_NAME = "sources.generated.yaml"
SNAPSHOT_NAME = "roster_openrouter.json"
FAILSTREAK_NAME = ".roster_failstreak"
API_KEY_ENV = "OPENROUTER_API_KEY"

_DEFAULT_GUARDS = {
    "min_days_in_window": 20,
    "min_authors": 5,
    "max_authors": 100,
    "failstreak_issue_after": 3,
}


# The only fields an overlay entry carries: membership and identity, nothing that
# moves day to day. Anything else in a previous overlay is dropped on carry-over.
_ENTRY_FIELDS = ("tier", "display_name", "origin", "openrouter_slug", "first_seen",
                 "index_urls", "scope", "homepage")


class RosterError(Exception):
    """A reason to keep the previous overlay. Message is human-readable."""


@dataclass
class AuthorStat:
    slug: str
    tokens: int
    days_present: int
    share: float = 0.0


# ---------------------------------------------------------------- inputs

def read_api_key(repo: Repo) -> str | None:
    """OPENROUTER_API_KEY from the environment, else parsed from <root>/.env.
    Phase A runs without sourcing .env (the agent sandbox masks it), so the
    roster step reads the one key it needs itself."""
    key = os.environ.get(API_KEY_ENV)
    if key:
        return key.strip()
    env_path = repo.root / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip().removeprefix("export ").strip() == API_KEY_ENV:
            return v.strip().strip('"').strip("'") or None
    return None


def fetch_rankings(endpoint: str, api_key: str, timeout: float) -> dict:
    try:
        r = requests.get(endpoint, headers={"Authorization": f"Bearer {api_key}"},
                         timeout=timeout)
    except requests.RequestException as e:
        raise RosterError(f"rankings fetch failed: {e.__class__.__name__}") from e
    if r.status_code != 200:
        raise RosterError(f"rankings fetch returned HTTP {r.status_code}")
    try:
        return r.json()
    except ValueError as e:
        raise RosterError("rankings response is not JSON") from e


def fetch_models(endpoint: str, timeout: float) -> dict[str, dict]:
    """Per-author identity hints from the public models list:
    {slug: {"display_name": str|None, "hf_org": str|None}}. Best effort — an
    empty dict just means overlay entries get slug-derived names and no index_urls."""
    try:
        r = requests.get(endpoint, timeout=timeout)
        if r.status_code != 200:
            return {}
        data = r.json().get("data") or []
    except (requests.RequestException, ValueError, AttributeError):
        return {}
    names: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    hf_orgs: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for m in data:
        if not isinstance(m, dict):
            continue
        mid = str(m.get("id") or "")
        if "/" not in mid:
            continue
        slug = mid.split("/", 1)[0]
        name = str(m.get("name") or "")
        if ": " in name:
            names[slug][name.split(": ", 1)[0].strip()] += 1
        hf = str(m.get("hugging_face_id") or "")
        if "/" in hf:
            hf_orgs[slug][hf.split("/", 1)[0]] += 1
    out: dict[str, dict] = {}
    for slug in set(names) | set(hf_orgs):
        out[slug] = {
            "display_name": names[slug].most_common(1)[0][0] if names[slug] else None,
            "hf_org": hf_orgs[slug].most_common(1)[0][0] if hf_orgs[slug] else None,
        }
    return out


# ---------------------------------------------------------------- pure logic

def validate_payload(payload: dict, guards: dict) -> list[dict]:
    """Schema + shape checks. Returns the row list or raises RosterError."""
    if not isinstance(payload, dict):
        raise RosterError("payload is not an object")
    meta = payload.get("meta") or {}
    if meta.get("version") != "v1":
        raise RosterError(f"unexpected dataset version {meta.get('version')!r} (expected 'v1')")
    rows = payload.get("data")
    if not isinstance(rows, list) or not rows:
        raise RosterError("payload has no data rows")
    for r in rows[:50]:
        if not {"date", "model_permaslug", "total_tokens"} <= set(r):
            raise RosterError("row schema changed (expected date/model_permaslug/total_tokens)")
    days = {r.get("date") for r in rows}
    min_days = int(guards.get("min_days_in_window", _DEFAULT_GUARDS["min_days_in_window"]))
    if len(days) < min_days:
        raise RosterError(f"only {len(days)} days in window (guard: >= {min_days})")
    return rows


def aggregate(rows: list[dict], policy: dict) -> tuple[list[AuthorStat], float]:
    """Token totals per author over the window, ignoring '~'-prefixed internal
    aliases and policy `ignore` slugs. Shares are of the ATTRIBUTABLE total (the
    dataset's 'other' bucket, everything outside each day's top 50, is excluded
    from the denominator). Returns (stats sorted by tokens desc, other_share of
    all tokens) so the coverage the cut really achieves stays visible."""
    ignore = set(policy.get("ignore") or [])
    tokens: collections.Counter = collections.Counter()
    days: dict[str, set] = collections.defaultdict(set)
    other = 0
    for r in rows:
        slug_full = str(r.get("model_permaslug") or "")
        try:
            t = int(r.get("total_tokens") or 0)
        except (TypeError, ValueError):
            continue
        if slug_full == "other":
            other += t
            continue
        if "/" not in slug_full:
            continue
        slug = slug_full.split("/", 1)[0]
        if slug.startswith("~") or slug in ignore:
            continue
        tokens[slug] += t
        days[slug].add(r.get("date"))
    total = sum(tokens.values())
    stats = [AuthorStat(slug=s, tokens=t, days_present=len(days[s]),
                        share=(t / total if total else 0.0))
             for s, t in tokens.items()]
    stats.sort(key=lambda a: (-a.tokens, a.slug))
    other_share = other / (total + other) if (total + other) else 0.0
    return stats, other_share


def check_guards(stats: list[AuthorStat], guards: dict) -> None:
    g = {**_DEFAULT_GUARDS, **(guards or {})}
    n = len(stats)
    if n < int(g["min_authors"]) or n > int(g["max_authors"]):
        raise RosterError(f"{n} authors after filtering "
                          f"(guard: {g['min_authors']}..{g['max_authors']})")


def select_authors(stats: list[AuthorStat], policy: dict) -> list[AuthorStat]:
    """Cumulative-share cut: walk authors largest-first, admit while the share
    already covered is below the cut (the author that crosses the line is in).
    Then drop authors present on too few days."""
    cut = float(policy.get("cumulative_share", 0.99))
    min_days = int(policy.get("min_days_present", 7))
    chosen, covered = [], 0.0
    for a in stats:
        if covered >= cut:
            break
        covered += a.share
        if a.days_present >= min_days:
            chosen.append(a)
    return chosen


def key_for(slug: str, policy: dict) -> str:
    aliases = policy.get("aliases") or {}
    return str(aliases.get(slug) or slug.replace("-", "_"))


def build_overlay(selected: list[AuthorStat], *, base_keys: set[str], previous: dict,
                  policy: dict, models_info: dict[str, dict], today: str, meta: dict) -> dict:
    """Previous overlay entries carry over (additive), minus anything now curated
    in base or denied; new qualifying authors are appended. The file changes only
    when membership changes, so its git diff is the human review gate on
    allowlist widening; shares/windows/dates go to the snapshot instead."""
    deny = set(policy.get("deny") or [])
    ignore = set(policy.get("ignore") or [])
    publishers: dict[str, dict] = {}
    for key, entry in ((previous or {}).get("publishers") or {}).items():
        slug = (entry or {}).get("openrouter_slug") or key
        if key in base_keys or slug in deny or slug in ignore:
            continue
        publishers[key] = {k: v for k, v in (entry or {}).items() if k in _ENTRY_FIELDS}
    for a in selected:
        if a.slug in deny:
            continue
        key = key_for(a.slug, policy)
        if key in base_keys:
            continue
        info = models_info.get(a.slug) or {}
        if key in publishers:
            continue          # membership only: nothing volatile is written per day
        publishers[key] = {
            "tier": 2,
            "display_name": info.get("display_name") or a.slug,
            "origin": "openrouter",
            "openrouter_slug": a.slug,
            "first_seen": today,
            "index_urls": ([f"https://huggingface.co/{info['hf_org']}"]
                           if info.get("hf_org") else []),
        }
    return {"meta": meta, "publishers": publishers}


# ---------------------------------------------------------------- orchestration

def _overlay_path(repo: Repo) -> Path:
    return repo.config_dir / OVERLAY_NAME


def _write_overlay(path: Path, overlay: dict) -> None:
    header = ("# GENERATED by cardtrack/roster.py — do not edit; edit config/roster.yaml.\n"
              "# Additive overlay merged under config/sources.yaml (base wins). Committed\n"
              "# with each daily run so a bad day is one `git revert` away.\n")
    body = yaml.safe_dump(overlay, sort_keys=False, allow_unicode=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(header + body, encoding="utf-8")
    os.replace(tmp, path)


def _record_failure(repo: Repo, reason: str, policy: dict) -> dict:
    repo.logs_dir.mkdir(parents=True, exist_ok=True)
    fs = repo.logs_dir / FAILSTREAK_NAME
    streak = 1
    if fs.exists():
        try:
            streak = int(fs.read_text().strip() or 0) + 1
        except ValueError:
            streak = 1
    fs.write_text(str(streak))
    guards = {**_DEFAULT_GUARDS, **(policy.get("guards") or {})}
    issue_ref = None
    if streak == int(guards["failstreak_issue_after"]):
        from .issues import file_issue
        issue_ref = file_issue(
            repo,
            title=f"pipeline-failure: OpenRouter roster sync failed {streak} runs in a row",
            body=(f"Latest reason: {reason}\n\nThe publisher allowlist overlay "
                  f"(config/{OVERLAY_NAME}) is frozen at its last good state; discovery "
                  "for already-listed publishers is unaffected. Check the endpoint/schema "
                  "in config/roster.yaml, or set `enabled: false` to silence this."),
            labels=["pipeline-failure"])
    return {"status": "kept_previous", "reason": reason, "failstreak": streak,
            "issue_ref": issue_ref}


def run_roster(repo: Repo, run_id: str, *, api_key: str | None = None,
               timeout: float | None = None) -> dict:
    """Entry point for scripts/roster.py. Returns a JSON-able summary and never
    raises: every failure, including a programming error, is fail-closed (previous
    overlay kept) and counted toward the failstreak so it cannot go unnoticed."""
    policy = repo.roster_policy
    if not policy.get("enabled", False):
        return {"status": "disabled"}
    try:
        return _sync(repo, run_id, policy, api_key=api_key, timeout=timeout)
    except RosterError as e:
        return _record_failure(repo, str(e), policy)
    except Exception as e:  # noqa: BLE001 — fail closed on anything, but stay observable
        return _record_failure(repo, f"crash: {e.__class__.__name__}: {e}", policy)


def _sync(repo: Repo, run_id: str, policy: dict, *, api_key: str | None,
          timeout: float | None) -> dict:
    if timeout is None:
        timeout = float((repo.settings.get("caps") or {}).get("fetch_timeout_seconds", 60))
    key = api_key or read_api_key(repo)
    if not key:
        raise RosterError(f"{API_KEY_ENV} not set (env or .env)")

    payload = fetch_rankings(str(policy["endpoint"]), key, timeout)
    rows = validate_payload(payload, policy.get("guards") or {})
    stats, other_share = aggregate(rows, policy)
    check_guards(stats, policy.get("guards") or {})
    selected = select_authors(stats, policy)
    models_info = fetch_models(str(policy.get("models_endpoint") or ""), timeout) \
        if policy.get("models_endpoint") else {}

    base = repo.base_sources
    base_keys = set(base.get("publishers") or {}) | set(base.get("evaluators") or {})
    previous = repo.roster_overlay
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    # Static meta only: the overlay must be byte-identical across days with the
    # same membership. Window/as_of/shares live in the snapshot below.
    meta = {"source": "openrouter", "endpoint": policy["endpoint"],
            "cumulative_share": policy.get("cumulative_share", 0.99),
            "min_days_present": policy.get("min_days_present", 7)}
    overlay = build_overlay(selected, base_keys=base_keys, previous=previous, policy=policy,
                            models_info=models_info, today=today, meta=meta)

    prev_keys = set(previous.get("publishers") or {})
    new_keys = sorted(set(overlay["publishers"]) - prev_keys)
    dropped_keys = sorted(prev_keys - set(overlay["publishers"]))
    if overlay != previous or not _overlay_path(repo).exists():
        _write_overlay(_overlay_path(repo), overlay)

    # Small, tracked audit table: every author seen this window and what happened to it.
    selected_slugs = {a.slug for a in selected}
    deny = set(policy.get("deny") or [])
    table = []
    for a in stats:
        k = key_for(a.slug, policy)
        if a.slug in deny:
            status = "denied"
        elif k in base_keys:
            status = "curated"
        elif a.slug in selected_slugs:
            status = "overlay"
        elif a.days_present < int(policy.get("min_days_present", 7)):
            status = "too_few_days"
        else:
            status = "below_cut"
        table.append({"slug": a.slug, "key": k, "share": round(a.share, 4),
                      "days_present": a.days_present, "status": status})
    meta_in = payload.get("meta") or {}
    snapshot_meta = {**meta, "as_of": utcnow(), "run_id": run_id,
                     "window_start": meta_in.get("start_date"),
                     "window_end": meta_in.get("end_date"),
                     "other_share_of_all_tokens": round(other_share, 4),
                     "covered_share_of_all_tokens": round(
                         (1 - other_share) * sum(a.share for a in stats
                                                 if a.slug in selected_slugs
                                                 or key_for(a.slug, policy) in base_keys),
                         4)}
    repo.logs_dir.mkdir(parents=True, exist_ok=True)
    (repo.logs_dir / SNAPSHOT_NAME).write_text(
        json.dumps({"meta": snapshot_meta, "authors": table}, indent=1, ensure_ascii=False)
        + "\n", encoding="utf-8")
    (repo.logs_dir / FAILSTREAK_NAME).unlink(missing_ok=True)
    return {"status": "ok", "authors_in_window": len(stats), "selected": len(selected),
            "overlay_publishers": len(overlay["publishers"]), "new": new_keys,
            "dropped": dropped_keys,
            "window": [meta_in.get("start_date"), meta_in.get("end_date")],
            "other_share_of_all_tokens": round(other_share, 4),
            "models_info_available": bool(models_info)}
