# wm-genconf

**A backend-neutral configuration compiler for Wayland window managers and compositors.**

wm-genconf accepts one canonical YAML, TOML, or JSON configuration, validates it, normalizes it into an intermediate representation (IR), and emits native configuration for supported backends.

## Architecture

```text
YAML / TOML / JSON
        |
        v
  Parse + validate  <--- JSON Schema
        |
        v
 Normalized IR (JSON-compatible)
        |
        v
 Backend adapters
   |   |   |   |
 Hypr Mango Niri Sway ... River / Qtile
```

The project deliberately separates portable settings from backend-specific features. It will report unsupported settings rather than silently pretending they were translated.

## Status

Early bootstrap. The initial implementation supports a small portable subset for Hyprland, MangoWC, Niri, and Sway. River and Qtile are planned; their command/configuration models differ enough that they need dedicated adapters and explicit capability handling.

## Quick start

Requires Python 3.11+.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
wm-genconf validate examples/wayle.yaml
wm-genconf compile examples/wayle.yaml --backend hyprland --output ./build/hyprland.conf
wm-genconf compile examples/wayle.yaml --backend mango --output ./build/mango.conf
wm-genconf compile examples/wayle.yaml --backend niri --output ./build/config.kdl
wm-genconf compile examples/wayle.yaml --backend sway --output ./build/sway.conf
```

You can also run it without installing the console script:

```sh
python -m wm_genconf validate examples/wayle.yaml
python -m wm_genconf compile examples/wayle.yaml --backend hyprland
```

## Canonical configuration

See [examples/wayle.yaml](examples/wayle.yaml) and [schema/wm-genconf.schema.json](schema/wm-genconf.schema.json).

The schema defines portable settings such as terminal, launcher, gaps, border width, and semantic keybindings. Backend-specific extensions are intentionally not part of the portable core yet.

## Design principles

- **One source of truth:** compositor settings are authored once.
- **Explicit portability:** adapters declare what they can translate.
- **No silent loss:** unsupported features produce diagnostics.
- **Deterministic output:** equivalent inputs should generate stable output.
- **Safe by default:** compilation writes to stdout unless an output path is supplied; it does not execute commands or modify live compositor configuration.
- **Incremental backend support:** add adapters without coupling the canonical schema to one compositor.

## Development

```sh
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Roadmap

1. [x] Canonical configuration model and JSON Schema
2. [x] YAML, TOML, and JSON input parsing
3. [x] Initial IR and CLI
4. [x] Initial Hyprland, MangoWC, Niri, and Sway adapters
5. [ ] Capability registry and structured diagnostics
6. [ ] River and Qtile adapters
7. [ ] Golden-file tests against compositor versions
8. [ ] Optional backend-specific extension namespaces
9. [ ] Wayle shell integration and config migration tooling

## License

MIT. See [LICENSE](LICENSE).
