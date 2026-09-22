"""Repository context: root discovery, paths, config loading."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


def utcnow() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def find_root(explicit: str | Path | None = None) -> Path:
    """Resolve the repo root: explicit arg > CARDTRACK_ROOT env > package location."""
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("CARDTRACK_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[1]


@dataclass
class Repo:
    root: Path
    _cache: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def locate(cls, explicit: str | Path | None = None) -> Repo:
        return cls(root=find_root(explicit))

    # --- paths ---
    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "docs.sqlite"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def text_dir(self) -> Path:
        return self.data_dir / "text"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    @property
    def site_dir(self) -> Path:
        return self.root / "site"

    def ensure_dirs(self) -> None:
        for p in (self.data_dir, self.raw_dir, self.text_dir, self.logs_dir):
            p.mkdir(parents=True, exist_ok=True)

    # --- config ---
    def _load_yaml(self, name: str) -> dict:
        if name not in self._cache:
            path = self.config_dir / name
            with open(path, encoding="utf-8") as f:
                self._cache[name] = yaml.safe_load(f) or {}
        return self._cache[name]

    @property
    def settings(self) -> dict:
        return self._load_yaml("settings.yaml")

    def _load_yaml_optional(self, name: str) -> dict:
        path = self.config_dir / name
        if not path.exists():
            return {}
        return self._load_yaml(name)

    @property
    def base_sources(self) -> dict:
        """The curated allowlist exactly as written in sources.yaml."""
        return self._load_yaml("sources.yaml")

    @property
    def roster_policy(self) -> dict:
        """config/roster.yaml; {} (=> disabled) when absent."""
        return self._load_yaml_optional("roster.yaml")

    @property
    def roster_overlay(self) -> dict:
        """config/sources.generated.yaml as written by cardtrack/roster.py; {} when absent."""
        return self._load_yaml_optional("sources.generated.yaml")

    @property
    def sources(self) -> dict:
        """Effective allowlist: sources.yaml plus, when roster sync is enabled, the
        generated overlay's publishers that do not collide with a curated key.
        Additive only — the overlay can never modify or remove a curated entry."""
        if "__sources__" not in self._cache:
            base = self.base_sources
            merged = {cat: dict(entries or {}) for cat, entries in base.items()}
            policy = self.roster_policy
            if policy.get("enabled", False):
                curated = set(merged.get("publishers") or {}) | set(merged.get("evaluators") or {})
                # deny is honoured here too, so it works even while the sync is
                # failing closed and cannot rewrite the overlay
                deny = set(policy.get("deny") or [])
                for key, entry in (self.roster_overlay.get("publishers") or {}).items():
                    slug = (entry or {}).get("openrouter_slug") or key
                    if key not in curated and slug not in deny and key not in deny:
                        merged.setdefault("publishers", {})[key] = dict(entry or {})
            self._cache["__sources__"] = merged
        return self._cache["__sources__"]

    @property
    def criteria(self) -> dict:
        return self._load_yaml("criteria.yaml")

    def setting(self, dotted: str, default: Any = None) -> Any:
        """Dotted lookup into settings.yaml, e.g. setting('caps.max_new_documents_per_run')."""
        node: Any = self.settings
        for key in dotted.split("."):
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node

    @property
    def fingerprint_ignore_patterns(self) -> tuple[str, ...]:
        """Line regexes excluded from content fingerprints (page furniture)."""
        return tuple(self.setting("fingerprint.ignore_line_patterns", []) or [])

    def publisher_info(self, publisher: str) -> tuple[dict, str] | None:
        """Return (entry, category) for a publisher key, category in {'publishers','evaluators'}."""
        for category in ("publishers", "evaluators"):
            entries = self.sources.get(category) or {}
            if publisher in entries:
                return (entries[publisher] or {}), category
        return None
