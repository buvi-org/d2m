"""Generate the SubCAD browser visualization demo session.

Run from the repository root:
    python examples/subcad_chrome_demo.py

Then open:
    http://127.0.0.1:8091/visualization.html?session=sessions/chrome_demo/scene.json
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.subcad import Stock  # noqa: E402


def build_demo_part() -> Stock:
    """Build a representative SubCAD part for browser playback testing."""
    return (
        Stock.rectangular(90, 55, 18, material="aluminum_6061")
        .face_mill(depth=1.0)
        .pocket(width=22, length=34, depth=5, cx=-12, cy=0)
        .circular_pocket(diameter=14, depth=4, cx=22, cy=0)
        .slot(length=42, width=8, depth=6, cx=0, cy=16)
        .drill(diameter=5, depth=12, cx=-30, cy=-16)
        .peck_drill(diameter=4, depth=14, cx=30, cy=-16)
    )


def export_demo_session(output_dir: Path, *, clean: bool = True) -> dict:
    """Export the demo visualization package and return the scene dict."""
    if clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    part = build_demo_part()
    return part.visualization_package(
        output_dir,
        target=part,
        tolerance_mm=0.25,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "web" / "sessions" / "chrome_demo"),
        help="Visualization session output directory.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove the existing output directory first.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    scene = export_demo_session(output_dir, clean=not args.no_clean)
    scene_path = output_dir / "scene.json"
    state_count = len(scene.get("assets", {}).get("stock_states", []))

    print(f"Wrote {scene_path}")
    print(f"Operations: {len(scene.get('operations', []))}")
    print(f"Stock states: {state_count}")


if __name__ == "__main__":
    main()
