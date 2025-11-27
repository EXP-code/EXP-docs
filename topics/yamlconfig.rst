.. _yamlconfig:

What is YAML?
=============

EXP and pyEXP use YAML for specifying configurations.  YAML is a data
serialization language that is often used for writing configuration
files. The official `YAML documentation <https://yaml.org>` says YAML
stands for yet another markup language or YAML ain’t markup language
(a recursive acronym), emphasizing that YAML is about data not
documents.

.. index:: YAML

.. toctree::
   :caption: YAML primer
   :hidden:

   yaml-primer

:doc:`yaml-primer`
     An optional quick introduction to YAML syntax


.. warning::

   Here and throughout the documentation, we give examples of
   configuring EXP.  However, this is not a complete description of
   all the available parameters and options for every method.

   For a more complete description of EXP classes and methods, you may
   configure and build the Doxygen manual which provides a detailed
   description of the classes, methods, and their arguments.  You may
   do this by specifying `-DBUILD_DOCS=ON` when invoking CMake or
   toggle the `BUILD_DOCS` parameter in ``ccmake``.  `BUILD_DOCS=OFF`
   by default.

   The Doxygen web manual will be built in the ``docs/html`` directory
   in the top-level ``EXP`` directory.  You can start the Doxygen
   manual in a web browser with the URL
   ``file:///<top-level-EXP-src>/docs/html/index.html``. Doxygen
   provides a search bar in the upper right corner and a navigation
   bar on the left.

.. _exp-config:

An annotated EXP YAML configuration
===================================

An example is probably better than paragraphs of description.  So here
is an EXP YAML file with annotation.

.. code-block:: yaml

   ---
   # YAML 1.2
   # See: http://yaml.org for more info.  EXP uses the
   # yaml-cpp library (http://github.com/jbeder/yaml-cpp)
   # for parsing and emitting YAML
   #
   # ------------------------------------------------------
   # These parameters control the simulation
   # ------------------------------------------------------
   Global:
     outdir     : /home/user/Nbody
     nbodmax    : 100000
     nthrds     : 1
     dtime      : 0.05
     ldlibdir   : /home/user/lib/user
     runtag     : run1
     nsteps     : 5
     multistep  : 10
     infile     : OUT.run1.chkpt

   # ------------------------------------------------------
   # This is a sequence of components. 
   #
   # Each component file should contain four fields 
   # deliminated by ':' characters.
   #
   # The first is the Force name.  The parameters for
   # the force are included as a parameter map.
   #
   # The second is the list of parameters that that will 
   # be passed to the Component on creation.
   #
   # The third is the name of the bodies file (in ascii).
   #
   # The fourth is the force name or id and list of
   # parameters that will be passed to the Force.
   #
   # Each indented stanza beginning with '-' is a component
   # ------------------------------------------------------
   Components:
     - name       : dark halo
       parameters : {nlevel: 1, indexing: true, EJ: 2, nEJkeep: 256, EJdryrun: true}
       bodyfile   : halo.bod
       force :
         id : sphereSL
	 parameters : {rmax : 2.5}

     - name       : star disk
       parameters : {nlevel: 1, indexing: true, EJ: 2, nEJkeep: 256, EJdryrun: true}
       bodyfile   : disk.bod
       force :
       id : cylinder
       parameters : {acyl: 1.0, nmax: 32, mmax: 2, hcyl: 0.05, ncylorder: 24, pca: true, hallfreq: 10, pcavtk: true}

   #
   # The parameters could be expressed like this,
   # equivalently:
   #
   #       parameters :
   #         acyl : 1.0
   #         nmax : 32
   #         mmax : 2
   #         hcyl : 0.05
   #         pca  : true
   #         ncylorder : 24
   #         hallfreq : 10
   #         pcavtk : true

   # ------------------------------------------------------
   # This is a sequence of outputs
   # ------------------------------------------------------
   Output:
     - id : outlog
       parameters : {nint : 10}
     - id : outps
       parameters : {nint : 5}
     - id : outpsp
       parameters : {nint : 1, timer : true}

   # ------------------------------------------------------
   # This is a sequence of external forces
   # This can be empty (or missing)
   # ------------------------------------------------------
   External:

   # Currently empty

   # ------------------------------------------------------
   # List of interations to exclude as name1 : name2 map
   #  entries.  This can be empty (or missing)
   # ------------------------------------------------------
   Interaction:
  
...

Some additional explanation
---------------------------

.. index: configuration; config; yaml
.. index:: Global; Components; External; Output; Interactions

