"""Small normalized intermediate representation (IR)."""
from __future__ import annotations

from typing import Any


def normalize(config: dict[str, Any]) -> dict[str, Any]:
    desktop = config["desktop"]
    appearance = desktop.get("appearance", {})
    gaps = appearance.get("gaps", {})
    bindings = desktop.get("keybindings", {})
    compositor = desktop.get("compositor", {})
    return {
        "version": config["version"],
        "terminal": desktop.get("terminal", "foot"),
        "launcher": desktop.get("launcher", "fuzzel"),
        "gaps": {"inner": gaps.get("inner", 6), "outer": gaps.get("outer", 10)},
        "border_width": appearance.get("border_width", 2),
        "keybindings": {
            "terminal": bindings.get("terminal", "Super+Return"),
            "launcher": bindings.get("launcher", "Super+D"),
            "close_window": bindings.get("close_window", "Super+Q"),
        },
        "layout": compositor.get("layout", "tile"),
    }


def split_binding(binding: str) -> tuple[list[str], str]:
    """Convert a binding such as Super+Shift+Return to modifiers and key."""
    parts = [part for part in binding.replace(" ", "").split("+") if part]
    if not parts:
        raise ValueError("Keybinding cannot be empty")
    aliases = {"super": "SUPER", "ctrl": "CTRL", "control": "CTRL", "alt": "ALT", "shift": "SHIFT"}
    modifiers = [aliases[p.lower()] for p in parts[:-1] if p.lower() in aliases]
    key = parts[-1]
    return modifiers, key
