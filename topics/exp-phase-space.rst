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
\S\ref{sec:design}, the smallest object is the particle phase space
described by :math:`m_i, \mathbf{x}_i, \mathbf{v_i}, \ldots`, for
:math:`i=1,\ldots, N`.  Similarly, each distinct astronomical component
(think \emph{stellar disk}, \emph{dark-matter halo}, etc.) is
described by a group of phase-space particle along with any geometric
or physical parameters common the the component.  That is, an
object-oriented code motivates a phase-space description which not
only contains the phase-space elements but the associated methods for
computing the gravitational field together with all information
required to reproduce the fields, together along with any common
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

A port of the PSP features to HDF would be straightforward and is
planned for a later release.


Implementation overview
-----------------------

The PSP format is a binary format.  However, for ease of construction,
EXP initializes its components with ascii files that describe
the particles and the associated geometric and force methods are
provided in the configuration file as previously described.  Each
phase-space particle is described by the mass, followed by the vector
position and velocity, followed by an arbitrary number of intger and
floating-point values.  These are described in ascii input by the
first line contains the following three integer values:

1. the number of bodies, :math:`N`,

2. the number of integer attributes, :math:`n_i`, per body

3. the number of real (float or double) attributes, :math:`n_d`, per body

The next :math:`N` lines are space delimited fields containing the
information for each particle.

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

- Early versions of EXP imported and exported to :index:`tipsy` files.
  The utilities `ascii2psp, psp2tipsy, tipstd2psp` may be used to make
  these conversions.  I am not generally using tipsy format at this
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
