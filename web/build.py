"""Builds the static site into web/dist (minifies whitespace). Run before starting the web app."""
from pathlib import Path

src = Path(__file__).parent / "src"
dist = Path(__file__).parent / "dist"
dist.mkdir(exist_ok=True)
for f in src.iterdir():
    (dist / f.name).write_text("\n".join(line.strip() for line in f.read_text().splitlines() if line.strip()))
print(f"built {dist}")
