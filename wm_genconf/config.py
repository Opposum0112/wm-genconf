"""Input loading and canonical configuration validation."""
from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "wm-genconf.schema.json"


class ConfigError(ValueError):
    """Raised when an input file cannot be parsed or validated."""


def load_config(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    suffix = source.suffix.lower()
    try:
        raw = source.read_text(encoding="utf-8")
        if suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(raw)
        elif suffix == ".toml":
            data = tomllib.loads(raw)
        elif suffix == ".json":
            data = json.loads(raw)
        else:
            raise ConfigError(f"Unsupported input format {suffix!r}; use YAML, TOML, or JSON")
    except (OSError, UnicodeError, yaml.YAMLError, tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Could not read {source}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigError("Configuration root must be an object/mapping")

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(map(str, e.path)))
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ConfigError(details)
    return data
