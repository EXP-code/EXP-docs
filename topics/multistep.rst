.. _multistep:

The EXP multistep implementation
================================

Overview
--------

EXP uses binary time-step tree to increase dynamical throughput for
simulations with large dynamic range in characteristic orbital times.
Time steps for each particle are chosen to be the minimum of 4
standard criteria (see below) and one criteria that may be applied by
user-defined modules (see :ref:`user modules <usermodules>`).
In practice, this multiple time stepping algorithm improves throughput
by an order of magnitude for CPU computations.  Less so for
GPU computations but it often still results in a factor of two gain.

Time step criteria
~~~~~~~~~~~~~~~~~~

.. index: time step criteria


1. The natural radius time scale: :math:`|r_{scale}|/|\mathbf{v}`,
   where :math:`r_{scale}` represents an internal or preset length
   scale.  This is only used when provided by an external user routine
   or in the Particle structure.

2. The characteristic drift time scale:
   :math:`|r_{char}|/|\mathbf{v}|`, where :math:`r_{char}` represents the
   natural length scale for the system.  For simplicity, we set
   :math:`r_{char}=1` and let the user tune the prefactor for their own
   system units (see below on tuning parameters). This criterion
   decreases the step size to follow fast particles.  Because this
   criterion is position dependent, it is given a very low weight by
   default.  The user may enable this criterion by setting `dynfracD` to
   some small value.

3. The force time scale: :math:`|\mathbf{v}|/|\mathbf{a}|` where
   :math:`\mathbf{a}` is the acceleration.

4. The work time scale: :math:`|\Psi|/|\mathbf{v}\cdot\mathbf{a}|` where
   :math:`\Psi` is the gravitational potential chosen to be 0 at large
   distances from the center of the particle distribution.

5. The escape time scale:
   :math:`\sqrt{|\Psi|/\mathbf{a}\cdot\mathbf{a}}`.
   This is derived by computing the time required to climb out of the
   potential well with magnitude :math:`|\Psi|` at fixed value of
   acceleration :math:`|\mathbf{a}|`.

Each of these are tuned by the prefactors :math:`\epsilon_S, \epsilon_D,
\epsilon_V, \epsilon_A, \epsilon_P` which are the following global
variables in the configuration file: `dynfracS, dynfracD, dynfracV,
dynfracA, dynfracP`.  These values must be calibrated for
a specific problem at hand, but values of order 0.01 would be typical.
Although I tend to be rather conservative about this.  When in doubt,
check individual representative orbits based on your own needs.  A
particular criterion can be ignored by choosing a large value for the
corresponding :math:`\epsilon`.

Finally, a fifth criterion is a specific field carried by a particle
that requests a particular time step.  Again, the value of this field,
`dtreq`, is zero by default.  A non-zero value of :index:`dtreq` will
fold this request into all of the other time step criteria. Code
developers take note: there is no tuning parameter for this criterion.

The Leapfrog integrator
-----------------------

.. index: pair: multistep; leapfrog

EXP uses a particular version of the symplectic Leapfrog
integrator.  We begin with a quick review.  Hamilton's equations for
our Hamiltonian :math:`H = p^2/2 + \Phi(\mathbf{x})` read

.. math::
   \dot{\mathbf{q}} = \frac{\partial H}{\partial\mathbf{p}}
   \dot{\mathbf{p}} = -\frac{\partial H}{\partial\mathbf{q}}

or, compactly,

.. math::
   \dot{\mathbf{z}} = \mathbf{f}(\mathbf{z}, t)

where :math:`\mathbf{z} = (\mathbf{q}, \mathbf{p})` and

.. math::

   \mathbf{f} = \left(
   \frac{\partial H}{\partial\mathbf{p}}, 
   -\frac{\partial H}{\partial\mathbf{q}}
   \right).

We can discretize this Hamiltonian by replacing :math:`H(\mathbf{q},
\mathbf{p})` by

.. math::
   H_h(\mathbf{q}, \mathbf{p}, t) = \frac{p^2}{2} + \Phi(\mathbf{q})\delta_h(t)

where

.. math::
   \delta_h(t) = h\sum_{k=-\infty}^{k=\infty}\delta(t + kh).

If we average over a time interval long compared :math:`h`, the new
Hamiltonian system should approach the original Hamiltonian system in
the limit :math:`h\rightarrow0`.

