.. _making-coefficients:

How to  generate coefficients from phase-space snapshots
========================================================


This example assumes that you have pulled the (`EXP examples
repository <https://github.com/EXP-code/EXP-examples>`_) and run the
``EXP/examples/Better`` simulation.  We have also provided output from
this simulation in the `Better/data` directory for your convenience.
But this methods in the example can be adapted for any simulation you
like, not only EXP-generated simulations.

Many of the examples described in this documentation also have
corresponding Jupyter notebooks in the (`pyEXP repo
<https://github.com/EXP-code/pyEXP-examples>`_).

Let's just dive in.  We begin by importing ``pyEXP`` and friends and
setting the working directory.

.. code:: ipython3

    import os
    import yaml
    import pyEXP
    
    # I have the Better run in my personal direcotry; obviously
    # another you will want to change this a directory containing
    # some snapshots of your own or point at the output provided in
    # the EXP examples repo.
    #
    os.chdir('/home/weinberg/Nbody/Better')

Create the basis
----------------

We’ll only do the halo coefficients in this simple example. The
cylindrical coefficients would procede similarly. See the
``sample_basis`` notebook for an example of creating the cylindrical
basis.

Basis objects in pyEXP often have many parameters.  We use YAML for
specifying the basis.  Recall that :ref:`YAML <yaml-primer>` is a
human-readable data serialization format that is often used for
configuration files and data exchange between programming languages.
YAML is designed to be easy to read and write by humans. Its syntax is
straightforward and doesn't rely on any specific programming language.
It has strong C++ and Python support, so it's perfect for EXP.
Because YAML files are plain text, they are portable across different
operating systems and platforms. 

The first bit of the code below shows two ways of constructing a YAML
file.  You may use an editor and make a file, here called `basis.yaml`
or you may construct it in Python as a text string, here called
`bconfig`.  The final line of the code snippit does the work of
constructing the basis, assigned to the variable `basis`.

.. code:: ipython3

    # Get the basis config
    #
    yaml_config = ""
    with open('basis.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        yaml_config = yaml.dump(config)
    
    # Alternatively, you could construct this on the fly, e.g.
    bconfig = """
    ---
    id: SphereSL
    parameters :
      numr: 2000
      rmin: 0.0001
      rmax: 1.95
      Lmax: 4
      nmax: 10
      rmapping: 0.0667
      modelname: SLGridSph.model
    ...
    """
    print('-'*60)
    print('Read from file')
    print('-'*60)
    print(yaml_config)
    print('-'*60)
    print('Constructed from string')
    print('-'*60)
    print(bconfig)
    print('-'*60)
    
    # Construct the basis instance
    #
    basis   = pyEXP.basis.Basis.factory(yaml_config)


.. parsed-literal::

    ------------------------------------------------------------
    Read from file
    ------------------------------------------------------------
    id: SphereSL
    parameters:
      Lmax: 4
      modelname: SLGridSph.model
      nmax: 10
      numr: 2000
      rmax: 1.95
      rmin: 0.0001
      rmapping: 0.0667
    
    ------------------------------------------------------------
    Constructed from string
    ------------------------------------------------------------
    
    ---
    id: SphereSL
    parameters :
      numr: 2000
      rmin: 0.0001
      rmax: 1.95
      Lmax: 4
      nmax: 10
      rmapping: 0.0667
      modelname: SLGridSph.model
    ...
    
    ------------------------------------------------------------
    ---- SLGridSph::read_cached_table: trying to read cached table . . .
    ---- SLGridSph::read_cached_table: Success!!


Getting coefficients from the basis
-----------------------------------

``pyEXP`` provides two strategies for using the ``Basis`` to construct
coefficients:

1. Using a ``ParticleReader``, a helper object that supplies particle
   phase space to the ``Basis.createFromReader`` member.  Many of the
   standard phase-space file types are supported including Gadget,
   Gadget HDF5, Bonsai and of course EXP.

2. Using arrays of masses and positions supplied by the users own
   post-processing pipeline.  In this case, these Python `np.ndarray``
   types are passed to the `Basis.createFromArray`` member.


In both cases the ``createFrom*`` members take an optional expansion center
vector. If you need more complicated coordinate transformations,
Option 2 will serve you best.


Creating and using a particle reader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to hand off the files that comprise a snapshot for
every time slice. The ``ParticleReader`` provides a helper function for
that. There are two helper functions: ``parseFileList`` and
``parseStringList``. The first reads a list from a file and the second
takes a list. Otherwise they are the same. The file names in the list
are assumed to end with a snapshot index and an optional part index. For
example, if you have single files per snapshot, the list might look
like: ``myrun.00000``, ``myrun.00001``, etc. If you have multiple files
per snapshot, they will look something like ``myrun.00000_0001``,
``myrun.00000_0002``, ``myrun.00001_0000``, ``myrun.00001_0001``, etc.

Here is the call for a file:

.. code:: ipython3

    # Construct batches of files the particle reader.  One could use the
    # parseStringList to create batches from a vector/list of files.  NB:
    # a std::vector in C++ becomes a Python.list and vice versa
    #
    batches = pyEXP.read.ParticleReader.parseFileList('file.list', '')

We now iterate the ``batches`` created by the file parser to create the
coefficients. For each batch we create a new reader and pass the reader
to the basis instance. The ``basis.createFromReader`` member creates and
returns the coefficients. The coefficients are added to a coefficient
container called ``coefs``. Note: on the first call ``coefs=None`` so a
new container is created on the first time through.

.. code:: ipython3

    # This will contain the coefficient container, need to start will a
    # null instance to trigger construction
    #
    coefs   = None
    
    for group in batches:
    
        print("file group is", group)
    
        # Make the reader for the desired type.  One could probably try to
        # do this by inspection but that's another project.
        #
        reader = pyEXP.read.ParticleReader.createReader('PSPout', group, 0, False);
    
        # Print the type list
        #
        print('The component names are:', reader.GetTypes())
    
        compname = 'dark halo'
        reader.SelectType(compname)
        print('Selected', compname)
    
        print('Call createFromReader at Time', reader.CurrentTime(), 'for', reader.CurrentNumber(), 'particles')
    
        coef = basis.createFromReader(reader)
        print("Created coef")
    
        # We need this stupid idiom here because None is not mapping to a
        # null pointer.  There is probably a way to do this.  Suggestions
        # anyone?
        #                          This is optional---+
        #                                             |
        if coefs is None:           #                 v
            coefs = pyEXP.coefs.Coefs.makecoefs(coef, compname)
        else:
            coefs.add(coef)
    
        print('Added coef')
        print('-'*60)
    
    print('\nCompleted the file group list\n')
    
    print('The coefficient time list is', coefs.Times())


.. parsed-literal::

    file group is ['OUT.run7.00000']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.0 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00001']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.005000000000000004 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00002']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.010000000000000007 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00003']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.015000000000000012 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00004']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.020000000000000014 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00005']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.02500000000000002 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00006']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.030000000000000023 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00007']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.035000000000000024 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00008']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.04000000000000003 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00009']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.04500000000000003 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    file group is ['OUT.run7.00010']
    The component names are: ['dark halo', 'star disk']
    Selected dark halo
    Call createFromReader at Time 0.05000000000000004 for 100000 particles
    Created coef
    Added coef
    ------------------------------------------------------------
    
    Completed the file group list
    
    The coefficient time list is [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]