The main configuration file identified on the ``exp`` command line as
the first parameter or optionally using the ``-f`` flag. The default
parameter file is named ``config.yml`` if no config file is given.

The parameter file is divided into stanzas.  Each stanza begins with a
tag of the form ``stanza_name``.  Each stanza is followed by lines
which contain Key and Value pairs demarcated in standard YAML syntax
by a ':'.  Each stanza is a YAML node and the order of nodes in the
YAML sequence is not significant.  I usually put the ``Global`` stanza
first anyhow, but note that YAML emitters are not required to preserve
order.

A line may be commented with a leading '#'.  The YAML EXP
configuration file has 5 sections or 'nodes' in YAML parlance.  The
``Components``, ``External``, and ``Output`` nodes are sequences that
instruct the containers to build particular objects.  Full parameter
lists for the ``Component``, ``Output`` and ``ExternalForce`` classes
are listed in the manpage for each class in the :ref:`Doxygen web
documentation <doxygen>`.


1. ``Global:``

  This stanza defines basic features of the simulation such as name,
  time step and time step parameters, and working directory.

  Each ``Key`` defines a specific parameter value or boolean toggle.

2. ``Components:``
     
  This stanza defines the phase-space components with associated
  parameters and force methods as a list.  Each list element starts
  with '-' and has four fields:

  ==========     ===========
  Key word       Explanation
  ==========     ===========
  name           the mnemonic name for the component
  parameters     a list of key: value pairs
  bodyfile       the name of the ascii phase-space file to initialize this component
  force          the method for computing the potential and acceleration
  ==========     ===========

  
  The mnemonic name may contain spaces.  The body file is in EXP
  native formation.  EXP has its own hierarchical phase space
  structure that we call :ref:`PSP <exp-phase-space>`.  EXP provides a
  number of standalone routines to manipulate, visualize and summarize
  the content of PSP files.  EXP uses the list index internally to
  describe the component. However, there is support for reflection by
  mnemonic name.

  For example, you could have a stellar disk component and a dark matter halo component. 
  The **dark halo** is the dark matter halo with a spherical basis, where parameters can 
  be set as follows:

.. code-block:: python

   # Make the halo basis config
  
   Components:
      - name:      dark halo             #component name, this is up to you
        bodyfile:  halo.bods             #body file, this can be omitted if you are only interested in making a basis and not a simulation
        parameters:
           #leaving blank to set to defaults, these are expert parameters
        force
            id:    sphereSL              #adaptive basis, here the sphereSL type
        parameters :
            numr:  2000                  # number of radial grid points
            rmin:  0.0001                # smallest radial grid point
            rmax:  1.95                  # largest radial grid point
            Lmax:  4                     # maximum spherical harmonic degree
            nmax:  10                    # maximum radial order
            rmapping: 0.0667             # radius for coordinate mapping
            modelname: SLGridSph.model   # model file name
            Cachename: slgrid_sph_cache  # cache name, this can be omitted if you are only interested in making a basis and not a simulation 


The parameters *rmin* and *rmax* define the inner and outer radii for the basis in units where
:math:`G = 1`, *Lmax* and *nmax* describe the maximum harmonic and radial
orders for the basis, respectively. The *rmapping* parameter adjusts the internal coordinate mapping
and a good choice is the characteristic or scale radius of the halo.



The **star disk** is the stellar disk with a cylindrical basis. Parameters for this component
are set as follows: 

.. code-block:: python

      - name:      disk                  #component name, this is up to you
        bodyfile:  disk.bods             #body file, this can be omitted if you are only interested in making a basis and not a simulation
        parameters:
           #leaving blank to set to defaults, these are expert parameters
        force: 
            id:    cylinder              #adaptive basis, here the cylindrical type
        parameters:
            acyl: 0.01                   # radial scale length for the disk basis reconstruction
            hcyl: 0.001                  # vertical scale height for the disk basis reconstruction
            nmaxfid: 32                  # maximum radial order for spherical basis
            lmaxfid: 32                  # maximum harmonic order for spherical basis
            mmax: 6                      # maximum azimuthal order of cylindrical basis
            nmax: 8                      # maximum radial order of cylindrical basis
            ncylodd: 3                   # vertically anti-symmetric basis functions
            ncylnx: 256                  # grid points in radial direction
            ncylny: 128                  # grid points in vertical direction
            vflag: 0                     # verbose output flag
            logr: false                  # logarithmically spaced radial grid
            density: false               # generate density basis functions
            eof_file: .eof.cache.run0    # EOF cache file name

