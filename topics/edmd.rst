.. _edmd:

Extended Dynamical Mode Decomposition
=====================================

.. index:: pair: Extended Dynamical Mode Decomposition; EDMD

Dynamical Mode Decomposition (DMD) is a a method for extracting
underlying linear dynamics from complex non-linear data.  This method
originates in the general proof by Koopman that a finite dimensional
non-linear dynamical flow maps on to a linear infinite dimensional
flow.  The theorem *does not* help us find that mapping and it's very
hard in general.  In essence, DMD is a high-dimensional finite
approximation to the infinite dimensional mapping envisioned by
Koopman (usually called a *Koopman operator*).  In essence, the DMD is
identifies the best-fit linear dynamical system in a least-squares
sense from samples of a flow that advances high-dimensional
measurements forwards in time. This is similar to and often justified
by the mathematical structure of the Koopman operator which also
advances the observation of a state at a given time to the next time
step.

Part of the growing attraction of DMD is attributed to its
equation-free nature. Although some dynamical systems could be modeled
from first principles (e.g. a set of ordinary differential equations),
many dynamical systems have unknown governing equations. Even within
systems with known dynamics, it is difficult uncover patterns that
allow for the characterization of how dominant behaviors evolve in
time.

Koopman Operators
-----------------

.. index:: pair: Extended Dynamical Mode Decomposition; Koopman operators

Consider dynamical systems that can be modeled as:

.. math::
   \mathbf{\dot{x}} = \mathbf{F}(\mathbf{x})

where the current state :math:`\mathbf{x}` is an element a state space
:math:`{\cal M}\in\mathbb{R}^n` and :math:`\mathbf{F}` is a flow
field.  If we discretize this problem we get:

.. math::
   \mathbf{x}_{j+1} = \mathbf{A}(\mathbf{x}_j)

where :math:`\mathbf{A}` is the mapping that represents the mapping
from time :math:`t=t_0 + hj` to :math:`t=t_0 + h(j+1)` where :math:`h`
is the numerical integration time step.  Since we are interested in
the prediction of time-steps of the dynamical system such as an N-body
simulation, we will be generally interested in this discrete time
formulation.

In 1931, Bernard Koopman [koopman31]_ proposed the existence of a
compositional operator for any dynamical system that that results in
linear system for the appropriate span of functions in Hilbert space.
This composition is now known as the Koopman operator.  It is usual
written as follows:

.. math::
   {\cal K}(t)\mathbf{g}(\mathbf{x}) = \mathbf{g}\circ\mathbf{F}(t, \mathbf{x})

where :math:`{\cal K}` denotes the Koopman operator which is a linear
transformation and :math:`\mathbf{F}` is the dynamical flow. 

This sounds too good to be true.  And it is.  The downfall here is
that the Koopman operator updates some unknown vector of real valued
functions of this dynamical system, usually called _observables_ which
echos the origin of this idea in quantum mechanics.  These
_observable_ functions, :math:`g(\mathbf{x})` that make the system
linear are unknown.  In the language of functional analysis, 
the vector space of these observables is infinite.  Figuratively, the
use of Koopman operators as a trade off from simple set of physically
motivated phase-space variables with non-linear dynamics to
complicated set of functions with simple dynamics.

.. note:: The following sections provides mathematical details of
	  extended Dynamical Mode Decomposition for motivation of the
	  method and to better describe its relationship to
	  multichannel SSA, and its implementation in EXP.  Feel free
	  to skip this on your first read through.  Some of this
	  presentation partly follows [brunton21]_.

Koopman Spectral Analysis
-------------------------

.. index:: pair: Extended Dynamical Mode Decomposition; Koopman spectral analysis

The discrete mapping version of the continuous Koopman operator has a
very similar form:

.. math::
   {\cal K}\mathbf{g}(\mathbf{x}) = \mathbf{g}\circ\mathbf{A}(\mathbf{x})

Our end goal is an estimation of the operator :math:`{\cal K}` directly from
the basis-function coefficients from our simulations.  This estimation
process is called extended Dynamical Mode Decomposition and will be
described below.  This will assume that the dynamics is
time-indepdendent; that is, :math:`{\cal K}` and :math:`A` are indepdendent
of time.

Let us assume that we know the Koopman operator eigenfunctions of
:math:`{\cal K}`: :math:`{\cal C}\phi_j = \lambda_j\phi_j` where
:math:`j` may be countably infinite.  In practice, we will have
:math:`j<M`.  Then, all of our observable functions
:math:`g(\mathbf{x})` can be represented as a linear combination of
the eigenfunctions:

