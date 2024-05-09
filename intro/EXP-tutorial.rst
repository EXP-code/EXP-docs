.. _intro-EXP-tutorial:

============
EXP Tutorial
============

In this tutorial, we'll assume that EXP is already installed on your system.
If that's not the case, see :ref:`intro-install`.

This tutorial will walk you through these tasks:

1. Import the example repository from github
2. Adjust the configuration file for your system
3. Run EXP on the example
4. Try some of the simple pyEXP analysis notebooks


Quick start
===========

Like many research codes, this code has many flags and parameters that
allow detailed control of methods.  Many of these were used for
testing the implemenation and algorithm and do not need adjustment.  I
have endeavored to provide sane values as defaults, but some
combinations are likely to fail on occasion and require study of the
source code to understand.  The class documentation often provides
details on specific parameters.  If you get stuck or confused, I will
do my best to help and will add to the documentation in response to
questions.  Also, feel free to contribute documentation and propose
changes.

Perhaps the best way to learn how to use this code is through an
example.  As described in :ref:`tutorial intro <intro-tutorial>`, we
have provided a separate `git repository
<https://github.com/orgs/EXP-examples>`_ with three quick examples.
Each example contains all of the body files, configuration files and
model files necessary to run the simulation.  All of these can be run
on a laptop or workstation.

1. ``Halo``: a spherical halo with 10000 particles

2. ``DiskHalo``: a disk and halo phase space, each component has 10000
   particles, and a cylindrial disk expansion up to :math:`m=1`.

3. ``Nbody``: similar to ``DiskHalo`` but 100000 halo particles, and a
   high-resolution cylindrial disk expansion up to :math:`m=6`.

4. ``Binary``: is a simple simulation two-body binary system.  While
   mostly a trivial test and example of calling EXP, it is a sanity
   check and possibly useful for experimenting with integration and tuning
   parameters. 

To run any or all of these, we recommend that you copy the directory to some
local scratch location.  Then adjust the `outdir` and `ldlibdir`
parameters in the YAML `Global` stanza to reflect the location for
data output and the `user` directory of the library install location.
This latter is optional, since we do not need the auxiliary loadable
modules for any of these examples.

Each of the simulation examples may then be run as follows:

.. code-block:: bash

   mpirun exp


Next steps
==========

This tutorial covered only the basics of EXP, but there's a lot of other
features not mentioned here. Check the :ref:`topics-whatelse` section in
:ref:`intro-overview` chapter for a quick overview of the most important ones.

