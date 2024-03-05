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
	 parameters : {rmax : 27.5}

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
  occasion reasons to have duplicates).

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
which is reproduced here for completeness.  When in doubt, use the
automatically supplied default value that you get without the key word.

  =============     ===========
  Key word          Explanation
  =============     ===========
  nsteps            maximum number of steps to execute
  nthrds            number of threads per process (e.g. one per processor)
  ngpus             the number of GPUs to assign on each node (can be more than than the physical number)
  nbalance          number of steps between load balancing (use 0 for none)
  dbthresh          load balancing threshold (larger difference initiates balancing)
  time              current or initial time on start up
  dtime             time step value
  PFbufsz           particle ferry buffer size (the size of the internal MPI particle buffer)
  NICE              Unix process priority
  VERBOSE           output logging level
  rlimit            virtual memory limit per process
  runtime           maximum runtime in wall clock hours
  multistep         number of time step levels
  shiftlevl         shift at most this number of step levels at one time
  centerlevl        compute active centering below this multistep level
  dynfracV          time step velocity coefficient (default: 0.01)
  dynfracA          time step acceleration coefficient (default: 0.03)
  dynfracS          time step crossing time for an externally set scale (default: 1.0)
  dynfracS          time step potential/accerlation coefficient (default: 0.05)
  use_cwd           the Node 0 home dir for the working dir on all nodes
  posnsync          synchronizes multistep positions at each substep (default: true)
  eqmotion          toggles phase space advance for use with externally supplied mapping.  On by default. 
  global_cov        resets total center of velocity to zero if true 
  ldlibdir          directory containing loadable modules
  infile            input file for restart
  parmfile          parameter dump file
  ratefile          initial processor rate file
  outdir            directory for output
  runtag            suffix or prefix used for labeling report files
  restart_cmd       command used to restart simulation on termination
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