This discretization allows us to develop an algebra to create
Hamiltonian mappings.  To see this, integrate the equations of motion
from :math:`t=-\epsilon` to :math:`t=\epsilon` where
:math:`0<\epsilon\gg h`.  The resulting value of
:math:`\mathbf{z}_\epsilon\equiv\mathbf{z}(t=\epsilon)` is:

.. math::
   \mathbf{q}_\epsilon = \mathbf{q}; \qquad \mathbf{p}_\epsilon =
   \mathbf{p} - h\mathbf{\nabla}\Phi(\mathbf{q}).

This is called a *kick* because the momentum changes but the
position remains the same.  Next, between :math:`t=\epsilon` and
:math:`t=h-\epsilon`, the value of the delta function is zero, so the
system has constant momentum.  Therefore, Hamilton's equations yield:

.. math::
   \mathbf{q}^\prime = \mathbf{q}_\epsilon + h\mathbf{p}_\epsilon; \qquad
   \mathbf{p}^\prime  = \mathbf{p}_\epsilon.

This is called a *drift* because the position changes but the
momentum remains the same.  Combining these results, we can define an
\emph{integrator} as a Hamiltonian mapping :math:`(\mathbf{q},
\mathbf{p})\rightarrow(\mathbf{q}^\prime, \mathbf{p}^\prime)` over
the time step :math:`h` beginning at :math:`t=-\epsilon` as follows:

.. math::
   \mathbf{p}^\prime = \mathbf{p} - h\mathbf{\nabla}\Phi(\mathbf{q});
   \qquad \mathbf{q}^\prime = \mathbf{q} + h\mathbf{p}^\prime.

If we start at :math:`t=\epsilon` we get the map:

.. math::
   \mathbf{q}^\prime = \mathbf{q} + h\mathbf{p}; \qquad
   \mathbf{p}^\prime = \mathbf{p} - h\mathbf{\nabla}\Phi(\mathbf{q}^\prime).

These define the *kick-drift* and *drift-kick* modified Euler
integrators.  The error for each step is :math:`\mathcal{O}(h^2)` so
these are first-order integrators.

By alternating kick and drift steps, we can construct higher-order
integrators ([yoshida93]_).  In particular, a scheme where we drift
for :math:`h/2`, kick for :math:`h` and drift for :math:`h/2` gives
the *drift-kick-drift* Leapfrog scheme:

.. math::
   \begin{equation}
   \mathbf{q}_{1/2} = \mathbf{q} + \frac{h}{2}\mathbf{p}; \qquad
   \mathbf{p}^\prime = \mathbf{p} -
   h\mathbf{\nabla}\Phi(\mathbf{q}_{1/2}); \qquad \mathbf{q}^\prime =
   \mathbf{q}_{1/2} + \frac{h}{2}\mathbf{p}^\prime.
   \end{equation}

We can flip the steps to get a *kick-drift-kick* form of
Leapfrog:

.. math::
   \begin{equation}
   \mathbf{p}_{1/2} = \mathbf{p} - \frac{h}{2} \mathbf{\nabla}\Phi(\mathbf{q});
   \qquad \mathbf{q}^\prime = \mathbf{q} + h\mathbf{p}_{1/2}; \qquad
   \mathbf{p}^\prime = \mathbf{p}_{1/2} - \frac{h}{2}
   \mathbf{\nabla}\Phi(\mathbf{q}^\prime).
   \end{equation}

Direct computation by Taylor series expansion shows that the error in
the mapping from :math:`t` to :math:`t+h` for the leapfrog algorithm is:

.. math::
  \mbox{error} = 1/6 h^3|\mathbf{q}^{[3]}(t)|.

Discussion
~~~~~~~~~~

The leapfrog integrator has many virtues:

- It is second- rather than first-order accurate, in that the
  error in phase-space position after a single timestep is
  :math:`\mathcal{O}(h^3)`;

- Leapfrog is time reversible in the sense that if leapfrog
  advances the system from :math:`(\mathbf{q}, \mathbf{p})` to
  :math:`(\mathbf{q}^\prime, \mathbf{p}^\prime)` over interval :math:`h`, it
  will also advance it from :math:`(\mathbf{q}^\prime,
  -\mathbf{p}^\prime)` to :math:`(\mathbf{q}, -\mathbf{p})`.  That is,
  leapfrog is time reversible.  Time-reversibility is a constraint
  on the phase-space flow that, like symplecticity, suppresses
  numerical dissipation, since dissipation is not a time-reversible
  phenomenon

