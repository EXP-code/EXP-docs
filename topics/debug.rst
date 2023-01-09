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

pyEXP
=====

Using the GDB debugger
----------------------

