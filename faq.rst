.. _faq:


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

The core EXP libraries are use `MPI <https://www.mpi-forum.org/>`_
which allows EXP and pyEXP in some instances use many compute nodes.
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

My HPC cluster does not have the required dependencies.  What are my options?
-----------------------------------------------------------------------------
Ask your HPC administrators about running applications in containers.
We have had good success with `Apptainer
<https://apptainer.org/>`_ (formerly known as `Singularity`).  Apptainer containers provide
all of the libraries and executable objects necessary to run EXP as an
MPI application in a Linux environment of their choosing.

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
   generic instructions.  Also: please consider contributing your
   working recipe to `this repo <https://github.com/EXP-code/EXP-apptainer>`_!

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
  you only report the approximately location in the source file, you
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
<https://github.com/EXP-code/pyEXP-examples>`_).
