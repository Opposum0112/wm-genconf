"""Native configuration backends."""
from .hyprland import render as render_hyprland
from .mango import render as render_mango
from .niri import render as render_niri
from .sway import render as render_sway

BACKENDS = {
    "hyprland": render_hyprland,
    "mango": render_mango,
    "niri": render_niri,
    "sway": render_sway,
}
