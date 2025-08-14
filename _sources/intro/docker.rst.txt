.. _intro-docker-notes:

==========================
Exploring EXP using Docker
==========================

.. note::

   * You will need Docker installed to use it!

   * Instructions for installing Docker on MacOS, Linux and Windows
     systems can be found `here <https://docs.docker.com/get-docker>`_.

   * We also suggest learning a bit about Docker, if you have not used
     it previously.  There are many available introductions to Docker,
     like `this one <https://docker-curriculum.com>`_.

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

1. Run the container with the command: ``expbox -t -d `pwd```.  The
   ``-t`` flag starts an interactive terminal. The ``-d <dir>`` flag
   uses ``<dir>`` as the working directory. You can omit this move to
   any desired working directory in your home tree.

2. Run the simulation with the command ``mpirun exp``.

A few notes:

* When the container starts running, you will see standard shell
  prompt: ``bash-5.1$``.  At this point, you can look around the
  system, browse files, etc.  It's a slimmed down Ubuntu Linux image.

* EXP in the Docker container is installed in ``/usr/local/EXP``.

* OpenMPI detects the available number of cores and uses that by
  default.  You can supply the ``-np X`` flag to ``mpirun`` to
  explicitly request ``X`` processes.

* Use the ``-h`` flag to ``expbox`` for a list of additional options. Take
  a quick look at `this README
  <https://github.com/EXP-code/EXP-container/tree/main/Docker>`_ for
  more details.

* The containers will continue to exist until you stop or remove them.
  For example, if you started a container named ``expbox_8889``, you
  can stop and remove it using ``docker rm -f expbox_8889``.  Use
  ``docker ps`` to see your containers.
