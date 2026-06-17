"""Generate Stage 2 single-metal-part requirements from raw SubCAD ideas.

The generated files are review candidates. They intentionally freeze one
metal part per raw product idea and exclude assemblies, purchased components,
electronics, rubber, plastic, seals, bearings, labels, and fasteners.
"""

from __future__ import annotations

import hashlib
import json
import re
import textwrap
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "docs" / "subcad_limit_test" / "raw_ideas"
OUT_DIR = ROOT / "docs" / "subcad_limit_test" / "single_metal_parts"

REQUIRED_IDEA_KEYS = {
    "idea_title",
    "product_context",
    "core_function",
    "likely_main_part",
    "why_it_tests_cad_representation",
}


def stable_int(seed: str, low: int, high: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    span = high - low + 1
    return low + int.from_bytes(digest[:4], "big") % span


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def stock_family(title: str, likely: str) -> str:
    text = f"{title} {likely}".lower()
    round_markers = [
        "collar",
        "sleeve",
        "plug",
        "bushing",
        "roller",
        "pin",
        "shaft",
        "spool",
        "cylind",
        "round",
        "tube",
        "knob",
    ]
    sheet_markers = [
        "sheet",
        "cover",
        "guard",
        "tray",
        "shield",
        "panel",
        "clip",
        "strap",
        "bracket",
        "flange",
        "plate",
    ]
    if any(marker in text for marker in round_markers):
        return "round_bar"
    if any(marker in text for marker in sheet_markers):
        return "sheet_or_plate"
    return "rectangular_block"


def material_for(title: str, context: str, family: str, seed: str) -> dict[str, str]:
    text = f"{title} {context}".lower()
    if any(word in text for word in ["food", "sanitary", "marine", "medical", "dental", "lab"]):
        return {
            "material": "AISI 316 stainless steel",
            "reason": "corrosion resistance and cleanable metal surfaces",
        }
    if any(word in text for word in ["electronics", "camera", "uav", "robot", "kiosk", "instrument"]):
        return {
            "material": "6061-T6 aluminum",
            "reason": "low mass with good machinability and stable flat features",
        }
    if any(word in text for word in ["hot", "grinder", "weld", "press", "clamp", "vise", "lathe"]):
        return {
            "material": "1045 medium-carbon steel, normalized",
            "reason": "durable wear surface for workshop loading",
        }
    if family == "round_bar" and stable_int(seed, 0, 3) == 0:
        return {
            "material": "4140 alloy steel, prehard",
            "reason": "strong cylindrical metal part with threaded and slotted details",
        }
    return {
        "material": "low-carbon steel, ASTM A36 or equivalent",
        "reason": "general-purpose single-piece metal stock",
    }


def clamp(value: int, step: int = 5) -> int:
    return int(round(value / step) * step)


def build_dimensions(seed: str, family: str) -> dict[str, Any]:
    if family == "round_bar":
        od = clamp(stable_int(seed + "od", 28, 95), 1)
        length = clamp(stable_int(seed + "len", 24, 120), 1)
        bore = clamp(max(8, od // stable_int(seed + "borediv", 3, 5)), 1)
        return {
            "outer_diameter_mm": od,
            "overall_length_mm": length,
            "axial_bore_diameter_mm": bore,
            "wall_minimum_mm": max(4, (od - bore) // 2),
        }
    if family == "sheet_or_plate":
        length = clamp(stable_int(seed + "len", 85, 260), 5)
        width = clamp(stable_int(seed + "wid", 45, 150), 5)
        thickness = stable_int(seed + "thk", 3, 12)
        return {
            "length_mm": max(length, width),
            "width_mm": min(length, width),
            "thickness_mm": thickness,
        }
    length = clamp(stable_int(seed + "len", 70, 220), 5)
    width = clamp(stable_int(seed + "wid", 35, 120), 5)
    height = clamp(stable_int(seed + "hgt", 16, 70), 1)
    return {
        "length_mm": max(length, width),
        "width_mm": min(length, width),
        "height_mm": height,
    }


def setup_context(family: str) -> str:
    if family == "round_bar":
        return (
            "Start from one cut length of round metal bar. Turn the outside, face both ends, "
            "bore the center, then mill secondary flats, slots, and radial holes as needed. "
            "No separate inserts or fasteners are part of the deliverable."
        )
    if family == "sheet_or_plate":
        return (
            "Start from one flat sheet or plate blank. Cut the outside profile, machine holes, "
            "slots, pockets, lips, and relief features into that same piece. If bends are called "
            "out, they are bends in the same sheet part, not separate welded pieces."
        )
    return (
        "Start from one rectangular metal block or plate. Saw oversize, face all datum sides, "
        "then machine the pockets, holes, slots, angled faces, grooves, and edge treatments into "
        "that same solid piece."
    )


def datum_text(family: str) -> str:
    if family == "round_bar":
        return (
            "Use the cylinder axis as X. The left faced end is datum A at X=0. The radial "
            "direction through the largest flat or slot is datum B. Positive Z points upward "
            "from the part centerline when the main flat faces up."
        )
    return (
        "Use the finished bottom face as datum A. Use the long left edge as datum B and the "
        "near short edge as datum C. The origin is the lower-left-near corner of the finished "
        "rectangular envelope; X follows length, Y follows width, and Z is upward."
    )


def feature_keywords(title: str, likely: str, why: str) -> set[str]:
    text = f"{title} {likely} {why}".lower()
    keys: set[str] = set()
    for name, markers in {
        "v_groove": ["v-groove", "v groove", "cylindrical work", "round stock"],
        "dovetail": ["dovetail"],
        "serration": ["serrated", "serration", "teeth", "stepped"],
        "angled_face": ["angle", "angled", "wedge", "taper"],
        "counterbore": ["counterbore", "counterbored", "bushing pocket"],
        "slot": ["slot", "slotted", "elongated", "relief"],
        "thread": ["thread", "tapped", "set screw", "screw"],
        "pocket": ["pocket", "recess", "pad", "relief"],
        "hook": ["hook", "clip", "toe", "keeper"],
        "flats": ["flat", "flats", "wrench"],
    }.items():
        if any(marker in text for marker in markers):
            keys.add(name)
    return keys


def round_features(seed: str, dims: dict[str, Any], keys: set[str]) -> list[dict[str, Any]]:
    od = dims["outer_diameter_mm"]
    length = dims["overall_length_mm"]
    bore = dims["axial_bore_diameter_mm"]
    flat_width = max(8, od // 3)
    slot_width = stable_int(seed + "slotw", 2, 6)
    features = [
        {
            "name": "single cylindrical body",
            "description": f"Turn one coaxial cylinder to OD {od} mm and length {length} mm from solid round bar.",
        },
        {
            "name": "axial through bore",
            "description": f"Machine a centered through bore diameter {bore} mm along the full length; both bore mouths have 1.0 mm x 45 degree chamfers.",
        },
        {
            "name": "end counterbores",
            "description": f"Add shallow concentric counterbores on both ends, diameter {min(od - 6, bore + 10)} mm x 3 mm deep.",
        },
        {
            "name": "milled reference flat",
            "description": f"Mill one longitudinal flat {flat_width} mm wide over {max(12, length - 8)} mm of length, centered on the top side.",
        },
        {
            "name": "radial clamp holes",
            "description": f"Add two radial tapped M{stable_int(seed + 'tap', 4, 8)} holes through the top flat at X={length // 3} mm and X={2 * length // 3} mm.",
        },
        {
            "name": "split relief slit",
            "description": f"Cut one full-length radial slit {slot_width} mm wide from the outside to the axial bore on datum-B side.",
        },
        {
            "name": "outside edge treatment",
            "description": "Break all outside circular edges with 1.0 mm chamfers and keep internal bore edges visibly chamfered.",
        },
    ]
    if "flats" in keys:
        features.append(
            {
                "name": "opposed wrench flats",
                "description": f"Mill two opposed flats across the outside, leaving {max(od - 8, int(od * 0.78))} mm across flats over the middle third of the length.",
            }
        )
    if "slot" in keys:
        features.append(
            {
                "name": "cross relief slot",
                "description": f"Machine one transverse slot {slot_width + 2} mm wide across the top flat at X={length // 2} mm, depth {max(2, od // 10)} mm.",
            }
        )
    return features


def flat_features(seed: str, dims: dict[str, Any], keys: set[str]) -> list[dict[str, Any]]:
    length = dims["length_mm"]
    width = dims["width_mm"]
    thickness = dims.get("thickness_mm", dims.get("height_mm", 10))
    hole_d = stable_int(seed + "hole", 5, 13)
    slot_w = stable_int(seed + "slotw", 7, 18)
    pocket_depth = max(1, min(thickness - 1, stable_int(seed + "pdepth", 1, max(2, thickness // 2))))
    edge = max(10, min(length, width) // 5)
    features = [
        {
            "name": "single rectangular metal body",
            "description": f"Machine one body with finished envelope {length} mm x {width} mm x {thickness} mm.",
        },
        {
            "name": "mounting hole pattern",
            "description": f"Drill two through holes diameter {hole_d} mm on the length centerline at X={edge} mm and X={length - edge} mm, Y={width // 2} mm.",
        },
        {
            "name": "functional center feature",
            "description": f"Machine a central obround slot {max(30, length // 3)} mm long x {slot_w} mm wide through the part, centered at X={length // 2} mm, Y={width // 2} mm.",
        },
        {
            "name": "top relief pocket",
            "description": f"Mill a rectangular relief pocket {max(25, length // 4)} mm x {max(18, width // 3)} mm x {pocket_depth} mm deep on the top face, centered between the mounting holes.",
        },
        {
            "name": "edge chamfers",
            "description": "Apply 1.0 mm x 45 degree chamfers to all top outside edges and 0.5 mm chamfers to hole and slot mouths.",
        },
    ]
    if "v_groove" in keys:
        features.append(
            {
                "name": "centered V-groove",
                "description": f"Cut a 90 degree V-groove along the full X length on the top face, groove mouth {min(width - 12, max(18, width // 2))} mm wide and depth {max(3, thickness // 3)} mm.",
            }
        )
    if "dovetail" in keys:
        features.append(
            {
                "name": "dovetail slide form",
                "description": f"Machine a straight dovetail groove on the top face, length {max(40, length - 24)} mm, throat {max(12, width // 5)} mm, included angle 60 degrees.",
            }
        )
    if "serration" in keys:
        features.append(
            {
                "name": "serrated contact edge",
                "description": f"Cut {stable_int(seed + 'teeth', 5, 12)} equal triangular serrations across the rear edge, each {stable_int(seed + 'tooth', 2, 5)} mm deep.",
            }
        )
    if "angled_face" in keys:
        features.append(
            {
                "name": "machined angled reference face",
                "description": f"Machine one top reference face at {stable_int(seed + 'ang', 10, 45)} degrees over the last {max(18, length // 5)} mm of length.",
            }
        )
    if "counterbore" in keys:
        features.append(
            {
                "name": "counterbored seat",
                "description": f"Add a central counterbore diameter {max(slot_w + 8, 20)} mm x {min(6, max(2, thickness // 3))} mm deep around the center feature.",
            }
        )
    if "hook" in keys:
        features.append(
            {
                "name": "integral hook lip",
                "description": f"Leave an integral hook lip on one short end, projecting {stable_int(seed + 'lip', 6, 18)} mm and undercut {stable_int(seed + 'undercut', 2, 6)} mm for registration.",
            }
        )
    if "thread" in keys:
        features.append(
            {
                "name": "side tapped hole",
                "description": f"Tap one side hole M{stable_int(seed + 'tap', 4, 10)} from the right long edge into the central pocket; hole axis is parallel to Y.",
            }
        )
    return features


def tolerances(family: str) -> list[str]:
    if family == "round_bar":
        return [
            "Outside diameter and axial bore diameter: +/-0.05 mm.",
            "Concentricity of bore to outer diameter: within 0.05 mm TIR.",
            "Milled flats and slots: +/-0.15 mm unless otherwise specified.",
            "Nonfunctional chamfers: +/-0.3 mm.",
        ]
    return [
        "Overall envelope dimensions: +/-0.20 mm.",
        "Hole diameters and slot widths: +/-0.10 mm.",
        "Hole and slot center positions from datums B and C: +/-0.15 mm.",
        "Pocket depths and relief depths: +/-0.10 mm.",
        "Nonfunctional chamfers and radii: +/-0.30 mm.",
    ]


def negative_requirements(raw_title: str) -> list[str]:
    return [
        "Represent exactly one metal part only.",
        "Do not model screws, nuts, springs, bushings, bearings, rubber pads, plastic covers, electronics, labels, handles, knobs, adhesives, weld beads, or separate inserts.",
        "Do not convert the part into an assembly or multiple bodies.",
        "Do not replace through holes, slots, pockets, grooves, flats, tapers, or chamfers with cosmetic markings.",
        "Do not omit datum-critical features just because they are small.",
        f"Do not broaden the requirement back into the full product idea named '{raw_title}'; this requirement is only for its chosen metal part.",
    ]


def acceptance(features: list[dict[str, Any]], family: str) -> list[str]:
    checks = [
        "The output contains one continuous metal solid representing one part.",
        "The stock family, material intent, envelope dimensions, and datum orientation match this requirement.",
    ]
    checks.extend(f"The feature named '{feature['name']}' is present with the stated size and position." for feature in features)
    checks.extend(
        [
            "All required chamfers, reliefs, and edge treatments are visible in STEP and STL outputs.",
            "No extra parts, fasteners, hardware, labels, cosmetic meshes, or nonmetal components are present.",
        ]
    )
    if family == "round_bar":
        checks.append("Round features are coaxial unless the requirement explicitly says they are radial or offset.")
    else:
        checks.append("Flat datums remain planar and usable; pockets or slots do not accidentally break unsupported walls.")
    return checks


def build_requirement(agent: dict[str, Any], idea: dict[str, Any], index: int) -> dict[str, Any]:
    agent_number = int(agent["agent_number"])
    seed = f"{agent_number:03d}-{index:02d}-{idea['idea_title']}"
    family = stock_family(idea["idea_title"], idea["likely_main_part"])
    dims = build_dimensions(seed, family)
    material = material_for(idea["idea_title"], idea["product_context"], family, seed)
    keys = feature_keywords(idea["idea_title"], idea["likely_main_part"], idea["why_it_tests_cad_representation"])
    features = round_features(seed, dims, keys) if family == "round_bar" else flat_features(seed, dims, keys)
    requirement_id = f"SMP-{agent_number:03d}-{index:02d}"
    target_name = f"{idea['idea_title']} - single metal part"
    full_description = (
        f"Make the single metal part for the product idea '{idea['idea_title']}'. "
        f"The broader use case is: {idea['product_context']} "
        f"The chosen deliverable is only the metal body implied by: {idea['likely_main_part']} "
        "All other product elements are external reference items and must not be modeled. "
        f"The part must perform this mechanical role: {idea['core_function']} "
        f"It is intentionally included in the SubCAD limit corpus because: {idea['why_it_tests_cad_representation']} "
        f"The part is made from {material['material']} using {family.replace('_', ' ')} stock. "
        f"{setup_context(family)}"
    )
    return {
        "requirement_id": requirement_id,
        "stage": "single_metal_part_requirement",
        "status": "review_candidate",
        "source": {
            "agent_number": agent_number,
            "agent_id": agent.get("agent_id"),
            "domain": agent.get("domain"),
            "raw_idea_index": index,
            "raw_idea_title": idea["idea_title"],
        },
        "part_name": target_name,
        "single_part_boundary": {
            "deliverable": "one metal part only",
            "stock_family": family,
            "allowed_stock_forms": ["sheet", "rod", "plate", "block"],
            "excluded_from_scope": [
                "assemblies",
                "fasteners",
                "springs",
                "bearings",
                "bushings",
                "rubber",
                "plastic",
                "electronics",
                "labels",
                "coatings as geometry",
            ],
        },
        "material": material,
        "manufacturing_context": setup_context(family),
        "overall_envelope_mm": dims,
        "datum_orientation": datum_text(family),
        "full_description": textwrap.fill(full_description, width=100),
        "functional_features": features,
        "tolerances": tolerances(family),
        "acceptance_checklist": acceptance(features, family),
        "negative_requirements": negative_requirements(idea["idea_title"]),
        "immutable_requirement_note": (
            "After review, this English requirement is the product truth for later SubCAD code generation. "
            "Do not simplify it to fit current SubCAD limitations."
        ),
    }


def validate_raw_agent(path: Path, data: dict[str, Any]) -> None:
    if not isinstance(data.get("ideas"), list):
        raise ValueError(f"{path}: ideas must be a list")
    for idx, idea in enumerate(data["ideas"], start=1):
        missing = REQUIRED_IDEA_KEYS - set(idea)
        if missing:
            raise ValueError(f"{path}: idea {idx} missing {sorted(missing)}")


def render_agent_markdown(agent_data: dict[str, Any], parts: list[dict[str, Any]]) -> str:
    lines = [
        f"# Agent {agent_data['agent_number']:03d} Single Metal Part Requirements",
        "",
        f"Domain: {agent_data.get('domain', 'unknown')}",
        "",
        "Each item below is one metal part only. Product assemblies and nonmetal components are explicitly out of scope.",
        "",
    ]
    for part in parts:
        lines.extend(
            [
                f"## {part['requirement_id']} - {part['source']['raw_idea_title']}",
                "",
                f"Part name: {part['part_name']}",
                "",
                f"Material: {part['material']['material']} ({part['material']['reason']})",
                "",
                f"Envelope: `{json.dumps(part['overall_envelope_mm'], sort_keys=True)}`",
                "",
                f"Datum orientation: {part['datum_orientation']}",
                "",
                "Full description:",
                "",
                part["full_description"],
                "",
                "Functional features:",
            ]
        )
        for feature in part["functional_features"]:
            lines.append(f"- {feature['name']}: {feature['description']}")
        lines.extend(["", "Tolerances:"])
        lines.extend(f"- {item}" for item in part["tolerances"])
        lines.extend(["", "Acceptance checklist:"])
        lines.extend(f"- {item}" for item in part["acceptance_checklist"])
        lines.extend(["", "Negative requirements:"])
        lines.extend(f"- {item}" for item in part["negative_requirements"])
        lines.extend(["", "---", ""])
    return "\n".join(lines).rstrip() + "\n"


def render_readme(total_files: int, total_parts: int) -> str:
    return f"""# Single Metal Part Requirements

This folder contains Stage 2 review candidates generated from the raw SubCAD
limit-test ideas.

Current frozen input size: {total_parts} raw ideas from {total_files} agent files.

Boundary rule:

- Each requirement describes exactly one metal part.
- The allowed starting forms are sheet, rod, plate, or block.
- Larger products, assemblies, electronics, plastic, rubber, bearings, bushings,
  springs, bought-out fasteners, labels, and coatings are outside the modeled
  scope.
- If the raw idea was a multi-part product, the Stage 2 requirement selects one
  metal part from that product and describes only that part.
- These are English review candidates. After review, accepted entries become
  immutable product truth for SubCAD program generation.

Files:

- `agent_###_*.json`: machine-readable Stage 2 requirements for one source agent.
- `agent_###_*.md`: human-readable review copy for the same requirements.
- `all_single_metal_parts.jsonl`: one JSON object per requirement.
- `manifest.json`: file counts, part counts, and generation rule summary.
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_files = sorted(RAW_DIR.glob("agent_*.json"))
    all_parts: list[dict[str, Any]] = []
    manifest_agents = []
    for raw_path in raw_files:
        agent_data = json.loads(raw_path.read_text(encoding="utf-8"))
        validate_raw_agent(raw_path, agent_data)
        parts = [
            build_requirement(agent_data, idea, index)
            for index, idea in enumerate(agent_data["ideas"], start=1)
        ]
        all_parts.extend(parts)
        stem = raw_path.stem.replace("agent_", "agent_")
        json_path = OUT_DIR / f"{stem}_single_metal_parts.json"
        md_path = OUT_DIR / f"{stem}_single_metal_parts.md"
        json_path.write_text(json.dumps({
            "agent_number": agent_data["agent_number"],
            "agent_id": agent_data.get("agent_id"),
            "domain": agent_data.get("domain"),
            "stage": "single_metal_part_requirements",
            "source_raw_file": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
            "requirements": parts,
        }, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(render_agent_markdown(agent_data, parts), encoding="utf-8")
        manifest_agents.append({
            "agent_number": agent_data["agent_number"],
            "domain": agent_data.get("domain"),
            "raw_file": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
            "json_file": str(json_path.relative_to(ROOT)).replace("\\", "/"),
            "markdown_file": str(md_path.relative_to(ROOT)).replace("\\", "/"),
            "requirements": len(parts),
        })

    (OUT_DIR / "all_single_metal_parts.jsonl").write_text(
        "".join(json.dumps(part, sort_keys=True) + "\n" for part in all_parts),
        encoding="utf-8",
    )
    manifest = {
        "stage": "single_metal_part_requirements",
        "status": "review_candidate",
        "source_raw_agent_files": len(raw_files),
        "total_requirements": len(all_parts),
        "boundary_rule": "Each requirement is exactly one metal part made from sheet, rod, plate, or block.",
        "agents": manifest_agents,
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "README.md").write_text(render_readme(len(raw_files), len(all_parts)), encoding="utf-8")
    print(json.dumps({
        "raw_files": len(raw_files),
        "requirements": len(all_parts),
        "output_dir": str(OUT_DIR),
    }, indent=2))


if __name__ == "__main__":
    main()
