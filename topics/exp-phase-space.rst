.. _exp-phase-space:

The EXP phase-space format
==========================

.. index: PSP

Why another format?
-------------------

When EXP was written, there was no common N-body format.  The
typical structures were serial lists of each phase-space variable
:math:`m_1, m_2, \ldots, m_N, x_1, x_2, \ldots, y_i, \ldots,`.  On the
other hand, for the object-orientated design strategy described in
:ref:`design`, the smallest object is the particle phase space
described by :math:`m_i, \mathbf{x}_i, \mathbf{v_i}, \ldots`, for
:math:`i=1,\ldots, N`.  Similarly, each distinct astronomical component
(think *stellar disk*, *dark-matter halo*, etc.) is
described by a group of phase-space particle along with any geometric
or physical parameters common the the component.  That is, an
object-oriented code motivates a phase-space description which not
only contains the phase-space elements but the associated methods for
computing the gravitational field together with all information
required to reproduce the fields, along with any common
properties of all components together, such as the current time.

The result was the EXP phase-space protocol (PSP).  This
hierarchical format begins with a header which describes the current
time and the number of components in the phase space.  This
\emph{master} header is then followed by a description of each
component (i.e. the name, the gravitational force method with all the
parameters necessary for generating the force-computation method, and
the phase-space particles themselves).  The code designed or user may
choose to concatenated successive time slices, multiple phase-spaces,
or put them in separate files.  Overall strategy the strategy of the
PSP is a self-describing format that keeps the parameters together
with phase-space details as a way of ensuring that the provenance of
the particular phase space description is clear.  This self-describing
phase-space format also expedites restarts.  The PSP format is fully
IEEE compliant and can be moved from one machine to another without
fear of incompatibility.  This format does not enforce endianness,
however, that is rarely a concern these days since there are very few
big endian architectures left.

Most of the PSP features have been ported directly to an HDF5
implementation in the latest EXP release. We currently recommend HDF5
over the native PSP for portable reading with Python using
:code:`h5py`. For a full description of the HDF5 implementation,
please see :doc:`output_hdf5`.


Implementation overview
-----------------------

Initialization
^^^^^^^^^^^^^^

For ease of construction, EXP initializes its components with
simplified ASCII or HDF5 files that describe the particles and the
associated geometric and force methods are provided in the
configuration file as previously described.  The ASCII format is
standard table of columns and the HDF5 schema (described) below is
easily constructed on the fly (e.g. using Python :code:`h5py`).  The
:code:`Component` class automatically detects HDF5 input files,
otherwise, it defaults to ASCII.

.. important::
   While the main PSP and HDF5 formats store all components
   in separate blocks, the initialization files describe a single
   component only.  You need one initialization file for every
   component.


ASCII
~~~~~

Each phase-space particle is described by the mass, followed by the
vector position and velocity, followed by an arbitrary number of
intger and floating-point values.  These are described in ascii input
by the first line contains the following three integer values:

1. the number of bodies, :math:`N`,

2. the number of integer attributes, :math:`n_i`, per body

3. the number of real (float or double) attributes, :math:`n_d`, per body

The next :math:`N` lines are space delimited fields containing the
information for each particle.

HDF5
~~~~

.. index: HDF5

The HDF5 schema takes the following form::
  /
  ├── Attributes
  │ ├── num_particles (int)
  │ ├── num_aux_ints (int)
  │ └── num_aux_floats (int)
  └── particles/ (Group)
  ├── index (Dataset, unsigned long)
  ├── m (Dataset, float/double)
  ├── x, y, z (Datasets, float/double)
  ├── u, v, w (Datasets, float/double)
  ├── aux_int_0, aux_int_1, ... (Datasets, int)
  └── aux_float_0, aux_float_1, ... (Datasets, float/double)

Main features:

- The design goal is keeping like data together and using chunking,
  bit shuffling, and compression at the HDF5 level to achieve up to a
  factor of 5 savings in file size for float32 and a factor of 2.5
  savings for float64.
- The index and aux_int_*, aux_float_* fields are optional.
- This schema is a precise mapping of the current body file data
  fields, except for the inverse ordering. One could make this more
  Gadget-like, but that would muddy the clarity here.
