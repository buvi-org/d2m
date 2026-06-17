# SubCAD Program Generation

Stage 3 converts each frozen Stage 2 English requirement into a SubCAD program.

## Boundary

- Generate one program per single-metal-part requirement.
- Do not change, simplify, or reinterpret the English requirement.
- If the requirement asks for a feature that SubCAD cannot currently express,
  write the closest honest SubCAD program and record the unsupported feature in
  the program metadata as a gap.
- Do not use imported STEP, STL, mesh, or opaque geometry as a shortcut.
- Do not add assemblies, fasteners, bearings, springs, bushings, rubber,
  plastic, electronics, labels, or bought-out items.

## Output Convention

Runnable program files live under:

`docs/subcad_limit_test/subcad_programs_py/`

Each requirement gets one standalone Python file:

`agent_###/smp-###-##_part_name.py`

Each Python file:

- imports `Stock` from `subcad`
- defines a variable named `part`
- keeps the requirement ID, part name, source idea, coverage notes, known gaps,
  and review notes as top-of-file comments

The intermediate batch JSON files in `docs/subcad_limit_test/subcad_programs/`
are metadata containers from the parallel generation step. The `.py` files are
the primary artifacts for execution and review.

## Minimum Program Shape

```python
from subcad import Stock

part = (
    Stock.rectangular(100, 50, 12, material="aluminum_6061")
    .drill(diameter=6, cx=20, cy=25, depth=12)
    .slot(width=10, length=40, depth=12, cx=50, cy=25)
    .chamfer(width=1.0)
)
```

For round-bar parts, use `Stock.cylindrical(diameter, height, material=...)`
and add available turning/cylindrical operations where they match the
requirement.

Generated programs are drafts until executed and reviewed against STEP/STL
artifacts.
