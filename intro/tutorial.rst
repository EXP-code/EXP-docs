.. _intro-tutorial:

=========
Tutorials
=========

.. index:: tutorials

.. toctree::
   :caption: Tutorials
   :hidden:

   pyEXP-tutorial
   EXP-tutorial

These tutorials are based on the companion :index:`GitHub` EXP
repositories which you can clone to your working computer in the usual
way.  To get the pyEXP examples do:

.. code-block:: bash
		
   git clone git@github.com:EXP-code/pyEXP-examples.git pyEXP-examples

and to get the EXP N-body examples do:

.. code-block:: bash

   git clone git@github.com:EXP-code/EXP-examples.git EXP-examples


.. note:: We use the ``Nbody`` example from ``EXP-examples`` to
	  illustrate some key features of pyEXP.  For pyEXP-only
	  users, we provide an abbreviated output set that may be
	  copied from ``EXP-examples/Nbody/data``.  In addition, for
	  those of you interested in _both_ EXP and pyEXP, we
	  recommend studying the example in ``EXP-examples/Nbody`` as
	  a template for an astronomically relevant simulation.

Quick-start examples
--------------------

The following two tutorials are quick excerpts from the larger example
suite to get you started.

:doc:`pyEXP-tutorial`
    Your first pyEXP example project.

:doc:`EXP-tutorial`
    Your first EXP example project.

Exploring EXP using Docker
--------------------------

As described in the top of the :ref:`FAQ <faq>`, our Docker container
provides a quick way of trying EXP without compiling the software on
your own.  To get started, download the `expbox
<https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox>`_
and make it executable.  Running the script will retrieve the latest
EXP docker image, build a docker container, and run Jupyter by
default.  You now have a fully working EXP installation; proceed to
the pyEXP tutorials!

If you would like to try the EXP n-body code, first change to a
working directory of your choice that contains the configuration and
supporting files.  For example, let's suppose that you've copied the
files from `DiskHalo <https://github.com/EXP-code/EXP-examples>`_ to
your current working directory. You can run this example with the
Docker container in two steps:

1. Run the container with the command: ``expbox -t``.  The ``-t`` flag
   starts an interactive terminal.

2. Run the simulation with the command ``mpirun exp``.

A few notes:

* When the container starts running, you will see standard shell
  prompt: ``bash-5.1$``.  At this point, you can look around the
  system, browse files, etc.  It's a slimmed down Ubuntu Linux image.

* EXP in the Docker container is installed in ``/usr/local/EXP``.

* Use the ``-h`` flag to ``expbox`` for a list of additional options. Take
  a quick look at `this README
  <https://github.com/EXP-code/EXP-container/tree/main/Docker>`_ for
  more details.
