.. _faq:

.. _faq-EXP-bs-cmp:


Are there pre-compiled versions of pyEXP and EXP?
-------------------------------------------------

Yes! We have a Docker containers for the Intel/AMD 64 and ARM64
architectures that will run under Linux, MacOS and Windows (using
WSL).  These will give you access to both the simulation code, EXP,
and the Python module, pyEXP using Jupyter Notebooks and Lab without
any additional configuration or code building.

Super quick start: download `this Bash script
<https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox>`_
and run it.  This will download the Docker image and start a Jupyter
notebook by default.  Use the `-t` flag for an interactive terminal.
Use the `-h` flag for additional options.  For further details and
links to installing Docker, see `this README
<https://github.com/EXP-code/EXP-container/tree/main/Docker>`_.

A native installation will be a bit faster and allow you to fine tune
package versions in HPC environments. See :ref:`the Installation Guide
<intro-install>` for details.

I only want pyEXP, do I need C++ to compile EXP?
------------------------------------------------

Yes, EXP is an C++ library with Python support provided by
`pybind11`_.  So, you need to compile the C++ library first.  However,
you can compile pyEXP without the N-body code itself.  Please see
:ref:`the Installation Guide <intro-install>` for compilation and
configuration details.

.. _pybind11: https://pybind11.readthedocs.io/

Why would I use EXP rather than pyEXP?
--------------------------------------

The EXP N-body code is designed to accurately model disequilbria from
modest satellite interactions, the gravitational coupling between
different galaxy components, and model internal instabilities.  The
bases used in EXP are also suitable for Hamiltonian perturbation
theory calculations.  This provides a self-consistency check and path
to understanding the non-linear development of linear predictions.
The EXP N-body code *will not* work well for major mergers!

pyEXP uses the same library routines as EXP but applies to analyses of
existing simulations done with EXP or most well-known cosmological
N-body codes.  The EXP code base provides stand-alone Unix routines
for these analyses, too.  If you want to analyze existing N-body
simulation output and prefer the Jupyter/Python ecosystem, pyEXP is
what you want.


What hardware do I need to run EXP and pyEXP?
---------------------------------------------
EXP and pyEXP can run on a wide variety of hardware, from laptops and
HPC clusters.  EXP and pyEXP can make use of multiple cores on a single laptop
or compute node using a combination of POSIX threads and OpenMP.

pyEXP in particular is optimized to run on a single node.  In Linux
you can use the environment setting to tell pyEXP to use 8 cores:

.. code-block:: bash

   export OMP_NUM_THREADS=8

This will speed up your mSSA computation in particular.

The core EXP libraries use `MPI <https://www.mpi-forum.org/>`_
which allows EXP (and pyEXP in some instances) to use many compute nodes.
While this is key for simulations with large numbers of particles,
pyEXP can be run on a cluster as well.  See the `pyEXP examples repo
<https://github.com/EXP-code/pyEXP-examples>`_ for some sample scripts
that use MPI.

Some of the core force implementations in EXP have GPU
implementations.  Even a simple commodity gaming card provides enough
power to allow you to easily perform a simulation with 1 million
particles.  Moreover, EXP can be run on GPU clusters, enabling
simulations of 100 million particles and larger.  For example, a
galaxy halo simulation on 8 NVidia V100 GPU cards will take
approximately 12 wall clock hours for 10 Gyr of simulation for a
Milky-Way-like model.  Similar throughput for a CPU cluster requires
approximately 512 cores.

How do I restart EXP from a checkpoint?
---------------------------------------

EXP uses Output routines to write phase space files to disk at regular
intervals. The main phase-space output routines are:

  =============     ===========
  Output type       Explanation
  =============     ===========
  outpsp            Writes single-precision binary N-body phase-space
                    in PSP format.
  outpsq            As in `outpsp` but each process writes in parallel
                    for runtime efficiency.
  outchkpt          Writes double-precision binary N-body phase-space
                    into a single file.
  outchkpq          As in `outchkpt` but each process writes in parallel
                    for runtime efficiency.
  =============     ===========

Each of these output routines takes the integer argument `nint`
describing the number of steps between each output.  These routines
will construct a unique file name based on the `runtag` and file type.
You can override this with the `filename` argument.  The first two in
the table above make sequentially index snapshots.  These are intended
to enable post-processing tasks.  The second two retain the final and
penultimate checkpoints only.

For example, assume that you are running simulation with 4000 time
steps and want a snapshot every 100 steps and a checkpoint every 1000
time steps. Your configuration might look like this:

.. code-block:: yaml

   Output:
     - id : outpsq
       parameters : {nint : 100}
     - id : outchkptq
       parameters : {nint : 1000}

This will write snapshot and checkpoint files of the following form:
`SPL.<runtag>.<xxxxx>` and `SPL.<runtag>.chkpt` where `runtag` is the
parameter specified in the `Global` section of the EXP YAML
configuration and `xxxxx` is a five-digit zero-padded number that
identifies the snapshot.  The previously written checkpoint has the
`.bak` suffix.  You can restart EXP from a snapshot checkpoint by
specifying one of these file names as the `infile` parameter.  For
example, assume that your run is tagged by `run001` and that you
want to restart from the last checkpoint:

.. code-block:: yaml

   Global:
     runtag: run001
     infile: SPL.run001.chkpt

EXP will read the checkpoint file `SPL.run001.chkpt`, check for
consistency with the parameters in the current configuration file, and start
from that point.


My HPC cluster does not have the required dependencies.  What are my options?
-----------------------------------------------------------------------------

See next question...

Can I run EXP or pyEXP in a container?
--------------------------------------

Ask your HPC administrators about running applications in containers.
This will help you avoid module conflicts and non-standard development
environments with missing dependencies.