- A sequence of :math:`n` leapfrog steps can be regarded as a drift
  step for :math:`1/2 h`, then :math:`n` kick-drift steps of the modified
  Euler integrator, then a drift step for :math:`-1/2 h`.  Thus, if
  :math:`n\gg1`, the leapfrog integrator requires negligibly more work
  than the same number of steps of the modified Euler integrator.

- Leapfrog also needs no storage of previous timesteps, so is
  economical of memory.

Because of all these advantages, most codes for simulating
collisionless stellar systems use the leapfrog integrator.

The basic multistep algorithm
-----------------------------

.. index: multistep

A binary time-step tree can dramatically increase throughput,
especially for the generic fully MPI implementation.
We begin by partitioning phase space :math:`m` ways such that each partition
contains :math:`n_j` particles that require a time step

.. math::
   \delta t=2^{-j} h

where :math:`h` is the largest time step and :math:`j=0,\ldots,m`.
The timestep for :math:`j=m` corresponds to the one that would be
required for a single time-step simulation.  Since the total cost of a
time step is proportional to the number of force evaluations, the
speed up factor is:

.. math::

   \mathcal{S} = \sum_{j=0}^{m}n_j/\sum_{j=0}^{m}
   n_j 2^{-j}.

For example, for an :math:`c=15` NFW dark-matter profile with
:math:`N=10^7` particles, we find that :math:`m=7` and
:math:`\mathcal{S}\approx 30`, an enormous speed up!  Forces in the
SCF algorithm depend on the expansion coefficients and the leap frog
algorithm requires linear extrapolation of these coefficients to
maintain second-order error accuracy per step.  This extrapolation and
the bookkeeping required for successive bisection of the time interval
is straightforward.  We checked the accuracy of this algorithm by
comparing to direct orbit integration methods.  This time stepping
algorithm will allow us to regularly compute models with
:math:`N=10^8` and occasionally models up to :math:`N=10^9`.

BFE implementation
------------------

The contribution to the expansion coefficients for all particles on a
particular level are stored separately for the current and previous
step.  Thus, each level maintains a full set of coefficients
corresponding to the contribution of particles at that level.  We call
this the *coefficient tableau*.  When computing the total
coefficients at particular multistep level, the offset of the velocity
update at the half step allows the coefficient contribution at the
lower inactive levels to be linearly interpolated.  The error in the
contribution from the interpolation is the same order as that for leap
frog itself.

The particle time step is computed after each step.  If a particle has
changed levels, its previous contribution is substracted from its
former level and its updated contribution is added to its new level.

The details
~~~~~~~~~~~

As described above, each particle is assigned a time
step *level*.  For each level with index :math:`j`, the coefficient
tableau is defined as the particles contributions restricted to that
level.  Define an indicator :math:`\zeta_j(k) = 1` if Particle :math:`k` is in
level :math:`j`, and zero otherwise.  With this definition, the
coefficient tableau becomes

.. math::
   \begin{equation}
   \hat{a}_n^j(t+hi/2^{m}) = \sum_{k=1}^N m_k \zeta_j(k) \phi_n(x_k)
   \label{eq:coeft}
   \end{equation}

where :math:`i\in[0, 1, \ldots, 2^{m}-1]` are the sub steps required for
the full time step interval :math:`h`.  We get the full coefficient given
in equation (\ref{eq:coefp})  summing over :math:`j`: :math:`\hat{a}_n(t) =
\sum_{j=0}^m \hat{a}_n^j(t)`.

For particles at Level :math:`l`, each time step is :math:`h/2^l`.  For
example, let us consider only two levels in total, :math:`m=1`. Particles
at Level 0 have time step :math:`h`. Applying the kick and drift steps
from the \emph{kick-drift-kick} algorithm in equation (\ref{eq:lfkdk})
brings the positions of Level 0 particles to the next time step.  This
allows us to evaluation :math:`\hat{a}_n^0(t)`, but in order to perform
the final kick step, we need :math:`\hat{a}_n(t+h) = \hat{a}_n^0(t+h) +
\hat{a}_n^1(t+h)`.  The second term requires advancing the particles
at higher levels.  Now consider the Level 1 particles.  The first sub
step brings the positions of Level 1 particles to :math:`t + h/2`. To
evaluate :math:`\hat{a}_n(t+h/2) = \hat{a}_n^0(t+h/2) + \hat{a}_n^1(t+h/2)`,
:math:`\hat{a}_n^1(t+h/2)` can be evaluated from the current positions,
but we need we need :math:`\hat{a}_n^0(t+h/2)`.  We approximate this by
linear interpolation:

