.. _replay:

Replaying a simulation using EXP
================================

This is an EXP topic.  For doing this with pyEXP, please see
:ref:`generating orbits in your BFE potential fields <orbits>`.

Recall that EXP uses a YAML configuration files.  Here is :ref:`an
annotated example <yamlconfig>` for reference.  We also provide a
general :ref:`quick intro to YAML syntax <yaml-primer>`.

EXP can use an existing coefficient file to generate forces instead of
self-consistently using the particles to generate the coefficients. 
This is done by adding the ``playback`` key word to the component
parameter options.  For example:

.. code-block:: yaml
		
   Components:
     - name       : dark halo
       force      :
       id         : sphereSL
       parameters : {..., playback: outcoef.xxxx.h5}

where ``outcoef.dark.run0.h5`` is the coefficient file for
simulation.  You can playback one component (specifying one coefficient file) with the others
self-consistent or playback all components by specifying ``playback``
for every component.  

There are two additional parameters that control the computation in
``playback`` mode.  The boolean parameter ``coefCompute`` set to true
will compute a new set of parameters from the particles in the
component whose force is played back.  In addition, the boolean
``coefMaster`` set to true does the interpolation of the coefficient
from the file on the master and sends the result to the worker nodes.
If set to false (the default), the coefficients are interpolated on
each worker node.  This option saves some memory overhead on worker
nodes but the results should be the same.

Use cases
---------

Playback mode has a number of possible uses:

* Apply a the force field from a previous simulation to further resolve a phase-space sample at fine scales

* Apply a the force field from a previous simulation to a new component such as a star cluster, satellite or stream

* Quickly generating orbit traces for some small subset of particles. This may also be done using pyEXP as described :ref:`here <orbits>`.
