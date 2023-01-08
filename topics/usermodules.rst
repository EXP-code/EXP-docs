.. _usermodules:

User modules
============

.. index: user modules; extending EXP; ExternalForce

Users may write modules that are found and loaded at runtime.  One may
derive classes from `ExternalForce` that may be built as
dynamic modules that may be loaded and instantiatied as needed.
Modules are built in the `src/user` directory.  This is
accomplished using dynamically loaded (DL) libraries that register
themselves on a list of `ExternalForce` instances that may be
instantiated as directed in your configuration file.  These new
modules have access to the entire phase space for each component.  It
is the user's responsibility to not change the phase space in
unphysical ways, of course.

There are only a few steps necessary to put one's code in the tree:

1. Write the code (see below for additional details)

2. Edit `CMakeLists.txt`.  Assume you module is called
   `foo` and is implemented in the following source files
   `foo1.cc` and `foo2.cc`. Do the following:

   - Define a new source variable pointing to the source files in the
     `CMakeLists.txt`.  E.g.  `set(foo_SRC foo1.cc foo2.cc)`
    
3. Compile the code

4. Install the code in the location defined by your configuration

Notes on writing your module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A good place to start is the code already in the `src/user`
directory. The simplest code is `UserTest.cc`; this does
nothing but print messages but illustrates all of the necessary
components.

All classes, of course, must derive from `ExternalForce`.  A quick
look at `src/ExternalForce.H` will show that you will need to
implement at least the member
`determine_acceleration_and_potential_thread()`.  In order to parse
command line parameters, you will also need a constructor and
`initialize()` and maybe a destructor.

In addition, there is a mechanism that identifies your new class to
EXP.  This has two parts.  First you must define a C
function which constructs an instance of your class and returns a
pointer. Using the C calling interface here gets around the problem of
name demangling in C++ in using the dynamic linking loader (there may
be a more transparent and portable way to do this).  You will notice
an addtional class at the end of the file called `proxy`.  An
instance of this simple class is instantiated when the module is
loaded (the last line in the file).  As a byproduct, a pointer to the
function `makeTest()` is is added to the factory map defined in
`ExternalForce.H`.  This function can then be invoked by name
in the code to create an instance of your class.  Cute trick, eh?  You
can simply copy this to your own source (changing `makerTest`
to `makerFoo` or someother unique name).

