.. _centering:

=========
Centering
=========

Although BFEs are inherently non-parametric, practical use of a BFE
requires a truncation of an infinite series of terms, and therefore
the reconstructed fields depend on the expansion center [#f1]_. To help
with this issue, every `Component` has the option of centering the
expansion on a fraction of the most bound particles, which we call
:math:`E`-centering.  Similarly, the basis may be rotated to realign
the vertical axis with the current :math:`L_z` axis, which we call
:math:`J`-centering. Both may be used together.

The algorithms for both centering types rely on the same logic as
follows.  The user specifies the desired number of states for
specifying the center or orientation, called ``nEJwant``.  On the
first call, all particles are ranked by binding energy.  The
``nEJwant`` values are retained and the center-of-mass and/or angular
momentum values are computed from this central component.  The maximum
potential (minimum binding energy) in this group is recorded for
subsequent steps, :math:`E_{max}`.  On subsequent steps, particles are
tested for membership if the EJ particle group is not full or has
energy value :math:`E<E_{max}`.  If a candidate member has a lower
potential value than one currently on the list, it is accepted for
membership.  Subsequent calls are offset by the time interval
``EJdT``.  The default value is 0, which implies an EJ computation on
every step. This value can be set to a preassigned time larger than
the step size to reflect the interesting dynamical times for the
user's system.

The center-of-mass position for this new EJ group may be used to
recenter the expansion or rotate the distribution to best align the
vertical direction with :math:`L_z`.  The rotation is performed by the
Euler matrix whose that makes the :math:`L_z` direction the transformed
:math:`z` axis with the new :math:`x` axis along the line of nodes.

The naive application of these transformations is jittery.  To reduce
the jitter, we only perform the transformation after first logging
``nEJkeep`` steps.  We use a linear least-squares solution of temporal
trajectory of both the center and the :math:`L_x, L_y, L_z` axes to
predict the current value of the center and axes.  We retain the last
``nEJkeep`` data points for all subsequent steps.  We provide the user
the option to *damp* the linear solution by interpolating to an
earlier time point by setting the ``EJdamp`` value less than its default
value of one.

The EJ algorithm is controlled by the ``EJ`` bit flag in the
``Component`` configuration.  A value ``1``, ``2`` enables
axis-orientation and centering, respectively.  For example, both may
be enabled by setting ``EJ: 3``. Diagnostic information about the EJ
center computation is enabled by setting ``EJdiag: true``.  We often
use the EJ centering computation as an internal diagnostic without
changing the expansion center by using ``EJdryrun: true`` along with
``EJdiag: true``.  We strongly recommend doing this for simulations of
isolated galaxies.  See :ref:`yamlconfig` for an example of setting EJ
parameters in the component stanza of the YAML config file.

.. rubric:: Footnotes

.. [#f1] Of course, a non-truncated one does not, owing to the
         translation property of harmonics.  In other words, the
	 center would be irrelevant with a arbitrarily large number of
	 terms in the expansion.
