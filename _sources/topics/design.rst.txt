.. _design:

Software design goals and features
==================================

The mathematical and algorithmic structure of basis function expansion
(BFE) technique is common to all variants of the method.
Object-oriented software patterns naturally promote code reuse by
allowing the programmer to implement algorithms generally and allow
variants to override the general case only when necessary.  Moreover,
the object-oriented approach allows the compiler to enforce the
underlying mathematical and physical relationships that the code
represents.  This approach makes the code easier to maintain, verify
and debug.

The classes are organized into major abstract classes the represent
common functions and relations between functions common to n-body
simulations and the BFE method in particular:

.. index:: Particle

* ``Phase space``. Each phase-space point is described by a
    ``Particle``, which contains the mass, position, velocity,
    and an arbitrary number of user-defined attributes
    (e.g. particular non-collisionless properties such as chemical
    state or various per particle diagnostics such as computational
    effort).

.. index:: Particle, Component,  ComponentContainer

* ``Distributions``. Particles are grouped together into a
    ``Component`` container.  A ``Component`` represents a particular
    distinct phase-space distribution.  For example, EXP uses
    individual components to represent astronomical entities such as a
    disks and dark-matter halos.  A force method appropriate for the
    geometry of each phase-space distribution is associated with each
    component (``PotAccel``, see below).  The ``Component`` instances
    are gather into a container, the ``ComponentContainer``.  The
    ``ComponentContainer`` instance, for example, triggers the
    evaluation of the acceleration for every particle in each
    component.  Specifically, the time step routine calls the
    ``compute_potential()`` of the simulation's ``ComponentContainer``
    instance to begin a force evaluation.

.. index::  PotAccel, Basis, AxisymmetricBasis, Sphere, Cylinder, Direct


* ``Force methods``.  The ``PotAccel`` class defines the
    core interface for describing a gravitational potential and
    acceleration.  From this abstract base class, the properties
    specific to basis function expansions are *layered on* by the
    derived class ``Basis``.  Further specializations include
    details specific to harmonic expansions in
    ``AxisymmetricBasis`` and the standard spherical and
    cylindrical geometries appropriate for halos and disks in
    ``Sphere`` and ``Cylinder``, respectively.  Most
    non-basis classes, such as ``Direct`` which defines a direct
    ring code have ``PotAccel`` as the parent class.

.. index:: ExternalForce, PeriodicBC

* ``External forces``. The class ``ExternalForce`` provides additional
    possibly time-dependent analytic or self-consistent forces to be
    applies to any or every component.  These methods can be very
    general manipulators of the phase space, not necessarily forces
    per se.  For example, EXP uses an external force class called
    ``PeriodicBC`` to enforce periodic boundary conditions.  The
    user-specified external forces are gather up into an
    ``ExternalForce`` list and evaluated at each step by the
    ``ComponentContainer``.  Per particle accelerations may be added
    to each particle's acceleration vector if appropriate.

.. index:: Output, OutputContainer, OutLog, OrbTrace, OutCoef

* ``Output routines``.  The ``Output`` base class
    integrate over phase-space components to provide summary
    statistics of various sorts and snapshots of the phase space
    itself.  Each ``Output`` instance either integrates over the
    entire phase space or individually specified phase-space
    components.  For example, the ``OutLog`` class provides the
    standard global quantities of center of mass and velocity, angular
    momentum, kinetic and potential energies, etc. for each component
    and the entirely.  The ``OrbTrace`` class records the
    trajectory of a list of specific particles.  The ``OutCoef``
    class records the basis expansion coefficients.  All of these
    ``Output`` instances are gather up into an
    ``OutputContainer``.  After each time step, each instance is
    *asked* whether it wants to run.  The run frequency is
    controlled by :ref:`input parameters <exp-config>`).

As described in :ref:`EXP time stepping <multistep>`, the Hamilton
equations are solved by a *kick-drift-kick* version of the
time-centered leapfrog algorithm.  In principle, time evolution could
(and perhaps should) be defined by an evolution operator class.  This
may be done for a future version of EXP.  At present, the time
evolution is driven by a calls to the ``ComponentContainer`` instance
to evaluate the accelerations.

Overall organization of the code
================================

.. index:: ComponentContainer, ExternalCollection, OutputContainer

The ``main()`` routine is defined in ``src/expand.cc``.  In essence, the
``main()`` calls three subroutines:

1. ``begin_run()``: this code initializes the three key container objects:

  - The ``ComponentContainer`` will hold phase-space and
    force definitions for each distinct component.  For example, a
    three-dimensional flattened disk or an approximately spherical
    halo along with its associated force would each be represented by
    a particular ``Container`` instance.  The
    ``begin_run()`` routine instantiates particular phase-space
    components as defined in the YAML configuration and adds them to
    the ``ComponentContainer``.

  - The ``ExternalCollection`` defines force methods that are
    applied to phase space components but are not defined by
    components.  For example, an external force, such as an analytic
    tidal field, would be instantiated as a member of the
    `ExternalCollection`.  This collection may have zero
    members.

  - The ``OutputContainer`` keeps a collection of procedures
    that may operate on each component or specific components in the
    ``ComponentContainer`` at some time step frequency
    defined by the parameter specification for each ``Output``
    method.  These are specified for construction in the YAML
    configuration.

2. ``do_step()`` inside of its time-step loop. ``do_step`` implements
   the kick-drift-kick leapfrog time-integration algorithm described in
   :ref:`multistep <multistep>`.

3. ``clean_up()`` calls the ``OutputContainer`` run method one last
   time, and then deletes the three container instances defined by
   ``begin_run()``.


Parallel usage
==============

.. index::
   triple: MPI; parallel; OpenMP

EXP is designed to use MPI for internode communication and
parallelization and POSIX threads (pthreads) and OpenMP for intranode
parallelization.  Although MPI can be used exclusively, without
multiple threads per process by starting one process for every core on
each node, basis tables and other data will be duplicated by these
heavy weight processes.  This may lead to poor allocation of memory
resources and out-of-core conditions.  By using multiple threads per
process on compute nodes with multiple cores, the storage internal
arrays and tables will not be duplicated.

The `Global` stanza (see :ref:`YAML config <yamlconfig>`) allows the
user to specify the number of threads per process using the ``nthrds``
parameter.  For example, on a cluster where nodes have 20 cores,
specifying ``nthrds: 20`` and one process per node using

.. code-block:: bash

   mpirun -bind-to none -npernode 1 exp -f myjob.yml

or for a Slurm job

.. code-block:: bash

   srun --ntasks-per-node=1 exp -f myjob.yml

allow code bottlenecks to using pthreads rather than MPI for
parallelization.  For MPI parallelization only, specify ``nthrds: 1``,
which is the default value.  Not all force methods are thread aware,
but many are.

Both pyEXP and EXP are use OpenMP to parallelize bottleneck loops. The
`FieldGenerator` in pyEXP, in particular, can achieve linear scaling
with the number of available cores.  To take advantage of this,
specify the `OMP_NUM_THREADS` environment variable and set it to the
number of available cores on your machine.  For example, in Bash:

.. code-block:: bash

   export OMP_NUM_THREADS=16

for an 16-core architecture.