.. math::
   g(\mathbf{x}) = \sum_j c_j\phi_j

Therefore, if we know the value of :math:`g(\mathbf{x}_0)` at some
initial state, :math:`\mathbf{x}_0`, then we know the value at time
step :math:`k`:

.. math::
   \mathbf{x}_k = {\cal K}^k_g(\mathbf{x}) = \sum_j
   c_j\lambda_j^k\phi_j

The value of :math:`\lambda_j` will be complex generally.  But we can
always write: :math:`\lambda_j = r e^{i\theta}` and use the value of
:math:`r` to determine the stability of the flow.

For our discrete dynamical system, we can write this entire
development using standard linear algebra.  Assume that we have a
vector of basis functions evaluated over some phase-space state:
:math:`\mathbf{g}(\mathbf{x})`.  To be specific, let us assume that
our :math:`\mathbf{g}` has rank :math:`L` The evolution equation
becomes:

.. math::
   \mathbf{g}(\mathbf{x}_{j+1}) = \mathbf{A}\mathbf{g}(\mathbf{x}_{j})

For some left eigenvector :math:`\mathbf{y}^\intercal\mathbf{A} =
\lambda\mathbf{y}^\intercal` which implies that
:math:`\phi(\mathbf{x}) = \mathbf{y}^\intercal\mathbf{g}(\mathbf{x})`.
In other words, if we can estimate :math:`\mathbf{A}` from our data,
we get an estimate the Koopman eigenfunctions.  We will describe this
approximation technique next.


Extended Dynamical Mode Decomposition
-------------------------------------

Suppose we have :math:`m` snapshots from our simulation.  Extended
Dynamical Mode Decomposition (eDMD) approximates the matrix
:math:`\mathbf{A}` from snapshot pairs of the basis function
evaluations of our N-body system:
:math:`\{(\mathbf{g}(\mathbf{x}_{j}),\mathbf{g}(\mathbf{x}_{j+1}))\}`
with :math:`j=0,\ldots,m-1`.  For convenience denote :math:`c_{k,j} =
g_k(\mathbf{x}_j)`. Now arrange each snapshot into two data matrices,
:math:`\mathbf{G}` and :math:`\mathbf{G}^\prime`:

.. math::
   \mathbf{G} = \begin{bmatrix} 
   c_{0,0} & c_{0,1} & \dots \\
   \vdots & \ddots & \\
   c_{L,0} &        & c_{L,m-1} 
   \end{bmatrix}
   \qquad
   \mathbf{G}^\prime = \begin{bmatrix} 
   c_{1,1} & c_{1,2}\dots  & c_{1,m}\\
   \vdots & \ddots & \vdots\\
   c_{L,1} & \dots  & c_{L,m} 
   \end{bmatrix}

Our discretized evolution equation is then :math:`\mathbf{G}^\prime =
\mathbf{A}\mathbf{G}`.  For EXP-based analyses, the elements of
:math:`\mathbf{G}` are the basis coefficients, :math:`c_{i,j}`.  The
best fit matrix :math:`\mathbf{A}` establishes a linear dynamical
system that approximately advances snapshot measurements forward in
time, which may be formulated as linear least-squares problem:

.. math::
   \mathbf{A} = \mbox{argmin}_{\mathbf{A}} \lVert\mathbf{G}^\prime −
   \mathbf{A}\mathbf{G}\rVert_F

where :math:`\lVert\cdot\rVert_F` is the Frobenius norm.  The Singular
Value Decomposition (SVD) is can be used to construct the solution
using the pseudo-inverse which we denote by :math:`\dagger`.  This
gives us:

.. math::
   \mathbf{A} = \mathbf{G}^\prime\mathbf{G}^\dagger

