.. _intro-install:

==================
Installation guide
==================

.. _faq-supported-systems:

Supported system versions
=========================

* EXP was developed using Debian and Ubuntu GNU-Linux systems but have
  been tested on a wide variety of Linux installs including RedHat and
  CentOS. With a few optional exceptions, it does not use OS specific
  features so we expect little difficulty compiling in any GNU
  environment.

* EXP has been thoroughly tested with the GNU compiler suite but we
  have verified that it will also compile with recent versions of Clang.

* Native support for MacOS is in progress, so please stay tuned.

* The code includes a GPU implementation for adaptive basis force
  evaluation using NVidia's Cuda system.  This is optional and not
  needed for pyEXP although we plan to implement a Cuda-aware pyEXP at
  some point.

* pyEXP requires `Python`_ 3.x as part of the internal pybind11
  implementation.


.. _intro-install-EXP:

Installing EXP and/or pyEXP
===========================

.. index:: install EXP

EXP and pyEXP are configured using CMake, a configuration system
widely used in HPC environments.  CMake will attempt to locate all
necessary dependencies.  pybind11, the C++ YAML support library
(yaml-cpp) and the HDF5 C++ wrappers (HighFive) are provided as git
submodules.  Be sure to initialize them after your first ``git clone``
using:

.. code-block:: bash

   $ git submodule update --init --recursive

.. index:: CMake

A typical CMake invocation begins by making a build directory.  We
will build out of source but the build directory may be in the source
tree or outside the source tree.  Your choice.  I tend to do this
inside the source tree myself, e.g.:

.. code-block:: bash

   $ mkdir -p build cd build

This allows one to have build various versions avaialble from the same
source, such as Release and Debug.

.. index:: Eigen3, Cuda

You may need to adjust the cmake call below.  Besides Cuda, make
sure that the Eigen3_DIR is set to the install location so CMake can
find the Eigen3 rules.

The install location will need to be changed in the example below.
E.g. I would use ``-DCMAKE_INSTALL_PREFIX=/home/mdw_umass_edu`` on the
UMass Unity cluster.

.. _compile-features:

Features
========

There are various features options.  A subset of user modules are ON
by default.  The important ones are:

* ``ENABLE_NBODY`` compiles the n-body code.  If you are only
  interested in pyEXP, use ``-DENABLE_NBODY=NO``.   ON by default.

* ``ENABLE_PYEXP`` compiles the Python bindings.  Similarly, if this
  is what you want, use ``-DENABLE_PYEXP=YES``.  OFF by default.

* ``ENABLE_CUDA`` set to TRUE will will compile EXP with NVidia GPU
  support of the Cuda SDK is found.  OFF by default.

* ``ENABLE_USER`` compiles a common subset user modules for the n-body
  code and these are ON by default.  These will only be built if
  ``ENABLE_NBODY`` is ON.

* ``ENABLE_USER_ALL`` compiles all the user modules.  OFF by default.

* ``BUILD_DOCS`` builds the `Doxygen`_ web-based documentation viewer.
  This requires Doxygen on your system and is OFF by default.  Doxygen
  is not required.

.. index:: Doxygen

Finding packages
================

CMake will do its best to find your FFTW pacakge by default.  If
that fails, and if you need or want FFTW and your FFTW is installed
in an unusual location, you can define that location using
``-DFFTW_ROOT=/path/to/fftw/location``.  Or you can provide the
location in the ``FFTWDIR`` environment variable.

A typical CMake build invocation without Cuda is:

.. code-block:: bash
		
   $ cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_USER=YES -DEigen3_DIR=$EIGEN_BASE/share/eigen3/cmake -DCMAKE_INSTALL_PREFIX=/home/user -Wno-dev ..

A typical invocation with Cuda is:

.. code-block:: bash
		
   $ cmake -DCMAKE_BUILD_TYPE=Release -DCUDA_USE_STATIC_CUDA_RUNTIME=off -DENABLE_CUDA=YES -DENABLE_USER=YES -DEigen3_DIR=$EIGEN_BASE/share/eigen3/cmake -DCMAKE_INSTALL_PREFIX=/home/user -Wno-dev ..

Some installations provide an EIGEN_BASE environment variable that
locates the install directory what contains 'include' and 'share'.
Alternatively, replace EIGEN_BASE with that path or set EIGEN_BASE
manually.

Many users will like configuring with one the CMake gui tools, such as
``ccmake`` or ``cmake-gui`` instead of the command-line ``cmake``.  The
gui will allow you to change the parameters interactively and display the
help info for each parameter.  For example:

.. code-block:: bash

   $ ccmake ..

and then enter your preferred build type and other options
interactively.  This provides a nice view of the configuration as a
bonus.  I recommend ``ccmake`` rather than the Qt ``cmake-gui`` but
this is personal preference.

You can use CMake build type Debug for debugging and etc. or use None or
empty and set your own ``CFLAGS`` and ``CXXFLAGS``.  See the CMake manual.

Finally, you are ready to make the package:

.. code-block:: bash

  $ make -j N

Here, ``N`` is the number of jobs to run
simultaneously.  I often use N=2*<number of cores> to take advantage
of hyperthreading

Finally, install to the target location.  You can select the target
install location using the ``CMAKE_INSTALL_PREFIX`` variable in CMake:

.. code-block:: bash

   $ make install

A note on multiple builds
=========================

CMake workflow is designed to permit multiple build types
(e.g. Debug, Release) in separate directories with the same source.
However, EXP generates a 'config.h' based on the available
packages. For example, if you want to generate a build hierarchy
like this:

