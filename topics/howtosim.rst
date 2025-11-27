.. _howtosim:

How to run your own N-body simulation in EXP
############################################

This tutorial will walk you through the steps to get started with running
your own N-body simulations in EXP. EXP uses YAML configuration files, and
we provide an :ref:`an annotated example <yamlconfig>` 
for reference as well as an :ref:`introduction to YAML syntax <yaml-primer>`. 
We will also need body and cache files, which we will discuss in more
detail below. These files can be generated within EXP, or you can provide
your own body file.

The general steps for creating an N-body simulation in EXP are to:

#. Generate a model file and body files. The model file contains the initial density distribution for your dark matter halo. The body file contains the initial phase space positions for (e.g.) your stellar disk and dark matter halo

#. Generate a cache file with your bases. In this example, you would need one cache file for your cylindrical (disk) basis and another for your spherical (halo) basis.
This is unnecessary in newer versions of EXP.  

#. Run a three-step relaxation process to ensure that your initial conditions are as quiet as possible

#. Run your simulation with EXP

#. Sanity check your output 

Step One: generate a model and body files
*****************************************
Model files are ascii files that contain the initial density distribution of your dark matter halo. We provide an example of how to create a  
model file from an analytic density distribution or a simulation snapshot in `the pyEXP-Examples repo <https://github.com/EXP-code/pyEXP-examples/blob/main/How-To/Recipes/Basis/generate%20GSE%20(Naidu%2B%202021)%20basis.py>`_. These files contain four columns that provide spherical radius values (R) along with
the density (D), mass enclosed (M), and gravitational potential (P) at that radius. Example  model files (ending in ``.model``,e.g. ``SLGridSph.model``) are provided in the DiskHalo, Halo, and NBody examples in the `EXP-Examples repo <https://github.com/EXP-code/EXP-examples/blob/main/>`_. Model files
must follow the file format of the provided examples.
 
Body files are ascii files that provide the initial phase-space information for your galaxy components. These could be generated from your favorite initial
conditions generator and translated into the correct format, or you could generate the files within EXP. The columns are particle mass, particle position
(:math:`x, y, z`), and particle velocity (:math:`V_x, V_y, V_z`). Example body files (ending in ``.bod``, e.g. ``halo.bod``) are provided in the Disk
Halo, Halo, and NBody examples in the `EXP-Examples repo <https://github.com/EXP-code/EXP-examples/blob/main/>`_. Body files must follow the same format as
these provided examples, and be in units where G = 1. The number of particles in the body files sets the number of particles that are in your simulation. 

Generating body files in EXP
----------------------------
The ``gendisk`` function, which lives in ``/utils/ICs``, can generate the body files for the disk and halo as well as the cache files (step three).
Parameters for ``gendisk`` are specified in a YAML file with the following fields:

