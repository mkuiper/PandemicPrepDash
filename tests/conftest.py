import sys
from pathlib import Path

# Ensure src directory is on sys.path for test runner
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