- We separate pos into x, y, z (and vel into u, v, w) to simply the
  std::variant coding to allow both float and double arrays. It is
  possible that consolidating into 2d arrays could be more
  efficient. But this is easier to code.
- The precision of the float data type is deduced for each dataset
  independently. One could mix precision between m, x, y, z, u, v, w
  if desired.
- The converter routine hdf5bods was initially designed to compress
  body files and it achieves that goal. It is implemented with OpenMP
  which gives some modest performance gains (but not MPI). A particle
  body files requires 10 seconds for conversion on a laptop.
- The Component class checks whether the specified body file is HDF5
  and reverts to the original ascii method if not; so all of the prior
  behavior is retained for compatibility.
- If the optional index field (unsigned long) exists, it will populate
  the EXP Particle.indx field. Similarly, the stand-along conversion
  routine has can read and write the index field for consistency with
  the original ASCII body table format.
- The stand-alone hdf5bods converter has support for multiple HDF5
  compression filters for testing. The default GZip has the highest
  compression ratio but it also takes the most CPU time.

Native binary output
^^^^^^^^^^^^^^^^^^^^

EXP phase-space output is in binary PSP format.  The floating-point
precision may be either single or double and specified by the user on
configuration.  There are two versions of PSP writers in EXP: one that
gather all particle information at the root node into a single
phase-space structure before writing to disk from the root node, and
one that using MPI-IO to write from each node.  Throughput will depend
on the cluster hardware.  In principle, we could implement a true
parallel writing scheme to many files with either an asynchronous
concurrent thread or post-processing utility to consolidate the
phase-space.  This is worth doing, especially as our ability to
compute dynamics seems to be outpacing our ability to write
phase-space files to storage.

Because the phase-space dumps may be large, considerable disk space is
saved by using the single- rather than double-precision floating
representation if analysis does not require the full precision.  It is
possible to restart a simulation from either a single- or
double-precision PSP file, but it makes most sense to use
double-precision PSP for checkpoints.


Phase-space file utilities
--------------------------

.. index: PSP; utilities

The following utilities manipulate the phase-space files:

- **pspinfo** reads the master header and the header for each
  component in the PSP format and writes these fields to the standard
  output.

- **psp2ascii** unpacks the PSP file into ascii files, one for each
  component with the same overall structure as the ascii input files.
  The one difference with the ascii input files is that the mass,
  position and velocity is followed by the value of the gravitational
  potential.

- **psp2hdf5** make a Gadget2-style HDF5 file from a PSP file and a
  Gadget template file for porting PSP to other N-body codes that use
  Gadget format.  No cosmological parameters are set.  No subgrid
  parameters will be set.  Use the numerical flags to assign component
  names to Gadget particle types.

- We do not provide a tool for converting between **native** binary
  PSP and **HDF5** PSP format at this point.  We recommending using
  the :code:`outhdf5` writer directly to produce HDF5 files from EXP.

- Early versions of EXP imported and exported to :index:`tipsy` files.
  The utilities `ascii2psp, psp2tipsy, tipstd2psp` may be used to make
  these conversions.  We are not generally using tipsy format at this
  time and have not maintained these routines in many years, so user
  beware.


Binary file-format details
--------------------------

.. index: pair: PSP; format

The binary phase space structure consists of a master header followed
by *stanzas*.  Each stanza is has a header followed by the phase
space.  The master header is:

.. code-block: c++

    struct MasterHeader {
      double time;
      int ntot;
      int ncomp;
    };

The parameters are:

- `time` - the current time
- `ntot` - total number of bodies in all components
- `ncomp` - number of components

Each stanza begins with a header:

.. code-block: c++
   
   struct ComponentHeader {
   int nbod;
   int niatr;
   int ndatr;
   int ninfochar;
   char info[ninfochar];
   };

which describes the number of bodies in the component (`nbod`),
the number of integer attributes (`niatr`), the number of
double components (`ndatr`), number of characters reserved for
the info string (`ninfochar`) and the info string itself.  The
default size is `ninfochar=1024`.