.. code-block:: python

   CMAPR                : 1                    # Radial coordinate mapping type for cylindrical grid (0:none, 1:rational fct)
   CMAPZ                : 1                    # Vertical coordinate mapping type for cylindrical grid (0:none, 1:sech, 2:power in z
   DF                   : 1                    # Use change-over from Jeans to Eddington
   DFLAG                : 0                    # Output flags for DiskHalo
   DIVERGE              : 0                    # Cusp extrapolation for primary halo model
   DIVERGE2             : 0                    # Cusp extrapolation for number model
   DIVERGE_RFAC         : 1                    # Extrapolation exponent for primary mass model
   DIVERGE_RFAC2        : 1                    # Extrapolation exponent for number model
   DMFAC                : 1.0                  # Disk mass scaling factor for spherical deprojection model
   DR_DF                : 1.0                  # Width of change for to Eddington
   DUMPCOEF             : false                # Dump coefficients
   ASCALE               : XXXXX                # radial scale length for disk basis construction (e.g. 0.01)
   HSCALE               : XXXXX                # Vertical scale length for disk basis construction (e.g. 0.002)
   LMAX                 : 18                   # Number of harmonics for Spherical SL for halo/spheroid
   LMAXFID              : 128                  # Number of harmonics for Spherical SL for determining disk basis (may want to bump to 256)
   LOGR                 : true                 # Make a logarithmic coordinate mapping
   MMAX                 : 6                    # Number of azimuthal harmonics for disk basis
   CHEBY                : false                # Chebyshev smoothing
   NCHEB                : 12                   # Chebyshev order for smoothing if CHEBY = true
   NDP                  : 8                    # Number of angular wedges for disc 
   NDR                  : 2000                 # Number of points in DiskHalo radial table for disk
   NDZ                  : 800                  # Number of points in DiskHalo vertical table for disk
   NHR                  : 800                  # Number of points in DiskHalo radial table for halo
   NHT                  : 800                  # Number of points in DiskHalo cos(theta) table for halo
   NMAXH                : 18                   # Number of radial basis functions in Spherical SL for halo/spheroid
   NMAXFID              : 64                   # Number of radial basis functions in Spherical SL for determining disk basis (may want to bump to 128)
   NODD                 : 6                    # Number of vertically antisymmetric disk basis functions per M-order
   NMAXD                : 18                   # Number of disk basis functions per M-order
   NMAXLIM              : 10000                # Restricts disk basis function to NORDER1<NORDER after basis construction for testing
   NOUT                 : 18                   # Number of radial basis functions to output for each harmonic order
   NUMDF                : 1000                 # Number of grid points for Eddington inversion
   NUMR                 : 2000                 # Size of radial grid for Spherical SL
   NUMX                 : 256                  # Radial grid size for disk basis table
   NUMY                 : 128                  # Vertical grid size for disk basis table
   PNUM                 : 1                    # Number of azimthal knots for EmpCylSL basis construction quadrature
   RCYLMAX              : 20.0                 # Maximum disk radius in units of ASCALE
   RCYLMIN              : 0.001                # Minimum disk radius
   RFACTOR              : 1.0                  # Disk radial scaling factor for spherical deprojection model
   RMIN                 : 0.001                # Minimum halo radius
   RNUM                 : 200                  # Number of radial knots for EmpCylSL basis construction quadrature
   RSPHSL               : 1.95                 # Maximum halo expansion radius
   RTRUNC               : 0.1                  # Maximum disk radius for erf truncation of EOF conditioning density
   RWIDTH               : 0.0                  # Width for erf truncation of r EOF conditioning density (ignored if zero)
   R_DF                 : -1.0e20              # Change over radius for Eddington (default is all Eddington)
   SCMAP                : 1                    # Turn on Spherical SL coordinate mapping (1, 2, 0:off)
   SCSPH                : XXXXX                # Scale for Spherical SL coordinate mapping - this should match rmapping in exp
   SEED                 : XXXXX                # Random number seed (e.g. your favorite number)
   SELECT               : false                # Enable significance selection in coefficient computation
   SHFAC                : 16                   # Scale height factor for assigning vertical table size
   TNUM                 : 80                   # Number of cos(theta) knots for EmpCylSL basis construction quadrature
   ToomreQ              : XXXXX                # Toomre Q parameter for stellar disk generation (e.g. 1.4)
   U0                   : 0.0                  # Disk-Halo x velocity center position
   V0                   : 0.0                  # Disk-Halo y velocity center position
   VFLAG                : 8                    # Output flags for EmpCylSL
   W0                   : 0.0                  # Disk-Halo z velocity center position
   X0                   : 0.0                  # Disk-Halo x center position
   Y0                   : 0.0                  # Disk-Halo y center position
   Z0                   : 0.0                   # Disk-Halo z center position
   basis                : false                # Print out disk and halo basis
   ignore               : XXXXX                # 'true' if you want to generate and save out cache files, otherwise 'false'
   cachefile            : XXXXX                # Name of EOF cache file (e.g. eof.cache.fileF)
   centerfile           :                      # Read position and velocity center from this file
   constheight          : true                 # Use constant disk scale height
   dbods                : disk.bods            # Disk particle output file
   deproject            : EXP                  # set deprojection model (Exponential or MN)
   disk_mass            : XXXXX                # Mass of stellar disk (e.g. 0.0125)
   dtype                : exponential          # Disk type for condition (one of: constant, gaussian, mn, exponential)
   expcond              : true                 # Use analytic density function for computing EmpCylSL basis
   gentype              : Asymmetric           # DiskGenType string for velocity initialization (Jeans, Asymmetric, or Epicyclic)
   halofile1            : XXXXX                # File with input halo model (your .model file here)
   evolved              : false
   hbods                : halo.bods            # Halo particle output file
   multi                : false                # Use multimass halo
   ndisk                : XXXXX                # Number of disk particles (e.g. 1000000)
   nhalo                : XXXXX                # Number of halo particles (e.g. 10000000)
   report               : false                # Report particle progress in EOF computation
   runtag               : XXXXX                # Label prefix for diagnostic images (e.g. 'run1')
   scale_height         : XXXXX                # Scale height for disk realization (e.g. 0.002)
   scale_length         : XXXXX                # Scale length for disk realization (e.g. 0.01)
   threads              : 1                    # Number of lightweight threads
   zerovel              : true                 # zero center of mass and velocity
   suffix               : ""