The SVD of :math:`\mathbf{G} =
\mathbf{U}\mathbf{\Sigma}\mathbf{V}^\ast` may be written as
:math:`\mathbf{X}^\dagger =
\mathbf{V}\mathbf{\Sigma}^{-1}\mathbf{U}^\ast`. The matrices
:math:`\mathbf{U}\in\mathbb{C}^{L\times L}` and
:math:`\mathbf{V}\in\mathbb{C}^{m\times m}` are unitary, so that
:math:`\mathbf{U}^\ast\mathbf{U} = \mathbf{I}` and
:math:`\mathbf{V}^\ast\mathbf{V} = \mathbf{I}` where :math:`\ast`
denotes complex-conjugate transpose. The columns of :math:`\mathbf{U}`
are known as POD [#]_ modes in DMD terminology.

.. important:: This prescription implicitly assumes that our dynamical
   problem and therefore our Koopman operator :math:`{\cal K}` is time
   independent.  That is, using linear least squares to estimate
   :math:`\mathbf{A]` implies that the same operator works for
   :math:`\mathbf{g}(\mathbf{x}_{j+1}) =
   \mathbf{A}\mathbf{g}(\mathbf{x}_{j})` for any value of :math:`j`
   for the same matrix :math:`\mathbf{A}`.  This may not be true if
   your galaxy is evolving.  In this case, you may need to break up
   your time series into temporal windows whose length are smaller
   than the evolution time.

In our case, the number of samples :math:`m` will be much larger than
the number of basis functions :math:`L`.  And the effective rank
:math:`r` of :math:`\mathbf{A}` is often even lower.  Therefore, we
can further reduce the dimensionality by projecting :math:`\mathbf{A}`
onto the first :math:`r` POD modes.  This provides a rank-:math:`r`
approximation of :math:`\mathbf{A}` using the SVD:
:math:`\mathbf{A}\approx\mathbf{U}_r\mathbf{\Sigma}_r\mathbf{V}_r`
where the subscript :math:`r` indicates the rank reduced versions of
the original SVD.  The resulting approximation to :math:`\mathbf{A}`
becomes:

.. math::
   \tilde{\mathbf{A}} = \mathbf{U}_r^\ast\mathbf{A}\mathbf{U}_r
   = \mathbf{U}_r^\ast\mathbf{A}^\prime\mathbf{A}^\dagger\mathbf{U}_r
   =
   \mathbf{U}_r^\ast\mathbf{A}^\prime\mathbf{V}_r\mathbf{\Sigma}^{-1}_r

with eigenvalues and eigenfunctions:

.. math::
   \tilde{\mathbf{A}}\mathbf{\Xi} = \mathbf{\Lambda}\mathbf{\Xi}

where :math:`\mathbf{\Xi}` is the matrix of eigenvectors and and
:math:`\mathbf{\Lambda}` is the diagonal matrix of eigenvalues.  The
estimated eigenvectors of the evolution matrix :math:`\mathbf{A}` may
be reconstructed from the reduced problem as follows:

.. math::
   \mathbf{\Phi} = \mathbf{U}_r\tilde{\mathbf{A}}\mathbf{\Xi} =
   \mathbf{A}^\prime\mathbf{V}_r\mathbf{\Sigma}_r^{-1}\mathbf{\Xi}

We can use the eigenvalues :math:`\Lambda_j` to identify the frequency
of interesting growing or oscillating patterns and use the corresponding
eigenvectors :math:`\mathbf{\Phi}_j` to reconstruct the physical
fields in the mode, just as we do for mSSA.  

Discussion and relationship to mSSA
===================================

Koopman's paper [koopman31]_ posits and proves the existence of a time
evolution operator for a finite dimensional non-linear dynamical
system by 'lifting' or projection of the finite-dimensional phase
space to an infinite dimensional space.  That is one takes an
M-dimensional manifold (i.e. phase space) and finds a mapping to an
infinite dimensional space.  Specifically, he considered a projection
to Hilbert space.  In the infinite dimensional function space, the
dynamics can be shown to be locally linear and therefore completely
describable.  This implies that one may find the eigenvalues and
eigenfunctions that describe the dynamics.  Then, one can project them
back to the original space to fully describe the original non-linear
problem.

In practice, this can be done analytically but for only very simple
systems with a cleverly chosen set of functions.  But it does work,
when one can solve it.  There are several nice examples showing that
phase space can be tiled with eigenfunctions around critical points to
recover the full dynamics.  The often used example is the Lorenz
*strange* attractor.  The need to do this hard work analytically
clearly limits the utility of Koopman operator theory.  However, one
can follow one or more trajectories in the original system and attempt
to elicit a finite dimensional approximation to a Koopman operator by
combining many samples over time simultaneously.  Since one is
implicitly assuming that the system is time independent, one tries to
find the linear operator that simultaneously evolves all the
trajectories at every time step to each of their next time steps.

In the simplest formulation, this method only works for
time-independent systems as described in the previous section; the
eigenfunctions need to span the phase space lift for all time to solve
it by the linear least-squares method.  Although one can extend the
approach to time-dependent systems that are an explicit function of
time using an extended phase-space approach, this can not be obviously
extended to a general time evolving system (like an evolving galaxy).

The application of eDMD to our basis function representation of a
simulation results in the matrix equation:
:math:`\mathbf{g}(\mathbf{x})_{j+1} = \mathbf{g}(\mathbf{x})_j` where
:math:`\mathbf{A}` is the finite-dimensional approximation Koopman
operator and :math:`\mathbf{x}_j` is state at time step
:math:`\mathbf{j}`.  Using the language of mSSA, we can *pile up* many
samples sample pairs trajectory matrix.  The matrix that does this is
a lag-1 trajectory matrix in mSSA speak.  Then, one can use SVD to
find the best fit operator M that does this best in the linear
least-squares sense.  This defines dynamical mode decomposition (DMD).
The basis-set coefficients represent an *observable* function of our
complex dynamics from the phase-space snapshots. We can then ask the
same question as DMD: what is the linear operator that best advances
all of the *observable* functions by one time step for all observed
time steps together.  This is called extended DMD (eDMD).  The
'observable' functions for our case would be basis functions (e.g.).
This is the closest finite-dimensional analog to what Koopman
originally proposed in 1931.  BTW, they called these special functions
of phase space 'observable' functions since they were envisioning
quantum mechanical systems where one does not directly observe states.
But this works for our purposes as basis functions just fine.

SSA is closely related to to Koopman theory (and eDMD) although it has
additional properties.  In fact, in 1980, Takens [takens80]_ proved
that the time-delayed trajectory that we use in SSA can be 'lifted' to
a higher dimensional space that makes the trajectories in the
high-dimensional space locally Euclidean; that is, they no longer
cross and can be locally interpreted as linear flow.  Same as Koopman.
A few recent papers have shown that SSA is also a valid representation
of a Koopman operator.  However, the motivation in the previous
sections illustrate an important difference: Koopman attempts to find
the analogous linear problem in a large number of dimensions that
simplifies the low dimensional problem through a mapping while SSA
attempts to find the temporal solution for the entire time series.
Therefore, my intuition suggests that extra time embedding provides
the SSA eigenfunctions (PCs) with more temporal structure that eDMD.
The main problem with eDMD relative to mSSA is that eDMD requires that
the entire input series really describe a time dependent segment of
the evolution.  While mSSA uses temporal autocorrelation to find
temporal regimes that are correlated. In some sense, the windowing
nature is able to break up the time series into segments that
correlate the dynamics in 'regimes' that approximate a temporally
constant segment of the evolution.

I have demonstrated this to myself by applying eDMD and mSSA to
segments of my unstable l=1 simulations [weinberg22]_.  If I apply
each method to the exponentially growing phase of the evolution, both
give consistent results.  Specifically eDMD is able to identify the
growing mode pair with the correct frequency.  The down side is that
eDMD identifies a whole pile of modes that don't seem to have any
particular meaning.  This is a well known problem with eDMD: it finds
spurious modes.  Once can argue that mSSA has the same problem but
mSSA provides some built in significance (in terms of the eigenvalues
themselves) while eDMD does not.  In addition, I know that there is
also a damped mode that mSSA finds and eDMD does not.  Moreover, if I
give the entire time series (post saturation of the exponential
growth), eDMD gives a mode pair that makes no physical sense.

My conclusion here is that eDMD can be used for strictly
time-independent problems (or time-indepdendent segments of an
evolving problem).  It has the one interpretive advantage of providing
the frequency of a mode directly.  However, it seems to mix up things
very easily.  The propensity of eDMD to do this is well documented, so
this finding is not specific to this particular application. mSSA is
more robust to this sort of confusion, although we also know that mSSA
can mix modes, too.

We have implemented eDMD in pyEXP with an analogous interface to
expMSSA, so you can try it if wish.  Please provide feedback!

.. [koopman31] B.O. Koopman. Hamiltonian systems and transformation in
	       Hilbert space, Proceedings of the National Academy of
	       Sciences, 17, 315, 1931

.. [brunton21] S. L. Brunton, M. Budišić, E. Kaiser, J.N. Kutz.
	       Modern Koopman Theory for Dynamical
	       Systems. arxiv:2102.12086v2

.. [takens80] F. Takens. Detecting strange attractors in turbulence
	      Dynamical Systems and Turbulence, Warwick 1980 (Lecture
	      Notes in Math. vol 898) pp 366–81

.. [weinberg22] M.D. Weinberg. New dipole instabilities in spherical
		stellar systems. arXiv:2209.06846.

.. [#] Proper Orthogonal Decomposition