Creating coefficients using your own arrays
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will assume that you have an one-dimensional array of masses for
each particle and a :math:`3\times N` two-dimensional array of
particle positions.   There are two possible strategies.

A single set of arrays
^^^^^^^^^^^^^^^^^^^^^^

You can load your entire phase space into the mass and position arrays
and call ``createFromArray`` for each time slice.  This might look
something like this:

.. code:: ipython3

    # This will contain the coefficient container, need to start will a
    # null instance to trigger construction
    #
    coefs   = None
    
    for snap in range(numsnaps):
    
        print("Snapshot #{}".format(snap))
    
        # Read the masses and positions using your custom pipeline.
	# Let's call those resulting arrays "m", "pos" at time "time".
	# Then:
        #
        coef = basis.createFromArray(m, pos, time)
        print("Created coef")
    
        # We need the idiom here because None is not mapping to a
        # null pointer.
        #                          This is optional---+
        #                                             |
        if coefs is None:           #                 v
            coefs = pyEXP.coefs.Coefs.makecoefs(coef, compname)
        else:
            coefs.add(coef)
    
        print('Added coef')
        print('-'*60)
    
    print('\nCompleted the snapshot list\n')
    
    print('The coefficient time list is', coefs.Times())

    
Multiple sets of arrays
^^^^^^^^^^^^^^^^^^^^^^^

For each time, you may process your phase space particles in bunches.
You will need this for very large phase-space snapshots.  This is
nearly the same as the method above but we break up
``createFromArray`` into three separate calls: ``initFromArray``,
``addFromArray``, and ``makeFromArray``.  The first and last are
called at the beginning and end and ``addFromArray`` is called once
for each bunch.  In fact, ``createFromArray`` is simply a call to each
of the three separate calls under the hood.

Here is an example code snippet:
    
.. code:: ipython3

    # This will contain the coefficient container, need to start will a
    # null instance to trigger construction
    #
    coefs   = None
    
    for snap in range(numsnaps):
    
        print("Snapshot #{}".format(snap))
    
	basis.initFromArray()

	for n in range(nbunches):

	   # Read the masses and positions using your custom pipeline for
	   # each of nbunches.  As before, let's call those resulting
	   arrays "m", "pos" at time "time".
	   #
           # Then:
           #
	   basis.addFromArray(m, pos)

	   
	coef = basis.makeFromArray(time)
	print("Created coef")

        # We need the idiom here because None is not mapping to a
        # null pointer.
        #                          This is optional---+
        #                                             |
        if coefs is None:           #                 v
            coefs = pyEXP.coefs.Coefs.makecoefs(coef, compname)
        else:
            coefs.add(coef)
    
        print('Added coef')
        print('-'*60)
    
    print('\nCompleted the snapshot list\n')
    
    print('The coefficient time list is', coefs.Times())


DONE!
-----

Our task is completed!  We now have a coefficient object in Python
called `coefs` that may be saved into an HDF5 file that may be read at
any future time (see :ref:`saving coefficients <saving-coefficients>`)
or used to generate fields and movies (see :ref:`visualizing fields
<visualizing-fields>`).
