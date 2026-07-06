EXP HDF5 Phase-Space Output
===========================

.. index:: HDF5

Overview
--------

Creation of EXP HDF5 phase-space snapshots is configured using the
``outhdf5`` entry in the ``Output`` stanza of the main
:ref:`YAML configuration <yamlconfig>`.

The EXP HDF5 output path is orchestrated by ``src/OutHDF5.cc``.  Its
role is to collect phase-space and per-particle metadata from the
runtime particle/component structures, then serialize them into an
HDF5 snapshot.

At a high level:

1. ``OutHDF5`` creates an output file and snapshot-level metadata.
2. It iterates over active components/particle containers.
3. It writes core phase-space arrays (mass, position, velocity, etc.).
4. It invokes helper/adapter routines in force implementations and
   particle-related structures to emit additional derived or
   model-specific fields.
5. It finalizes the file with attributes needed for downstream
   analysis and restart compatibility.

This design keeps HDF5 writing centralized while allowing each physics
module to contribute fields in a modular way.

File Structure
--------------

A typical EXP HDF5 snapshot is organized around:

- **global file attributes** (snapshot metadata),
- **component groups** (one per EXP component),
- **datasets within each component** for particle properties.

Conceptually:

.. code-block:: text

   /
   ├── Attributes
   │   ├── time
   │   ├── step
   │   ├── code_version        (if available)
   │   └── ...
   ├── components/
   │   ├── <component_0>/
   │   │   ├── Attributes
   │   │   │   ├── num_particles
   │   │   │   ├── component_name
   │   │   │   └── ...
   │   │   ├── m               (N)
   │   │   ├── x, y, z         (N each)
   │   │   ├── u, v, w         (N each)
   │   │   ├── id / index      (optional, N)
   │   │   ├── aux_*           (optional)
   │   │   └── force-added fields (optional)
   │   └── <component_1>/
   │       └── ...
   └── ...

.. note::

Exact group/dataset names may vary slightly with component type and
output options.

The defining behavior is that ``OutHDF5`` writes canonical phase-space
fields and then appends optional/helper-provided fields.

Core Particle Datasets
----------------------

For each component, the core phase-space representation is written in
**structure-of-arrays** form:

- ``m``: particle mass
- ``x``, ``y``, ``z``: Cartesian position
- ``u``, ``v``, ``w``: Cartesian velocity

All arrays have length ``N = num_particles`` in that component.

Optional canonical fields may include:

- ``index`` (or equivalent particle identifier)
- integer or floating auxiliary arrays (e.g. ``aux_int_*``, ``aux_float_*``)

Data Types and Precision
------------------------

The writer supports floating-point output compatible with the
in-memory particle representation and/or configured output
precision. In practice:

- kinematic/scalar fields are written as ``float`` or ``double`` datasets,
- integer-like metadata (IDs, discrete tags) are written as integer datasets.

If mixed precision is enabled by upstream code paths, fields may not
all share the same floating type. Consumers should inspect each
dataset dtype rather than assume uniform precision.

Module/Force-Contributed Fields
-------------------------------

``OutHDF5.cc`` delegates module-specific output to helper methods in
force implementations and related particle structures. This enables
adding fields such as:

- potentials,
- accelerations,
- diagnostics or basis-expansion terms,
- solver- or force-specific per-particle quantities.

Expected behavior:

- these datasets are aligned 1:1 with the particle ordering used for
  core phase-space arrays,
- helpers only write fields they own/understand,
- absent modules imply absent optional datasets.

.. important::

   Downstream analysis scripts should treat non-core fields as
   optional and test for dataset existence.

Particle Ordering and Alignment
-------------------------------

Within a component group, all per-particle arrays are expected to use
the same row index convention:

- entry ``i`` in ``x``, ``y``, ``z``, ``u``, ``v``, ``w``, ``m`` (and
  optional arrays) refers to the same particle.
- if ``index``/ID is present, it provides a stable external key for
  cross-snapshot tracking.

When joining fields, use either:

1. direct array index alignment (fast path), or
2. explicit key alignment through ``index`` if reordering is possible
   in your pipeline.

Metadata and Attributes
-----------------------

Snapshot- and component-level HDF5 attributes are used to capture
context needed for interpretation and reproducibility, commonly
including:

- simulation time,
- step/cycle number,
- component identity and particle counts,
- run/build annotations (if configured).

Consumers should read attributes first and use them to validate assumptions (units, step identity, component semantics).

Compatibility Notes
-------------------

- The HDF5 output path is designed to coexist with legacy formats.
- Existing ASCII workflows remain usable where supported by EXP
  input/output logic.
- HDF5 should be preferred for modern analysis due to typed datasets,
  compression support, and robust metadata handling.

Recommended Reader Strategy
---------------------------

When building analysis tools:

1. Open file-level attributes and record snapshot metadata.
2. Enumerate component groups dynamically (do not hardcode names).
3. Read required core datasets (``m``, ``x``, ``y``, ``z``, ``u``, ``v``, ``w``).
4. Probe for optional datasets (``index``, aux fields, force-specific fields).
5. Validate per-component array lengths before combining fields.
6. Gracefully skip unknown optional fields.

Minimal Python Example
----------------------

.. code-block:: python

   import h5py

   with h5py.File("snapshot.h5", "r") as f:
       # Example: inspect top-level metadata
       for k, v in f.attrs.items():
           print("file attr", k, v)

       comps = f.get("components", None)
       if comps is None:
           raise RuntimeError("No 'components' group found")

       for cname, g in comps.items():
           print(f"\\nComponent: {cname}")
           n = g.attrs.get("num_particles", None)
           print("N =", n)

           # Required core fields (typical)
           m = g["m"][:]
           x = g["x"][:]; y = g["y"][:]; z = g["z"][:]
           u = g["u"][:]; v = g["v"][:]; w = g["w"][:]

           # Optional fields
           idx = g["index"][:] if "index" in g else None

           # Enumerate extra module-provided fields
           core = {"m", "x", "y", "z", "u", "v", "w", "index"}
           extras = [name for name in g.keys() if name not in core]
           print("extra fields:", extras)

Developer Notes
---------------

For contributors extending output:

- Keep new datasets strictly per-particle and shape-consistent with
  component ``N``.
- Prefer explicit names and add matching attribute documentation when
  semantics are non-obvious.
- Avoid changing meaning of existing dataset names across releases.
- If adding force/helper fields, ensure they are emitted only when
  valid and initialized.
