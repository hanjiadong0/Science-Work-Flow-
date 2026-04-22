from __future__ import annotations

from pathlib import Path

__all__ = ["__version__"]
__version__ = "0.1.0"

_PACKAGE_DIR = Path(__file__).resolve().parent
_SRC_PACKAGE_DIR = _PACKAGE_DIR.parent / "src" / "cambagent_eval"

if _SRC_PACKAGE_DIR.exists():
    __path__ = [str(_PACKAGE_DIR), str(_SRC_PACKAGE_DIR)]
else:
    __path__ = [str(_PACKAGE_DIR)]
