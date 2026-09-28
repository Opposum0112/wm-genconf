# Architecture

## Pipeline

1. Front ends parse YAML, TOML, or JSON into a Python mapping. YAML uses safe loading.
2. Validation checks the versioned JSON Schema before normalization.
3. The intermediate representation normalizes defaults and semantic keybindings.
4. Backend adapters translate the supported subset into compositor-native text.
5. Output goes to stdout or an explicitly requested file. The compiler never activates generated configuration.

## Portability contract

The canonical schema represents only the portable subset. A setting should be added to the shared schema only when its meaning can be defined independently of a specific compositor. Backend-specific functionality should eventually live in namespaced extensions, for example extensions.hyprland.

The first bootstrap exposes terminal, launcher, inner/outer gaps, border width, and three semantic bindings. The current renderers are initial templates, not a promise of full compositor feature parity. Validate generated files against the target compositor's installed version before deploying them.

## Planned capability model

Each backend should declare:
- supported canonical fields;
- native feature mappings;
- unsupported or lossy mappings;
- backend/version constraints;
- whether an operation is compile-time configuration or runtime IPC.

Diagnostics should distinguish errors (cannot compile safely), warnings (setting cannot be represented), and informational notes (approximate mapping).
