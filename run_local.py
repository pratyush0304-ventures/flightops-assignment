"""Run smoke tests using this file's folder, not VS Code's workspace cwd."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

print("script:", os.path.abspath(__file__))
print("cwd:   ", os.getcwd())
print("app.py exists:", os.path.isfile(os.path.join(ROOT, "app.py")))
print("python:", sys.executable)
print()

if not os.path.isfile(os.path.join(ROOT, "app.py")):
    print("This copy of the project is missing app.py.")
    print("Clone or unzip so app.py, memory.py, and tools.py are in the same folder.")
    sys.exit(1)

from app import run_tool_tests

run_tool_tests()
