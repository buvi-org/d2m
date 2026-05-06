"""Streamlit UI for d2m CAPP Process Planning.

Provides a web interface for the full inference pipeline:
  - Upload STEP files
  - Select material, volume, tolerances
  - View parsed geometry summary
  - Generate manufacturing process plans via DeepSeek
  - Review DFM warnings and operations table
  - Download full JSON plan

Usage:
    streamlit run app/main.py
"""

from __future__ import annotations

import os
import json
import time
import sys
from pathlib import Path
from typing import Optional

# Ensure project root is on sys.path so src/ imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="d2m - CAPP Process Planner",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Late imports (after page config)
# ---------------------------------------------------------------------------
from src.knowledge_graph import list_materials, get_material_properties
from src.cad_parser import parse_step

from app.pipeline import InferencePipeline, PipelineResult


# =========================================================================
#  Constants / helpers
# =========================================================================

def _format_material_label(key: str) -> str:
    """Convert material key to a readable label.

    'aluminum_6061' -> 'Aluminum 6061-T6'
    'stainless_316' -> 'Stainless 316'
    """
    props = get_material_properties(key)
    desc = props.get("description", "")
    # Extract common name from description
    if desc:
        return desc.split(".")[0].strip()
    return key.replace("_", " ").title()


def _material_display_name(key: str) -> str:
    """Short display name for dropdown."""
    name = key.replace("_", " ").title()
    # Fix common abbreviations
    name = name.replace("Peek", "PEEK")
    name = name.replace("Nylon Pa6", "Nylon PA6")
    name = name.replace("Abs", "ABS")
    return name


# =========================================================================
#  CSS
# =========================================================================