Parameters that have values set to 'XXXXX' are those that users are encouraged to change. Example values are given in the
comment following the parameter value. The remaining parameters are "expert parameters" and generally do not need to be changed
unless you have a good reason to use a different value. The listed parameter values are the defaults. Note that the ``exponential`` disk is
exponential in R and :math:`sech^2` in z.

To generate the initial conditions, you would run:

.. code-block:: python

   mpirun gendisk --config gendisk_step1.yml 

in the terminal, replacing ``gendisk_step1.yml`` with the name of your YAML file that specifies the ``gendisk`` parameters. If
you set ``ignore = true``, it may take a moment to generate the cylindrical bases cache file. The cylindrical bases will be
saved out to whatever name is specified in ``cachefile``, and the halo basis will generally be saved out to
``.slgrid_sph_cache``. Note that the ``diskgen`` YAML file here is distinct from the EXP YAML config file, EXP YAML config files 
look like :ref:`this annotated example <yamlconfig>`.

Step Two: generate cache files
******************************
If you didn't generate cache files in step one and you have an old install of EXP, you need to generate these files now. An example of how to do this is in the
`pyEXP-Examples repo <https://github.com/EXP-code/pyEXP-examples/blob/main/How-To/Utilities/create%20Cylinder%20basis%20(parallel).py>`_.
If you are including a stellar disk in your simulation, EXP requires that you provide a cylindrical cache file with a name that matches
the ``cachename`` for the **star disk** in the EXP YAML config file. You are not required to provide a spherical cache file, as it is much 
faster to compute the spherical cache file than the cylindrical cache file. You must specify a name for the spherical cache file in the 
EXP YAML config file, and if that file does not exist, EXP will generate the spherical cache file on-the-fly and save it as the specified name.

Step Three: three-part relaxation process (**optional**)
*********************************************************
We recommend a performing the following three step process to produce quiet initial conditions. This process minimizes ringing and other symptoms of
slight dynamical disequilibrium in the initial conditions by allowing the disk and halo to adjust and virialize in the presence of one another before
starting the full simulation. The steps are as follows:

A. After creating your disk and halo body files, relax the halo in the presence of the disk. To do this, set the following parameters in the ``force`` parameter map for the halo portion of the EXP YAML config to true:

.. code-block:: python
   
   self_consistent:       true
   EVEN_L:                true
   M0_ONLY:               true

and set ``self_consistent`` in the ``force`` parameter map of the disk portion of the EXP YAML config to false

.. code-block:: python
   
   self_consistent:       false

(see e.g. :ref:`an annotated example <yamlconfig>`). The rest of your config YAML file should be as normal. Lets call this YAML file "first_step_config.yml". We suggest running for at least T ~ 4 Gyr, though you should check the output coefficients to know if you should run for longer. Note that in the YAML config, you can reduce the cadence of when phase space dumps (i.e. snapshots) are saved out to avoid unnecessarily cluttering up your storage. The ``acyl`` and ``hcyl`` parameters should match ``ascale`` and ``hscale`` in your ``gendisk`` YAML config file. Run EXP with this YAML config file:

.. code-block:: python

   mpirun -v exp --config first_step_config.yml

B. Generate a new disk in your newly relaxed halo. To do this, you'll need to convert the last phase space output of the EXP run in the previous step into a properly formatted body file. You can do this in the terminal using ``psp2ascii``:

.. code-block:: python 

   psp2ascii -a -f your_file_name_here.last_timestep -o your_chosen_outfile_name.diag

followed by:

.. code-block:: python

   cp your_chosen_outfile_name.diag.halo your_chosen_outfile_name.diag.halo.diag

to comply with naming conventions. Here we have assumed that the ``name`` for your dark matter halo in first_step_config.yml was 'halo'. You can now use this body file as an input to ``gendisk`` to generate your new disk in this halo. Make a copy your original ``gendisk`` YAML file and give the copy a new name. In this example, we'll call this new copy "gendisk_step2.yml". Pick a name for your new disk body file and change the following lines in your copied ``gendisk`` YAML file:

.. code-block:: python

   hbods:        your_chosen_outfile_name.diag.halo.diag
   evolved:      true
   dbods:        disk_step2.bod

here we call our new disk body file "disk_step2.bod". Run ``gendisk`` with ``--config`` set to this new YAML file.

C. Relax this disk in the presence of the halo. Make a copy of your original EXP YAML config file and rename it, we'll call this new file "third_step_config.yml" in our example. In your copied EXP YAML config file, change the following lines in the ``force`` parameter map of the halo:

.. code-block:: python

   self_consistent:     false
   EVEN_L:              true
   M0_ONLY:             true

and the following lines in the ``force`` parameter map of the disk:

.. code-block:: python

   self_consistent:     true
   mlim:                0

Finally, set the disk and halo ``bodyfile`` parameters to your updated body files (here we would set the halo ``bodyfile`` to your_chosen_outfile_name.diag.halo.diag and the disk ``bodyfile`` to disk_step2.bod). Setting ``mlim`` to zero here allows only axisymmetric structure to evolve. Run EXP with this edited YAML config file, we recommend allowing the system to evolve for at least T ~ 2 Gyr. As before, you can set a low cadence for saving out phase space dumps to reduce the amount of storage used in this step.  The last phase space dump from this step will be the input initial conditions (body files) for your full run of the simulation. Follow the procedure given in B to get the phase space files into the proper body file format, remembering to separate the phase space file into the stellar and dark components for the disk and halo body files, respectively. 

As a final note, the symmetries in the ``sphereSL`` (i.e. dark matter halo) can be controlled by setting the following options to true or false:

``NO_L0`` -  turn off the monopole component (you've supplied a background model!)

``NO_L1`` - turn off the dipole component

``EVEN_L`` - only allow even harmonic orders to evolve

``EVEN_M``  - only allow even harmonic subspaces to evolve

``M0_ONLY`` - only allow the m=0 harmonic subspace to evolve

``self_gravity`` - allow the component to evolve

with similar options for the stellar disk.

Step Four: run the simulation
******************************
Run your full simulation! Make an EXP YAML config file, we'll call ours "real_run_config.yml", then run it with ``mpirun -v exp --config first_step_config.yml`` . If you skipped Step 3, you'll set the disk and halo ``bodyfile`` parameters in the EXP YAML config file to the files from Step 1. If you did the full three-step relaxation process, you'll need to reformat the last phase space output from Step 3C into disk and halo body files, then you will set the ``bodyfile`` parameters to these new body files. If you generated your own disk initial conditions, the ``acyl`` and ``hcyl`` parameters should match ``ascale`` and ``hscale``, respectively, in your ``gendisk`` YAML config file (note that ``scale_length`` and ``scale_height`` can differ from ``acyl`` and ``hcyl``). For the real run of your simulation, ``self_consistent`` should be set to true for all components and ``mlim`` should be set to a value equal to or greater than your ``mmax`` parameter  (instead of setting these explicitly, these lines can be omitted from the EXP YAML config file which will set these values to the sensible defaults). 

Step Three and Four can be run with a ``.sh`` script, and could even be combined into a single script. If you're using a machine with SLURM, you can set the SLURM parameters at the top of the script.

Step Five: sanity check your output
***********************************
You've run your first simulation with EXP! You should check that the results are sensible. You can do this in a few ways, we provide a few checks that we like to perform. If you have additional checks that you do, please contribute these!

#. Inspect the phase space dumps at a few times in the simulation. Do you see big rings at early times? A three armed spiral/bar? These patterns can be a sign of issues with dynamical equilibrium in the initial conditions. You can do the three step relaxation procedure to help ensure a quiet start

#. Inspect ``OUTLOG file``, which should live in the same directory as your phase space dumps. Plotting column 1 versus 38 and column 1 versus 58 is a helpful diagnostic - these plots will show the virial parameter (i.e. :math:`-2T/V_c`, where :math:`V_c` is the Virial of Clausius) for the halo and disk, respectively. Perfect equilibrium would have :math:`-2T/V_c = 1` - this plot should look like tiny oscillations around one.

#. Look at some orbits of star particles. Are they sensible? 


