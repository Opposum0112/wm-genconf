"""Command-line interface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .backends import BACKENDS
from .config import ConfigError, load_config
from .ir import normalize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wm-genconf", description="Compile portable WM configuration")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="parse and validate a configuration")
    validate.add_argument("config")
    compile_cmd = sub.add_parser("compile", help="compile to a native backend configuration")
    compile_cmd.add_argument("config")
    compile_cmd.add_argument("--backend", choices=sorted(BACKENDS), required=True)
    compile_cmd.add_argument("--output", "-o", help="output file (default: stdout)")
    ir_cmd = sub.add_parser("ir", help="print normalized intermediate representation as JSON")
    ir_cmd.add_argument("config")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        if args.command == "validate":
            print(f"Valid configuration: {args.config}")
            return 0
        ir = normalize(config)
        if args.command == "ir":
            print(json.dumps(ir, indent=2, sort_keys=True))
            return 0
        output = BACKENDS[args.backend](ir)
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0
    except (ConfigError, ValueError, OSError) as exc:
        print(f"wm-genconf: error: {exc}", file=sys.stderr)
        return 2