We have had good success with `Apptainer <https://apptainer.org/>`_
(formerly known as `Singularity`).  Apptainer containers provide all
of the libraries and executable objects necessary to run EXP as an MPI
application in a Linux environment of their choosing.

Most likely, your HPC admin will have recommendations for a base
container OS image that will work with your cluster.  There are two
ways of getting EXP into a container:

1. Building natively on an OS instance that is the same as your target
   container.  Installing the OS in VirtualBox is a good strategy if
   you do not have a native installation. Then you can copy the
   compiled EXP into the container. This `repo
   <https://github.com/EXP-code/EXP-apptainer>`_ gives a simple
   example of this approach for an Ubuntu image.

2. You can build EXP inside the container.  This is more
   self-contained but will require some work.  See `this link
   <https://apptainer.org/user-docs/3.1/build_a_container.html>`_ for
   generic instructions.

3. The NVidia people have developed the `HPC Container Maker
   <https://github.com/NVIDIA/hpc-container-maker>`_, a Python tool
   called `hpccm` for generating an Apptainer/Singularity definition
   file using base images for Linux distributions with Cuda support.
   Our `repo <https://github.com/EXP-code/EXP-apptainer>`_ also gives
   an `hpccm` recipe for an Ubuntu image.  The container includes EXP
   and pyEXP with AstroPy, NumPy, Matplotlib, and mpi4py. EXP in this
   container has been tested but remains experimental (esp. for pyEXP).
   Please provide feedback and bug reports on this and please consider
   contributing your working recipe to `our EXP repo
   <https://github.com/EXP-code/EXP-apptainer>`_!

Some HPC centers are exploring Kubernetes, also known as K8s.  This is
an open-source system for automating deployment, scaling, and
management of containerized applications.  We have no experience with
EXP as a Kubernetes app.  So, again, please share your experience!

I got a "seg fault", now what do I do?
--------------------------------------

First of all, we are sorry!  Please report the problem in our `issue tracker`_.

As you probably know, segmentation faults often arise when a program
is attempting to access memory that the OS cannot locate or will not
allow.  Most often, this is the result of EXP/pyEXP being used in a
way that the developers haven't considered and tested.

If you are an experienced programmer and would like to contribute by
providing a fix, this is what we usually do:

* Recompile EXP/pyEXP as 'Debug' using ``ccmake`` or by changing the
  value of the ``CMAKE_BUILD_TYPE`` to 'Debug' in your
  ``CMakeCache.txt`` file.

* Run the code in ``gdb``.  If you are using pyEXP, you can launch
  ``gdb python3`` and run your script in the debugger.

* Look for failures such as undefined arrays, vectors, etc.  Even if
  you only report the approximate location in the source file, you
  will have saved the developers a lot of time and sped up the time to
  a fix.

.. _issue tracker: https://github.com/orgs/EXP-code/repositories/issues


How can I do a calculation with phase space in pyEXP
----------------------------------------------------

The phase-space interface in pyEXP is the ``ParticleReader`` which is
really a stream or iterator.  The user can access the phase-space
variables directly using the ``pyEXP.util.particleIterator(reader,
func)`` where ``reader`` is of type ``pyEXP.read.ParticleReader`` and
``func`` is a callback function that takes a scalar mass, position and
velocity arrays, and a scalar index as input. For example, you can
define the callback ``func`` in your Python environment and accumulate
summary statistics or even collect up phase space vectors by appending
to existing arrays.  Because ``ParticleReader`` is a stream, pyEXP does
not have an interface to phase space by array index.  This was a
design choice; the idea was not to push huge phase space snapshots
onto the users stack.

A simple example of this in practice is provided in the
``sample_part1_callback.ipynb`` in `pyEXP-examples repo
<https://github.com/EXP-code/pyEXP-examples>`_.

What do these parameters mean?
--------------------------------------

There are a lot of parameters that you can set in EXP/pyEXP! We describe
some of them below.

``numr`` is the number of radial grid points for spherical expansion, this
sets the interpolation length between grid points. There is really no downside to making this 
large, but anything larger than ~2000 is overkill. This generally doesn't need to
be changed from the defaults.


``rnum``, ``pnum``, and ``tnum`` are the radial, azimuthal, latitudinal quadrature knots, 
respectively, for Gram matrix. These are for computing orthogonal functions for cylindrical 
bases. You generally want ``rnum`` to be of order ``numr`` (like 1000), ``tnum`` can be a 
factor of 10 down from that (~100). ``pnum`` should be 1 *unless* you do not have an axisymmetric 
mass distribution (e.g. if you are starting with an arbitrary set of particles and you want to
build a basis from that with the most naive approach - here you would use ``pnum`` ~ 100 and let it go).
These generally don't need to be changed from the defaults.

The EJ parameters are explained in :ref:`the section on centering <centering>`.
You only want to change these values from their defaults if you have an external perturber,
these shouldn't be changed if you are working with with simulations of isolated systems.

``ratefile`` is an expert parameter for load balancing, this file gives diagnostics about
the different nodes/processesors on your system. EXP will produce a ``ratefile`` when running
simulations.


``nmax``, ``lmax``, ``mmax`` are the maximum radial order of cylindrical or spherical basis, the
the maximum spherical harmonic order, and maximum azimuthal order of the cylindrical basis. There 
are benchmark numbers but no hard-and-fast recommendations for these values. For simulations with
~ one million particles in the halo, we typically use ``lmax`` = 6,  ``nmax`` = 18 in the spherical
halo ``mmax`` = 6, ``nmax`` = 18 for the disk. This should give you all or most of the signal but 
some coefficients will be noisy. In general, we recommend that you go slightly past what you want
so that you get all the components and can analyse the significance of each coefficient post-facto.