def _inject_css():
    """Inject a small amount of custom CSS for polish."""
    st.markdown("""
    <style>
        /* Metric card styling */
        [data-testid="stMetric"] {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #e9ecef;
        }
        [data-testid="stMetric"] label {
            font-size: 0.85rem;
            color: #6c757d;
        }
        /* Warning/error expanders */
        .dfm-error {
            border-left: 4px solid #dc3545;
        }
        .dfm-warning {
            border-left: 4px solid #ffc107;
        }
        /* Step status */
        .step-done {
            color: #198754;
        }
        .step-error {
            color: #dc3545;
        }
        .step-running {
            color: #0d6efd;
        }
        /* Table spacing */
        .stDataFrame {
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)


# =========================================================================
#  Session state initialization
# =========================================================================

def _init_session_state():
    """Initialize all keys in st.session_state if they do not exist."""
    defaults = {
        "step_file": None,
        "step_filename": None,
        "geometry": None,
        "pipeline_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================================
#  Sidebar
# =========================================================================

def _render_sidebar() -> dict:
    """Render the sidebar controls and return their values as a dict."""
    st.sidebar.title("Manufacturing Setup")

    st.sidebar.markdown("---")

    # Material selection
    materials = list_materials()
    material_labels = {key: _material_display_name(key) for key in materials}

    # Sort by display name
    sorted_materials = sorted(materials, key=lambda k: material_labels[k])

    selected_label = st.sidebar.selectbox(
        "Material",
        options=sorted_materials,
        format_func=lambda k: material_labels[k],
        index=sorted_materials.index("aluminum_6061") if "aluminum_6061" in sorted_materials else 0,
        help="Select the workpiece material.",
    )

    # Show material properties in an expander
    props = get_material_properties(selected_label)
    if props:
        with st.sidebar.expander("Material Properties"):
            mat_type = props.get("material_type", "unknown").capitalize()
            st.markdown(f"**Type:** {mat_type}")
            st.markdown(f"**Density:** {props.get('density_gcm3', 'N/A')} g/cm^3")
            ts = props.get("tensile_strength_mpa", "N/A")
            st.markdown(f"**Tensile Strength:** {ts} MPa")
            mach = props.get("machinability_pct")
            if mach is not None:
                st.markdown(f"**Machinability:** {mach}%")
            st.caption(props.get("description", ""))

    st.sidebar.markdown("---")

    # Production volume
    volume = st.sidebar.number_input(
        "Production Volume",
        min_value=1,
        max_value=100000,
        value=100,
        step=10,
        help="Number of units to produce.",
    )

    # Tolerance
    tolerances = st.sidebar.text_input(
        "Tolerances",
        value="±0.1mm",
        help="General tolerance specification (e.g., ±0.1mm, ISO 2768-m).",
    )

    st.sidebar.markdown("---")

    # API Key
    default_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    api_key = st.sidebar.text_input(
        "DeepSeek API Key",
        value=default_api_key,
        type="password",
        placeholder="sk-...",
        help="Your DeepSeek API key. Also read from DEEPSEEK_API_KEY env var.",
    )

    if not api_key:
        st.sidebar.warning(
            "No API key provided. Set the DEEPSEEK_API_KEY environment "
            "variable or enter it above."
        )

    st.sidebar.markdown("---")

    # Generate button
    generate_clicked = st.sidebar.button(
        "Generate Plan",
        type="primary",
        use_container_width=True,
        disabled=not api_key or st.session_state.get("step_file") is None,
    )

    if st.session_state.get("step_file") is None:
        st.sidebar.caption("Upload a STEP file to enable plan generation.")

    return {
        "material": selected_label,
        "material_label": material_labels[selected_label],
        "volume": volume,
        "tolerances": tolerances,
        "api_key": api_key,
        "generate_clicked": generate_clicked,
    }


# =========================================================================
#  Main panel: header
# =========================================================================

def _render_header():
    """Render the main panel header."""
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.title("CAPP Process Planner")
        st.caption(
            "Computer-Aided Process Planning for CNC machining. "
            "Upload a STEP file, specify material and volume, and get a "
            "manufacturing process plan generated by AI."
        )
    with col2:
        # Placeholder for logo or branding
        pass


# =========================================================================
#  Main panel: file upload + geometry summary
# =========================================================================

def _render_file_upload():
    """Render the STEP file uploader and geometry summary."""
    st.subheader("Part Geometry")

    uploaded = st.file_uploader(
        "Upload STEP file",
        type=["step", "stp", "stpnc"],
        help="Drag and drop a STEP file (AP203/AP214).",
        key="step_uploader",
    )

    # Handle new upload
    if uploaded is not None:
        # Check if it's a new file
        if st.session_state.get("step_filename") != uploaded.name:
            # Save to a temp location for parsing
            import tempfile

            st.session_state["step_filename"] = uploaded.name
            st.session_state["step_file"] = None
            st.session_state["geometry"] = None
            st.session_state["pipeline_result"] = None

            with tempfile.NamedTemporaryFile(
                suffix=Path(uploaded.name).suffix,
                delete=False,
            ) as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            try:
                geometry = parse_step(tmp_path)
                st.session_state["geometry"] = geometry
                st.session_state["step_file"] = tmp_path
            except Exception as e:
                st.error(f"Failed to parse STEP file: {e}")
                st.session_state["step_file"] = None
                st.session_state["geometry"] = None
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

    # Show geometry summary if available
    geometry = st.session_state.get("geometry")
    if geometry:
        st.markdown("### Geometry Summary")

        dims = geometry.get("overall_dimensions", (0, 0, 0))
        vol = geometry.get("volume", 0)
        faces = geometry.get("faces", [])
        faces_count = len(faces)
        edges_count = len(geometry.get("edges", []))
        vertices_count = geometry.get("vertices_count", 0)
        is_closed = geometry.get("is_closed_shell", False)

        # Face type distribution
        from collections import Counter
        face_types = Counter(
            f.type if hasattr(f, "type") else f.get("type", "other")
            for f in faces
        )

        # Metric cards row
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Dim X", f"{dims[0]:.1f} mm")
        with m2:
            st.metric("Dim Y", f"{dims[1]:.1f} mm")
        with m3:
            st.metric("Dim Z", f"{dims[2]:.1f} mm")
        with m4:
            st.metric("Volume", f"{vol:.1f} mm^3")
        with m5:
            st.metric("Faces", str(faces_count))

        # Second row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Edges", str(edges_count))
        with c2:
            st.metric("Watertight", "Yes" if is_closed else "No")
        with c3:
            parser_used = geometry.get("parser", "unknown")
            st.metric("Parser", parser_used)

        # Face type distribution
        if face_types:
            with st.expander("Face Type Distribution"):
                type_cols = st.columns(len(face_types))
                for col, (ftype, count) in zip(type_cols, sorted(face_types.items())):
                    with col:
                        st.metric(ftype.capitalize(), str(count))

        # Warnings from parser
        parse_warnings = geometry.get("parse_warnings", [])
        if parse_warnings:
            with st.expander(f"Parse Warnings ({len(parse_warnings)})"):
                for w in parse_warnings:
                    st.warning(w)

    elif st.session_state.get("step_filename"):
        st.info("Loading geometry...")
    else:
        st.info("Upload a STEP file to see geometry details.")


# =========================================================================
#  Main panel: run pipeline
# =========================================================================

def _render_pipeline_execution(sidebar: dict):
    """Execute the pipeline and render progress + results."""
    if not sidebar["generate_clicked"]:
        return

    step_file = st.session_state.get("step_file")
    if step_file is None:
        st.error("No STEP file available. Please upload a file first.")
        return

    material = sidebar["material"]
    material_label = sidebar["material_label"]
    volume = sidebar["volume"]
    tolerances = sidebar["tolerances"]
    api_key = sidebar["api_key"]

    if not api_key:
        st.error(
            "No DeepSeek API key provided. Set the DEEPSEEK_API_KEY "
            "environment variable or enter it in the sidebar."
        )
        return

    st.markdown("---")
    st.subheader("Process Plan Generation")

    # Create pipeline
    pipeline = InferencePipeline(deepseek_api_key=api_key)

    # Progress bar + status
    progress_bar = st.progress(0.0, text="Starting pipeline...")
    status_container = st.empty()

    # Run step-by-step and capture the generator return value
    gen = pipeline.step_by_step(
        step_file, material=material, volume=volume, tolerances=tolerances
    )
    pipeline_result: Optional[PipelineResult] = None

    while True:
        try:
            update = next(gen)
        except StopIteration as exc:
            # exc.value contains the PipelineResult returned by the generator
            pipeline_result = exc.value
            break
        except Exception as e:
            status_container.error(f"Pipeline crashed: {e}")
            pipeline_result = None
            break

        step_name = update["step"]
        status = update["status"]
        progress = update["progress"]

        if status == "running":
            progress_bar.progress(progress, text=f"{step_name}...")
        elif status == "done":
            progress_bar.progress(progress, text=f"Done: {step_name}")
        elif status == "error":
            progress_bar.progress(progress, text=f"ERROR: {step_name}")
            status_container.error(
                f"{step_name} failed: {update['data'].get('error', 'Unknown error')}"
            )
            # The generator returns after an error yield;
            # the PipelineResult is in StopIteration.value
            continue

    progress_bar.empty()
    status_container.empty()

    st.session_state["pipeline_result"] = pipeline_result

    # Render results
    _render_results(pipeline_result, material_label)


def _render_results(result: PipelineResult, material_label: str):
    """Render the pipeline results in the main panel."""
    if not result:
        return

    # --- Errors ---
    if result.errors:
        st.error("Errors encountered during pipeline execution:")
        for err in result.errors:
            st.markdown(f"- {err}")

    # --- Timing summary ---
    st.markdown(f"**Total pipeline time:** {result.elapsed_time:.2f}s")
    if result.step_times:
        time_parts = [f"{k}: {v:.2f}s" for k, v in result.step_times.items()]
        st.caption(" | ".join(time_parts))

    # --- DFM / Rule Engine Results ---
    rule_result = result.rule_result
    if rule_result:
        st.markdown("---")
        _render_rule_results(rule_result)

    # --- Process Plan ---
    plan = result.plan
    if plan:
        st.markdown("---")
        _render_plan(plan, material_label)

        # Post-plan validation
        if result.validation_warnings:
            with st.expander(f"Plan Validation Warnings ({len(result.validation_warnings)})"):
                for w in result.validation_warnings:
                    st.warning(w)

        # Download button
        st.markdown("---")
        _render_download_section(result)

    elif result.errors:
        st.warning("Process plan was not generated due to errors above.")
        # Still show rule engine results as partial output
        st.info(
            "Review the DFM analysis above. You can still get useful "
            "manufacturing insights from the rule engine output."
        )


# =========================================================================
#  Rule engine results rendering
# =========================================================================

def _render_rule_results(rule_result: dict):
    """Render DFM rule-check results: errors and warnings."""
    errors = rule_result.get("errors", [])
    warnings = rule_result.get("warnings", [])
    suggested_ops = rule_result.get("suggested_operations", [])

    st.subheader("DFM Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("DFM Warnings", len(warnings))
    with col2:
        st.metric("DFM Errors", len(errors), delta=None if len(errors) == 0 else f"{len(errors)}")
    with col3:
        st.metric("Suggested Operations", len(suggested_ops))

    # Errors first (critical)
    if errors:
        with st.expander(f"DFM Errors ({len(errors)})", expanded=True):
            for i, err in enumerate(errors):
                severity = err.get("severity", "error")
                msg = err.get("message", str(err))
                suggestion = err.get("suggestion", "")
                source = err.get("source", "")
                fidx = err.get("feature_index", "")

                header = f"[{severity.upper()}] {msg}"
                if fidx != "":
                    header = f"Feature {fidx}: {msg}"

                st.error(header, icon="🚫")
                if suggestion:
                    st.caption(f"**Suggestion:** {suggestion}")
                if source:
                    st.caption(f"*Source: {source}*")
                if i < len(errors) - 1:
                    st.markdown("---")

    # Warnings
    if warnings:
        with st.expander(f"DFM Warnings ({len(warnings)})", expanded=len(errors) == 0):
            for i, warn in enumerate(warnings):
                severity = warn.get("severity", "warn")
                msg = warn.get("message", str(warn))
                suggestion = warn.get("suggestion", "")
                source = warn.get("source", "")
                fidx = warn.get("feature_index", "")

                header = f"[{severity.upper()}] {msg}"
                if fidx != "":
                    header = f"Feature {fidx}: {msg}"

                st.warning(header, icon="⚠️")
                if suggestion:
                    st.caption(f"**Suggestion:** {suggestion}")
                if source:
                    st.caption(f"*Source: {source}*")
                if i < len(warnings) - 1:
                    st.markdown("---")

    # Suggested operations
    if suggested_ops:
        with st.expander(f"Rule-Suggested Operations ({len(suggested_ops)})"):
            ops_data = []
            for op in suggested_ops:
                feed = op.get("feeds_speeds", {}) or {}
                ops_data.append({
                    "Feature": op.get("feature_index", ""),
                    "Operation": op.get("operation", ""),
                    "Tool": op.get("tool_type", ""),
                    "Diameter (mm)": op.get("tool_diameter_mm", ""),
                    "Depth (mm)": op.get("depth_mm", ""),
                    "RPM": feed.get("rpm", ""),
                    "Feed (mm/min)": feed.get("feed_rate_mm_min", ""),
                    "Notes": op.get("notes", "")[:60] + "..." if len(op.get("notes", "")) > 60 else op.get("notes", ""),
                })
            st.dataframe(ops_data, use_container_width=True, hide_index=True)


# =========================================================================
#  Process plan rendering
# =========================================================================

def _render_plan(plan: dict, material_label: str):
    """Render the LLM-generated process plan."""
    st.subheader("Generated Process Plan")

    # Part summary
    summary = plan.get("part_summary", {})
    if summary:
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("Material", summary.get("material", material_label))
        with s2:
            size = summary.get("overall_size_mm", [0, 0, 0])
            st.metric("Size", f"{size[0]}x{size[1]}x{size[2]}" if len(size) == 3 else str(size))
        with s3:
            st.metric("Complexity", summary.get("complexity_level", "N/A"))
        with s4:
            st.metric("Setups", summary.get("estimated_setups", "N/A"))

    # Total time
    total_time = plan.get("total_estimated_time_minutes", 0)
    if total_time:
        st.info(f"**Total Estimated Machining Time:** {total_time:.1f} minutes")

    # Operations table
    operations = plan.get("operations", [])
    if operations:
        st.markdown("### Operations")
        ops_rows = []
        for op in operations:
            tool = op.get("tool", {})
            cp = op.get("cutting_parameters", {})
            feat_refs = op.get("features_referenced", [])
            ops_rows.append({
                "Step": op.get("step_number", ""),
                "Operation": op.get("operation_name", ""),
                "Tool Type": tool.get("type", ""),
                "Diameter (mm)": tool.get("diameter_mm", tool.get("diameter", "")),
                "Strategy": op.get("strategy", ""),
                "RPM": cp.get("rpm", ""),
                "Feed (mm/min)": cp.get("feed_rate_mm_per_min", ""),
                "DOC (mm)": cp.get("depth_of_cut_mm", ""),
                "Coolant": op.get("coolant", ""),
                "Time (min)": op.get("estimated_time_minutes", ""),
                "Machine": op.get("machine_type", ""),
                "Features": ", ".join(feat_refs) if feat_refs else "",
            })

        st.dataframe(ops_rows, use_container_width=True, hide_index=True)

        # Operation notes
        with st.expander("Operation Details"):
            for op in operations:
                notes = op.get("notes", "")
                if notes:
                    st.markdown(
                        f"**Step {op.get('step_number', '?')} - "
                        f"{op.get('operation_name', 'Unknown')}:**"
                    )
                    st.caption(notes)

    # DFM notes
    dfm_notes = plan.get("dfm_notes", [])
    if dfm_notes:
        with st.expander(f"DFM Notes ({len(dfm_notes)})"):
            for note in dfm_notes:
                st.markdown(f"- {note}")

    # Alternative approaches
    alternatives = plan.get("alternative_approaches", [])
    if alternatives:
        with st.expander(f"Alternative Approaches ({len(alternatives)})"):
            for i, alt in enumerate(alternatives):
                desc = alt.get("description", "No description")
                tradeoffs = alt.get("tradeoffs", "")
                est_time = alt.get("estimated_time_minutes", "N/A")
                st.markdown(f"**Alternative {i+1}:** {desc}")
                if tradeoffs:
                    st.caption(f"*Tradeoffs: {tradeoffs}*")
                if est_time:
                    st.caption(f"*Estimated time: {est_time} min*")
                st.markdown("---")


# =========================================================================
#  Download section
# =========================================================================

def _render_download_section(result: PipelineResult):
    """Render download buttons for the full JSON plan."""
    st.subheader("Downloads")

    plan = result.plan
    if not plan:
        return

    # Build comprehensive JSON output
    download_data = {
        "plan": plan,
        "rule_engine_result": {
            "warnings": result.rule_result.get("warnings", []),
            "errors": result.rule_result.get("errors", []),
            "suggested_operations": result.rule_result.get("suggested_operations", []),
        },
        "plan_validated": result.plan_validated,
        "validation_warnings": result.validation_warnings,
        "elapsed_time": result.elapsed_time,
        "step_times": result.step_times,
        "pipeline_errors": result.errors,
        "features_extracted": [
            {k: v for k, v in f.items() if k != "face_indices"}
            for f in result.features
        ],
        "geometry_summary": {
            "faces": len(result.geometry.get("faces", [])),
            "edges": len(result.geometry.get("edges", [])),
            "vertices": result.geometry.get("vertices_count", 0),
            "volume": result.geometry.get("volume", 0),
            "dimensions": result.geometry.get("overall_dimensions", (0, 0, 0)),
            "watertight": result.geometry.get("is_closed_shell", False),
        },
    }

    # Convert numpy types to native Python for JSON serialization
    def _convert_to_native(obj):
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        if isinstance(obj, dict):
            return {k: _convert_to_native(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_convert_to_native(v) for v in obj]
        return obj

    download_data = _convert_to_native(download_data)

    # JSON download
    json_str = json.dumps(download_data, indent=2, ensure_ascii=False)
    st.download_button(
        label="Download Full Plan (JSON)",
        data=json_str,
        file_name="process_plan.json",
        mime="application/json",
        use_container_width=True,
    )

    # Operations-only CSV
    ops = plan.get("operations", [])
    if ops:
        import io
        import csv

        csv_buffer = io.StringIO()
        if ops:
            # Flatten operations for CSV
            fieldnames = [
                "step_number", "operation_name", "tool_type", "tool_diameter_mm",
                "strategy", "rpm", "feed_rate_mm_per_min", "depth_of_cut_mm",
                "coolant", "estimated_time_minutes", "machine_type",
            ]
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for op in ops:
                row = {
                    "step_number": op.get("step_number", ""),
                    "operation_name": op.get("operation_name", ""),
                    "tool_type": op.get("tool", {}).get("type", ""),
                    "tool_diameter_mm": op.get("tool", {}).get("diameter_mm", ""),
                    "strategy": op.get("strategy", ""),
                    "rpm": op.get("cutting_parameters", {}).get("rpm", ""),
                    "feed_rate_mm_per_min": op.get("cutting_parameters", {}).get("feed_rate_mm_per_min", ""),
                    "depth_of_cut_mm": op.get("cutting_parameters", {}).get("depth_of_cut_mm", ""),
                    "coolant": op.get("coolant", ""),
                    "estimated_time_minutes": op.get("estimated_time_minutes", ""),
                    "machine_type": op.get("machine_type", ""),
                }
                writer.writerow(row)

        st.download_button(
            label="Download Operations (CSV)",
            data=csv_buffer.getvalue(),
            file_name="operations.csv",
            mime="text/csv",
            use_container_width=True,
        )


# =========================================================================
#  Main entry point
# =========================================================================

def main():
    """Streamlit app entry point."""
    _init_session_state()
    _inject_css()

    sidebar = _render_sidebar()

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "d2m v0.1.0 -- Phase 0 Prototype"
    )

    _render_header()
    st.markdown("---")
    _render_file_upload()

    if sidebar["generate_clicked"]:
        _render_pipeline_execution(sidebar)


if __name__ == "__main__":
    main()
