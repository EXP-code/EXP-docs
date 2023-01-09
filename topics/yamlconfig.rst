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
     outdir     : /home/weinberg/Nbody/DiskHaloExample
     nbodmax    : 100000
     nthrds     : 1
     dtime      : 0.05
     ldlibdir   : /home/weinberg/lib/user
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
