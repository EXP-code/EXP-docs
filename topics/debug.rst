.. _topics-debug:

=============
Debugging EXP
=============
.. _debug:

EXP
===

The combination of MPI, threading and CUDA makes debugging a
challenge.  To aid in this, EXP both installs its own error handlers
and tries to use C++ exceptions and clean MPI terminations with error
messages when possible.  Nevertheless, some number of *ugly* unhandled
erros that generate tracebacks are unavoidable.  When possible, *EXP*
will unwind the stack on each process and write the traceback to a
file tagged with the runtag name and the MPI node number.  Most
problems can be diagnosed by a very careful reading of the standard
output messages and generated tracebacks.  The EXP code can seem very
*chatty* at times and and the user may have the tendency to ignore the
various messages.  So to repeat: when in doubt, **check the standard
output logfile first**.


Diagnostic output for various VERBOSE values
--------------------------------------------

EXP has a `VERBOSE` flag at the global top level `YAML configuration
<yamlconfig>` which sets the chattiness as follows:

- `VERBOSE=0`

  * No extra output

- `VERBOSE=1` (default value)

  * Output timestep diagnostics for each component `multistep.cc`

- `VERBOSE=2`

  * Currently an unused level

- `VERBOSE=4`

  * multistep output timestep diagnostics for each component
    `multistep.cc`

  * use cputime counters for timing each part of the force
    computation and time step advance `ComponentContainer.cc`

  * use cputime counters for each part of the step `step.cc`

  * log each center and axis computation `Cylinder.cc`

- `VERBOSE=5`

  * output the multistep level totals for each component `step.cc`

- `VERBOSE=6`

  * thread timing in force routines

- `VERBOSE=7`

  * log force calls that are off the basis grid to stdout
    `Cylinder.cc`

  * dump YAML config file to standard output.  The current
    configuration will also be written to `PARAM.<runtag>.yml`

- `VERBOSE=11`

  * write out multistep control structure (no one really needs this
    level of detail unless one is debugging `multistep.cc`


Floating-point error handling
-----------------------------

For numerical errors that generate floating point exceptions (FPEs),
EXP offers a three levels of debugging support using the `gdb`
debugger.

1. The global parameter `fpe_trap: true` enables the installation of a
   user FPE error handler.  To use this, start EXP in `gdb` or in many
   instances of `gdb` for MPI debugging.  Then set a breakpoint in
   `fpetrap.h:21` to catch and debug FP errors.

2. The global parameter `fpe_trace: true` installs an error handler
   that prints a backtrace to stderr on detecting an FP error.  In
   order to use this productively, you will need to compile with
   symbols; that is, with the `gcc/g++` compile flag `-g` (DEBUG in
   CMake).

3. The global parameter `fpe_wait: true` installs an error handler
   that will print an error message to the standard output and wait.
   When an FPE is signalled, process will spin, waiting for a `gdb`
   connection. Messages describing the affected node and pid will be
   written to the standard output.

4. To allow a person to set break points when the run starts, EXP
   offers the global parameter `debug_wait: true`.  all processes will
   wait in a loop until `gdb` is attached and the loop is freed but
   setting the variable `debug_wait` to `false`.  If the global
   parameter `main_wait: true`, only the root process will wait.

5. Finally, the global parameter `mpi_wait: true` enables
   the installation of an MPI error handler that will spin in a loop
   when called, waiting for a gdb connection. Messages describing the
   affected node and pid will be written to the standard output.


Checking for MPI consistency
----------------------------

EXP includes a built-in synchronization checker, ``BarrierWrapper``,
that uses `MPI_Barrier` to mark a code location with a string token
and verifies that each process in the MPI multi-computer arrives at
the barrier with the same token.

There are two distinct implementations, a light-weight and
heavy-weight checker.  The light-weight implementation is simple: when
nodes arrive at an MPI barrier, the tokens are sent to the root node.
When all processes have arrived at the barrier, the root node checks
that all tokens agree, and complains to stdout if they do not.  The
heavy-weight implementation polls in loop and reports the status of
processes that have reached and not reached the barrier.  This
provides more information than the light-weight version but can be
confusing.

The light-weight version is used by default.  The heavy-weight version
can be specified by including ``barrier_light: false`` in the global
YAML stanza (see the :ref:`YAML config example <yamlconfig>`).
Other global parameters affecting the ``BarrierWrapper`` behavior
include:

* ``barrier_check``: set to ``true`` to enable the ``BarrierWrapper``. The default is ``false``.

* ``barrier_quiet``: set to ``true`` turns OFF extra output describing
  the wrapper state.  This is the default.

* ``barrier_verbose``: set to ``true`` turns ON extra output
  describing the wrapper state.  This is the opposite of
  ``barrier_quiet: true``.

* ``barrier_debug``: provides some additional information about internal synchronization to be used if the wrapper is providing confusing results.

* ``barrier_extra``: provide even more internal diagnostics than verbose.


pyEXP
=====

Using the GDB debugger
----------------------

Debugging the C++ implementation of pyEXP is no different than EXP.
For example, you can just start GDB with Python:

.. code-block:: bash

   gdb python
   break <C++ function break point>
   run mytest.py

You need to compile EXP with debug information by specifying
'Debug' for ``CMAKE_BUILD_TYPE`` by editing the ``CMakeCache.txt``
file directly.  For example, from your build directory you can execute:

.. code-block:: bash

   ccmake <top-level source dir>

If you are not debugging the Python interpreter itself, you do not
need to do anything special; you can use the regular interpreter and
no extensions.  GDB will complain that there are no debugging symbols
in `python3` but that does not matter; the C++ code referenced by the
pyEXP bindings *will* have debugging symbols.

Debugging both Python and C++ from GDB is more complicated but
possible although we do not recommend doing this. You will need a
Python build with debug info.  For example, if you are running Python
3.10 on Ubuntu, you can install the debug build as follows:

.. code-block:: bash

   sudo apt install python3.10-dbg

There are a number of online resources for debugging Python using
GDB.  See `Python GDB`_ to get started.

.. _Python GDB: https://wiki.python.org/moin/DebuggingWithGdb
