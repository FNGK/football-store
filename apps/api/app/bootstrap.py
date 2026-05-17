"""Add monorepo packages to sys.path for local development."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_PATHS = [
    _ROOT / "packages" / "shared",
    _ROOT / "packages" / "gateway",
    _ROOT / "packages" / "agents",
    _ROOT / "packages" / "crm",
]

for path in _PATHS:
    s = str(path)
    if s not in sys.path:
        sys.path.insert(0, s)