The *ncylodd* parameters sets the number of vertically anti-symmetric basis functions. The first 
*nmax-ncylodd* basis functions are symmetric and the last *ncylodd* are vertically anti-symmetric. 
You can adjust these parameters to provide the desired number of basis functions, 
anticipating the degree of vertical symmetry. The parameters *acyl* and *hcyl* are the scale length and height,
respectively, in virial units. 

See :ref:`how to run simulations <howtosim>` for how to generate the relevant files.

3. ``Output:``

  The list of output methods to be run after each step at the user
  specified frequency.  Again, each list item begins with '-' and
  there are two fields:

  ==========     ===========
  Key word       Explanation
  ==========     ===========
  id             the name of the ``Output`` class
  parameters     a list of key: value pairs
  ==========     ===========


  The ``id`` is the class name in lower case.  The id value is
  parsed and used to construct a class of that type.  EXP
  will terminate with an error message if the class does not exist.
  You can have as many instances of these as you like (there might be
  occasional reasons to have duplicates). 
  See :ref:`EXP outputs <EXP-output>` for more information on EXP outputs
  and the parameter options.

4. ``External:``

  All of the external forces and phase-space manipulations that occur
  in addition to the gravitational fields generated by the phase space
  itself.  These have the same two fields as the ``Output`` node and
  the same overall keys: the ``id`` key is the class name in lower
  case and the ``parameters`` are a list key: value pairs.

5. ``Interaction:``

  This stanza defines the couplings between all of the phase-space
  components to exclude.  These may be toggled to explore the
  influence of the various phase-space components on each other.

  Key and Value pairs here define the interactions between components
  to remove.  Think: Key feels Value to get the sense of the
  interaction.

  If no pairs are listed, all components interact with each other.



More on the Global stanza
-------------------------

The allowed parameters in the ``Global`` stanza are listed in the
``Configuration files`` sidebar page in the Doxygen web documentation
which is reproduced here for completeness. We provide the key words and 
their definitions below, separating key words into those that are changeable
and of interest to users and those that are "expert" parameters that should 
generally not be changed unless there is a specific reason. When in doubt, use the
automatically supplied default value that you get without the key word.

  =============     ===========
  Key word          Explanation
  =============     ===========
  nsteps            maximum number of steps to execute
  nthrds            number of threads per process (e.g. one per processor)
  ngpus             the number of GPUs to assign on each node (can be more than the physical number)
  time              current or initial time on start up
  dtime             time step value
  NICE              Unix process priority
  VERBOSE           output logging level
  runtime           maximum runtime in wall clock hours
  multistep         number of time step levels
  ldlibdir          directory containing loadable modules
  infile            input file for restart
  parmfile          parameter dump file
  outdir            directory for output
  runtag            suffix or prefix used for labeling report files
  restart_cmd       command used to restart simulation on termination
  =============     ===========

**Expert Parameters**

These parameters should generally not need to be changed. We recommend that you
ommit them from the YAML file, which will ensure that the default values will
automatically be applied.

  =============     ===========
  Key Word          Explanation
  =============     ===========
  nbalance          number of steps between load balancing (use 0 for none)
  rlimit            virtual memory limit per process
  dbthresh          load balancing threshold (larger difference initiates balancing)
  PFbufsz           particle ferry buffer size (the size of the internal MPI particle buffer)
  ratefile          initial processor rate file
  global_cov        resets total center of velocity to zero if true 
  shiftlevl         shift at most this number of step levels at one time
  centerlevl        compute active centering below this multistep level (set to 1/2 the multistep level, multistep is most conservative)
  posnsync          synchronizes multistep positions at each substep (default: true)
  use_cwd           the Node 0 home dir for the working dir on all nodes
  dynfracV          time step velocity coefficient (default: 0.01)
  dynfracA          time step acceleration coefficient (default: 0.03)
  dynfracS          time step crossing time for an externally set scale (default: 1.0)
  dynfracS          time step potential/accerlation coefficient (default: 0.05)
  eqmotion          toggles phase space advance for use with externally supplied mapping.  On by default. 
  =============     =========== 

Additional metadata
-------------------

.. index: metadata; config; yaml
.. _add metadata:

You can include entries that are not part of the EXP YAML convention
and they will be ignored by EXP.  For example, you can include a
`Comment` stanza as follows:

.. code-block:: YAML

   Comment:
     - Project: This is Run0 for the tidal interaction project
     - Author: Martin Weinberg
     - Date: June 23, 2022
   # EXP will ignore the above stanza
   Global:
   .
   .
   .