.. math::
   \hat{a}_n^0(t+h/2) = \frac{\hat{a}_n^0(t) + \hat{a}_n^0(t+h)}{2}.

This allows us to compute the next kick and drift, bringing all
particles to the time :math:`t+h` which allows the evaluation of the
final kick for all particles.  The error in the force (acceleration)
interpolation is :math:`\mathcal{O}(h)` and contributes to an error in
the trajectory proportional :math:`|\mathbf{q}^{[3]}|`. Propagating
this error using equations (\ref{eq:lfkdk}), we find that the error
from the linear interpolation is the same order as the leapfrog itself
so there is no need for higher-order interpolation.

The extension to any number of levels is straightforward.  Consider
sub step :math:`i` at Level :math:`l`.  The fraction of the full step :math:`h` is
:math:`f \equiv i/2^{m}`.  The last fractional step for Level :math:`o<l` is
:math:`g_- \equiv \lfloor i/2^{m-o} \rfloor /2^{o}` and the next fraction
step is :math:`g_+ \equiv \lceil i/2^{m-o} \rceil /2^{o}`.  Then, at each
level :math:`l`, all particles at Level :math:`o<l` are advanced using the
following interpolation in coefficients:

.. math::
  \hat{a}_n^o(t+hf) =
  \frac{\hat{a}_n^o(t+hg_-) [f - g_-]  + \hat{a}_n^0(t+hg_+) [g_+ - f]}{g_+ - g_-}.

In our previous example for :math:`m=1`, at time :math:`t+h/2`, we have
:math:`i=1`.  For :math:`o=0`, we gave :math:`g_- = 0` and :math:`g_+ = 1`.  For a
more complex example, consider :math:`m=2`, at time :math:`t+h/4` which is
again :math:`i=1`.  For :math:`o=1`, we gave :math:`g_- = 0` and :math:`g_+ = 1/2`.
So, using equation (\ref{eq:cinterp}), we have:

.. math::
   \begin{eqnarray*}
   \hat{a}_n^1(t+h/4) &=&
   \frac{\hat{a}_n^1(t) (1/4 - 0) + \hat{a}_n^1(t+h/2) [1/2 - 1/4]}{1/2}
   \\
   &=& \frac{\hat{a}_n^1(t)+ \hat{a}_n^0(t+h/2)}{2}.
   \\
   \end{eqnarray*}

Level update
~~~~~~~~~~~~

We compute the time-step level for each particle at the end of each
sub time step using the algorithms described above.  We flag level
changes and update the coefficient tableau by computing a difference
array at the current level that describes the change to each lower or
higher level.  This is straightforward for levels greater or equal to
the current level but requires rolling back the trajectory to a
previous time for levels smaller than the current level.  Therefore,
the level update is most easily applied at the top level (Level 0)
where all times are synchronized.

Algorithm summary
-----------------

1. The global variable \texttt{multistep} sets the number of time
   step levels.  Each successive level has time step :math:`t_0/2^l` where
   :math:`l` is the level counter and :math:`t_0` is master time step,
   the parameter `dtime`.  Theerfore the smallest stepping interval
   is :math:`t_0/2^{multistep}`.

2. All bodies start on highest level :math:`l=\mbox{multistep}`
   (smallest time step) to start on the first step.  After the first
   step, new levels are computed and the multistep coefficient tableau
   is updated.

3. At each substep, particle time steps are recomputed.  Particles
   that change levels are flagged.  At the end of the step, a particle
   update tableau is computed on each node and sum reduced over all
   nodes.


External time step variable
---------------------------

The `Particle` structure has two time step specific variables
`dtreq`, the user-specified time step, and `scale`, the
intrinsic scale for the particle.  If these values are less then zero,
the user-requested time step criterion or the characteristic drift
time scale, respectively, are ignored.  These values are set to -1 by
default (ignored).

.. [yoshida93] H. Yoshida. Recent Progress in the Theory and
	       Application of Symplectic Integrators. Celestial
	       Mechanics and Dynamical Astronomy, 56:27–43, Mar. 1993.