.. code-block:: bash

   build/
   build/debug
   build/release

with the different build types alone, the multiple build strategy will
work perfectly.  However, if Cuda is enabled in one build and not the
other, you will need to manually delete the top-level config.h when
changing build directories.  This will trigger a full recompile.

Things that are good to know
----------------------------

EXP is written in C++-17 (largely) and depends on a few key C++ packages:

* `FFTW`_, an efficient Fast-Fourier Transform implementation

* `OpenMPI`_, a modern MPI-2/3 implementation.  Other implementation
  (e.g MPICH) should also work but we have not verified them recently.

* `HDF5`_, an implementation of the HDF5 standard as provided by the
  HDF5 consortium.  We use the HighFive C++ header-only interface with
  the C-API.

* `Eigen3`_, a suite of vector/matrix classes along with standard
  linear algebra and eigen problem solvers.

* `HighFive`_, a header-only C++ API for HDF5 used by EXP as provided
  as a git submodule.

* `libyaml-cpp`_, a C++ library implementing YAML reading, parsing and
  emitting.  Also provided as a git submodule.



Some of these packages might require additional installation steps
depending on your platform.  Please check :ref:`platform-specific
guides below <intro-install-platform-notes>`.

In case of any trouble related to these dependencies,
please refer to their respective installation instructions:

.. _intro-using-virtualenv:

Using a virtual environment (recommended)
-----------------------------------------

.. index:: pair: Python; venv
.. index:: Lua modules

TL;DR: We recommend installing pyEXP inside a virtual environment
on all platforms that use ``lmod modules``.  

Python packages can be installed either globally (a.k.a system wide),
or in user-space.

Instead, we recommend that you install EXP within a so-called "virtual
environment" (:mod:`venv`).  Virtual environments allow you to not
conflict with already-installed Python system packages (which could
break some of your system tools and scripts), and still install
packages normally with ``pip`` (without ``sudo`` or obtaining root
privileges in some other way).

For example, assume that you have loaded a Python module or wish to
use the current Python version in your executable path.  An example
virtual environment installation is:

.. code-block:: bash

   $ python3 -m venv ~/venv/python9
   $ source ~/venv/python3.9/activate

This creates and activates the virtual Python environments.  I called
my virtual environment ``python9`` to distinguish it from a venv that
might be installed for some other reason.

Now, you can then install your favorite Python modules using ``pip``
as usual.  For example, you will need ``numpy`` and you may want
``pyplot``.  Similarly, for using MPI-aware Python scripts you will
need ``mpi4py``.  After activating your virtual environment, you can
install those with

.. code-block:: bash

   $ pip install numpy matplotlib mpi4py

.. index:: sort: Python; path

Once you have created a virtual environment, you can copy or link the
shared library to your site packages directory. The actual name
depends on your build environment.  For example, in Ubuntu 22.04 using
Python3.9, the library is called
``pyEXP.cpython-309-x86_64-linux-gnu.so``.  In this same case, this
would be copied to ``~/venv/python9/lib/python3.9/site-packages``.
(See :ref:`platform-specific guides <intro-install-platform-notes>`
below for known dependencies that you may need to install beforehand).


.. _intro-install-platform-notes:

Platform specific installation notes
====================================

.. _intro-install-windows:

Windows
-------

Though it should be possible to install EXP and pyEXP under Windows,
we haven't tried.  If you have a working install, please *do*
contribute some notes!

.. _intro-install-ubuntu:

Ubuntu 18.04 and above
----------------------

EXP has been currently developed under Ubuntu for 10 years.  It
currently requires the C++-17 language features and has been thorougly
tested with recent versions of Ubuntu.  A typical recipe to install
packages might be:

.. code-block:: bash

   $ apt install libeigen3-dev libopenmpi-dev libhdf5-dev libfftw3-dev
   $ apt install libpng-dev libvtk7-dev libtirpc-dev doxygen
   $ apt install cuda-toolkit-11.7

where the first line is required, the second line is optional, and the
third line is necessary only if you want to build Cuda support for EXP.

Linux-based HPC using lmod
--------------------------

Every HPC center names their modules differently.  A typical recipe to
install modules might be:

.. code-block:: bash

   $ module load openmpi gcc cmake fftw cuda hdf5 python3 vtk eigen slurm openblas

Although no specific versions were specified in the command, we
recommend being specific by version.  E.g. ``module load
gcc/11.3.0`` to get a specific release instead of simply ``module load
gcc`` that may be an older system defult.  I recommend examining the
available modules using ``module avail`` and pick recent versions of
the packages.  Many HPC centers have older ones for backward
compatibility.

Once you have a good build, save your module set using ``module save
EXP`` and restore it before running using ``module restore EXP``.

.. _intro-install-macos:

macOS
-----

Work in progress.

.. _intro-install-troubleshooting:

Troubleshooting
===============

Some strange error that we've seen
----------------------------------

Provide a fix or suggestion.

.. _Python: https://www.python.org/
.. _FFTW: http://fftw.org
.. _OpenMPI: https://www.open-mpi.org/
.. _HDF5: https://portal.hdfgroup.org/display/HDF5/HDF5
.. _Eigen3: https://eigen.tuxfamily.org/
.. _HighFive: https://github.com/BlueBrain/HighFive
.. _libyaml-cpp: https://github.com/jasonjei/libyaml-cpp
.. _Doxygen: https://www.doxygen.nl/
