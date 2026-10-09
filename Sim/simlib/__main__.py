"""Allow `python -m simlib ...` as a shortcut for the runner."""
from .run import main

if __name__ == "__main__":
    raise SystemExit(main())
