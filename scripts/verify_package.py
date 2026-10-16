"""Check the built sdist and wheel before publishing: expected files only, matching name and version.

Usage: python scripts/verify_package.py DIST_DIR
"""

from __future__ import annotations

import sys
import tarfile
import zipfile
from email.parser import Parser
from pathlib import Path

import tomllib

project = tomllib.loads(Path("pyproject.toml").read_text())["project"]
name, version = project["name"], project["version"]
dist = Path(sys.argv[1])
wheels, sdists = list(dist.glob("*.whl")), list(dist.glob("*.tar.gz"))
assert len(wheels) == 1 and len(sdists) == 1, f"Expected one wheel and one sdist in {dist}"

with zipfile.ZipFile(wheels[0]) as wheel:
    files = wheel.namelist()
    info = f"{name}-{version}.dist-info/"
    unexpected = [f for f in files if not (f.startswith("bachs/") or f.startswith(info))]
    assert not unexpected, f"Unexpected files in wheel: {unexpected}"
    assert not [f for f in files if "__pycache__" in f or f.endswith(".pyc")], "Compiled files in wheel"
    for required in ("bachs/__init__.py", "bachs/py.typed", "bachs/webhooks.py", f"{info}licenses/LICENSE"):
        assert required in files, f"Missing from wheel: {required}"
    metadata = Parser().parsestr(wheel.read(info + "METADATA").decode())
    assert (metadata["Name"], metadata["Version"]) == (name, version), (metadata["Name"], metadata["Version"])

with tarfile.open(sdists[0]) as sdist:
    root = f"{name}-{version}/"
    allowed = ("src/bachs/", "tests/", "scripts/", ".github/", "README.md", "CHANGELOG.md", "RELEASING.md", "LICENSE",
               "pyproject.toml", "PKG-INFO", ".gitignore")
    members = [m.name.removeprefix(root) for m in sdist.getmembers() if m.isfile()]
    unexpected = [m for m in members if not m.startswith(allowed)]
    assert not unexpected, f"Unexpected files in sdist: {unexpected}"

print(f"Verified {wheels[0].name} ({len(files)} files) and {sdists[0].name} ({len(members)} files)")
