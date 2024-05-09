.. _bfetheory:

==========
BFE theory
==========

The BFE method has four primary advantages over tree- and grid-method
gravity solvers: (1) the computational effort in the force calculation
scales linearly with particle number; (2) the dynamic range of
multi-scale systems, such as the disk-halo system, can be better
resolved by tailoring the geometry and scale of the density and
potential variation to each of the components individually; (3)
sensitivity to weak global distortions is possible because small-scale
noise can be removed; and (4) intercomponent interactions can be
explicitly selected and controlled to allow the study of different
mechanisms individually.  In particular, EXP is designed to allow the
self-gravity and intercomponent forces between all components to be
independently selected and controlled by simple configuration
parameters (see :ref:`yamlconfig`).

In the remainder of this chapter, I will give a brief introduction to
the mathematics of the BFE method which then motivates the overall
software design. This should provide enough review of the background
to begin using the code (:ref:`EXP tutorial <intro-EXP-tutorial>` and
:ref:`pyEXP tutorial <intro-pyEXP-tutorial>`).  Additional technical
details will be summarized in later chapters.

.. _bfedefs:

The basic BFE algorithm
=======================

The harmonic basis-function expansion (BFE) technique has been used to
both study and compare simulations to theoretical predictions, owing
to its natural relationship with analytic perturbation theory
([weinberg07a]_, [weinberg07b]_). To use the BFE approach for $n$-body
simulations, one uses the :index:`biorthogonal` nature of the
appropriately chosen basis functions to solve the :index:`Poisson
equation` using separable azimuthal harmonics at the same time as the
expansion.  A biorthogonal system is a pair of indexed families of
vectors in some topological vector space such that the inner product
of the pair is the Kronecker delta.  The BFE method constructs a
biorthongal system :math:`d_j(\mathbf{x}), p_k(\mathbf{c})` such that
:math:`\nabla^2 p_i = 4\pi G d_i` and :math:`\int d\mathbf{x}\,
d_j(\mathbf{x}) p_k(\mathbf{x}) = 4\pi G\delta_{jk}.` Let the density
of our particle distribution of :math`N` points with masses
:math:`m_i` described by

.. math::
   \tilde{\rho}(\mathbf{x}) = \sum_{i=1}^N m_i \delta\left(\mathbf{x} - \mathbf{x_i}\right).

Then, approximations for the density and potential fields are

.. math::
   \text{density:}\qquad
   \hat{\rho}(\mathbf{x}) &= \sum_{j=1}^n a_i d_j(\mathbf{x}), \\
   \text{potential:}\qquad
   \hat{\Phi}(\mathbf{x}) &= \sum_{j=1}^n a_i p_j(\mathbf{x}),

where

.. math::
   a_j = \int d\mathbf{x}\, \tilde{\rho}(\mathbf{x}) p_j(\mathbf{x}) =
   \sum_{i=1}^N m_i p_j(\mathbf{x_i}).


.. index:: expansion algorithm

Generally, any technique making use of these properties may be called
BFE ([cluttonbrock72]_, [cluttonbrock73]_, [kalnajs76]_,
[hernquist92]_, [earn96]_, [weinberg99]_).  BFE has many notable
features that make them ideal for studying disturbances to equilibrium
stellar discs. For simulations using BFE methods, harmonic function
analysis decomposes a distribution into linearly-summable functions
that resemble expected evolutionary scenarios in disc galaxy
evolution. The primary diagnostics available are the amplitude and
phase of each function. In addition, the time-dependence of the
coefficients themselves provides another dimension for studying
evolution that may not clearly manifest itself in analytic studies
(see :ref:`mSSA <mssa>` and [weinberg21]_). Using harmonic
function analysis in BFE simulations, no matter what Poisson solver is
reconstruction of the potential at any time in the simulation, for any
arbitrary combinations of particles.


Empirical Orthogonal Functions
==============================

.. _EOF:

.. _disk_amplitudes:
.. figure:: images/basis1.png
    :figwidth: 80 %
    :width: 80 %
    :align: center

    In-plane amplitude variations as a function of disk scale length
    for all radial functions per harmonic order in the cylindrical
    disk basis. We show the :math:`m=0,1,2,4` harmonic subspaces as
    panels from top to bottom. The amplitude in each panel has been
    normalized to the maximum in the corresponding subspace. Functions
    that are zero everywhere are vertically asymmetric.

.. _disk_3d_amplitudes:
.. figure:: images/basis2.png
    :figwidth: 80 %
    :width: 80 %
    :align: center

    Examples of vertically symmetric (:math:`m=2,n=4`, upper
    panel), and vertically asymmetric (:math:`m=2,n=11`, lower
    panel) functions for the disk basis. The :math:`x` and :math:`z`
    axis correspond to the radial and vertical axes in the simulation,
    and the amplitude of the variations between panels has been
    normalized to the maximum :math:`m=2` amplitude.

A BFE computes the gravitational potential by projecting particles
onto a set of biorthogonal basis functions that satisfy the Poisson
equation as described in [petersen2022]_. Then, the force at the
position of each particle is evaluated from the basis-function
approximation to the field at the particle position.  Fundamentally,
this approach relies on the mathematical properties of the
Sturm-Louiville equation (SLE) of which the Poisson equation is a
special case. The SLE describes many physical systems, and may be
written as:

.. math::
   :label: sle

   \frac{d}{dx}\left[p(x)\frac{d\Phi(x)}{dx}\right] - q(x)\Phi(x) =
   \lambda \omega(x) \Phi(x)

where :math:`\lambda` is a constant, and :math:`\omega(x)` is a
weighting function. The eigenfunctions :math:`\phi_j` of the SLE form
a complete basis set with eigenfunctions :math:`\lambda_j`, where
:math:`j` may be truncated from the theoretically infinite
series. When applied to the Poisson equation specifically, the
equation separates in conic coordinate systems.  For Cartesian, the
widely-used Fourier expansion is a well-known examples. The BFE
potential solver is built using properties of eigenfunctions and
eigenvalues of the SLE.

For an expansion in spherical harmonics, the SLE/Poisson equation
separates into angular and radial equations, giving rise to spherical
harmonics and Bessel functions naturally.  The boundary conditions are
easy to apply in radius (at the origin and at infinity).  For example,
a dark-matter halo can be expanded into a relatively small number of
spherical harmonics :math:`Y_{lm}` and appropriate radial functions.
Each term in halo potential is given by :math:`\Phi_{lm}^j =
\phi_{lm}^j(r)Y_{lm}(\theta,\phi)`.  Even more interesting, Bessel
functions are not the only choice.  By changing the weighting function
we may derive an infinity of radial bases.  In particular, the
weighting function :math:`\omega` in equation :eq:`sle` may be
selected to be an equilibrium solution of the Poisson equation.  In
other words, the unperturbed potential would be represented by a
single term! In EXP, we solve the SLE to get the new
biorthogonal basis using the SLEDGE solver [pruess_fulton93]_.

The disk is more complicated.  Although one can construct a disk basis
from the eigenfunctions of the Laplacian as in the spherical case
\citep[e.g.][]{earn96}, the boundary conditions in cylindrical
coordinates make the basis hard to implement. To get around this, our
solution method starts with a spherical basis with :math:`l\le36` and
uses a singular value decomposition (SVD) to define a rotation in
function space to best represent a target disk density.  Specifically,
each density element :math:`\rho(R, z)\,d^3x` contributes

.. math::
   :label: contrib

        \frac{1}{4\pi G}\phi_{lm}^j(r)Y_{lm}(\theta,\phi)\rho(R, z)d^3 x

to the expansion coefficient :math:`a_{lm}^j`, or

.. math::
   :label: coeff

         a_{lm}^j &= \frac{1}{4\pi
        G}\int \phi_{lm}^j(r)Y_{lm}(\theta,\phi)\rho(R, z)d^3x \\
                  &= \lim_{N\rightarrow\infty}\frac{1}{4\pi
        G}\sum_{i=1}^N m_i \phi_{lm}^j(r_i)Y_{lm}(\theta_i,\phi_i)

where :math:`R, z` are the radial and vertical cylindrical
coordinates.  The second equation shows the approximation for
:math:`N` particles where :math:`\sum_i m_i = \int \rho(R, z)d^3x`.


The covariance of the coefficient given the density :math:`\rho(R,
z)`, :math:`\mbox{cov}(\mathbf{a})`, is constructed similarly.  The
covariance matrix describes which terms :math:`a_{lm}^j` contribute
the most variance.  By diagonalizing :math:`\mbox{cov}(\mathbf{a})`,
we may find a new basis, uncorrelated by the target density .  Because
:math:`\mbox{cov}(\mathbf{a})` is symmetric and positive definite, all
eigenvalues will be positive.  The term with the largest eigenvalue
describes the majority of the correlated contribution, and so on for
the second largest eigenvalue, etc.  EXP performs this diagonalization
using the singular value decomposition (SVD) and the singular matrices
(now mutual transposes owing to symmetry) describe an rotation of the
original basis into the uncorrelated basis.

The new basis functions optimally approximate the true distribution
from the spherical-harmonic expansion in the original basis in the
sense that the lagest amount of variance is contained in the smallest
number of terms; we might call this optimal in the *least-squares
sense*. Since the transformation and the Poisson equation are linear,
the new eigenfunctions are also biorthogonal.  The new coefficient
vector is related to the original coefficient vector by an orthogonal
transformation.  Because we are free to break up the spherical basis
into meriodinal subspaces by azimuthal order, the resulting
two-dimensional eigenfunctions in :math:`r` and :math:`\theta` are
equivalent to a decomposition in cylindrical coordinates :math:`r,~z,`
and :math:`\theta`.  We condition the initial disk basis functions on
an analytic disk density such that the lowest-order potential-density
pair matches the initial analytic mass distribution. This choice also
acts to reduce small-scale discreteness noise as compared to
conditioning the basis function on the realized positions of the
particles \citep{weinberg98}. Although there could be some other
biases introduced by this procedure, our experience to date suggests
that this approach provides a fair representation of the disk density
and potential fields.

We can represent the potential and density of a galaxy as a
superposition of several basis functions. This allows us to decompose
the galaxy based on their geometry and symmetry. For an initially
axisymmetric example, azimuthal harmonics :math:`m`, where :math:`m=0`
is the monopole, :math:`m=1` is the dipole, :math:`m=2` is the
quadrupole, and so on, will efficiently summarize the degree and
nature of the asymmetries. The sine and cosine terms of each azimuthal
order give the phase angle of the harmonic that can be used to
calculate the pattern speed.  For disks, each azimuthal harmonics
represents both the radial and vertical structure simultaneously; that
is each basis function is a two-dimensional meridional plane multipled
by :math:`e^{im\phi}`.  The symmetry of the input basis and the
covariance matrix further demands that the singular value
decomposition produce vertically symmetric or anti-symmetric
functions.  See :ref:`Visualizing bases
<visualizing-cylindrical-basis>` for examples of both types of
functions and hints on how to explore them using pyEXP.

After some exploration, we determined that a radial scale factor for
the spherical profile of approximately :math:`\sqrt{2}` time larger than
spherical deprojected profile of the disk represented the disk profile
is the smallest number of terms.  This choice of radial scale is not
very sensitive to the resulting basis, however.

Examples
--------

:numref:`disk_amplitudes` shows the in-plane amplitude
variations for radial functions (:math:`n` orders) as a function of
radius, separated by harmonic subspace (:math:`m` orders) for an
exponential disk in an NFW ([navarro97]_) halo.  We show the four
harmonic subspaces that are most relevant for the evolution of the
simulation, :math:`m=0,1,2,4`, from top to bottom in the panels. In
each harmonic subspace, the lowest-order radial order, :math:`n=1`,
has no nodes except at :math:`R=0` for :math:`m\ge0`. The number of
nodes increases with order :math:`n`. The nodes are interleaved by
radial order, but the increasing number of nodes means that the
smallest radius node always decreases in radius as the number of nodes
increases. Therefore, an increase in amplitude for
higher--:math:`n`--order harmonics corresponds to the movement of mass
to smaller radii. Additionally, the spacing of nodes gives an
approximate value for the force resolution of the simulation. For
example, the highest order :math:`m=0` radial function (:math:`n=12`)
has a zero at :math:`R=0.2a`, or 600 pc in a MW-like
galaxy. Additionally, the radial orders are interleaved between
harmonic orders, such that the location of the first node,
:math:`R^{[1st]}`, is given by

.. math::
   R_{m=2,n=1}^{[1st]} \approx \frac{1}{2}\left(R_{m=1,n=1}^{[1st]} +
   R_{m=1,n=2}^{[1st]}\right).

The lowest-order basis function exactly matches the initial density
profile and has no nodes.  In this example, the highest-order basis
function, :math:`n=12`, would only imply a spatial resolution of 100
pc, the basis resolves a power law in density down to 10 pc. This
choice removes or filters high spatial frequencies that may increase
relaxation noise.  :numref:`disk_3d_amplitudes` illustrates the
vertical structure in the disk basis functions. The upper panel shows
the :math:`m=2,n=4` basis function in radius--z space. This function
is symmetric about the :math:`z=0` axis. The combination of vertically
symmetric and asymmetric harmonics represent all possible variations
in the gravitational field above and below the plane consistent with
the spatial scales in the basis. In both panels, the color has been
normalized to the maximum amplitude of the :math:`m=2` harmonic
subspace.

.. _twodcyl:
.. include:: two_d_disk.rst

.. _slabSL:
.. include:: slab.rst

.. _cube:
.. include:: cube.rst

Final comments and caveats
==========================

The basic expansion algorithm is described at the beginning of this
chapter. EXP can be configured to log coefficients each step or in any
multiple of steps (see :ref:`design` and :ref:`yamlconfig`).  The
coefficients for each :math:`n` order are generally complex.  The real
and imaginary parts correspond to the cosine and sine components of
the analogous Fourier terms :math:`A_m` and :math:`B_m`. The
coefficients are written in sine and cosine form for easy
interpretation.  Thus, the user may compute the phase angle for any
basis function and use the total amplitude or modulus as an indicator
of power.  Additional details about using multiple time-step levels
along with the leap-frog algorithm can be found in Section
:ref:`multistep`.

The BFE approach trades off precision and degrees-of-freedom with
adaptability. The truncated series of basis functions intentionally
limits the possible degrees of freedom in the gravitational field in
order to provide a low-noise bandwidth-limited representation of the
gravitational field. One must investigate whether the basis can
capture all possible mechanisms of disk evolution.  For example, this
method will work very well for near equilibrium systems but could give
biases results for grossly asymmetric systems.  A simple example of
this is centering (see Sec. :ref:`centering`).   Please be vigilant.

On the up side, a basis function representation provides an
information--rich summary of the gravitational field and provides
insight into the overall evolution.  This method allows for the
decomposition of different components into dynamically-relevant
subcomponents for which the gravitational field can be calculated
separately.

.. [bt08] J. Binney and S. Tremaine. Galactic Dynamics: Second
	  Edition. Princeton University Press, Princeton, NJ USA, 2008.


.. [cluttonbrock72] M. Clutton-Brock. The Gravitational Field of Flat
		    Galaxies. APSS, 16:101–119, Apr. 1972.

.. [cluttonbrock73] M. Clutton-Brock. The Gravitational Field of Three
		    Dimensional Galaxies. APSS, 23:55–69, July 1973.

.. [earn96] D. J. D. Earn. Potential-Density Basis Sets for Galactic
	     Disks. ApJ, 465:91, July 1996.

.. [guizar04] M. Guizar-Sicairos and J. C. Gutiérrez-Vega.
	      Computation of quasi-discrete Hankel transforms of
	      integer order for propagating optical wave
	      fields. J. Opt. Soc. Am. A 21(1):53-58, 2004.

.. [hernquist92] L. Hernquist and J. P. Ostriker. A self-consistent
		 field method for galactic dynamics. ApJ, 386:375–397,
		 Feb. 1992.

.. [kalnajs76] A. J. Kalnajs. Dynamics of Flat
	       Galaxies. II. Biorthonormal Surface Density-Potential
	       Pairs for Finite Disks. ApJ, 205:745–750, May 1976.

.. [navarro97] J. F. Navarro, C. S. Frenk, and S. D. M. White. A
	       Universal Density Profile from Hierarchical
	       Clustering. ApJ, 490:493–508, Dec. 1997.

.. [pruess_fulton93] S. Pruess and C. T. Fulton. Mathematical Software
		     for Sturm-Liouville Problems. ACM Transactions on
		     Mathematical Software, 19:360–376, Sept. 1993.

.. [weinberg99] M. D. Weinberg. AJ, 117:629, 1999.

.. [weinberg07a] M. D. Weinberg and N. Katz. The bar-halo
		 interaction - I. From funda- mental dynamics to
		 revised N-body requirements. MNRAS, 375:425–459,
		 Feb. 2007

.. [weinberg07b] M. D. Weinberg and N. Katz. The bar-halo
		 interaction - II. Secular evolution and the religion
		 of N-body simulations. MNRAS, 375:460–476, Feb. 2007.

.. [weinberg21] M. D. Weinberg and M. S. Petersen. Using multichannel
		singular spectrum analysis to study galaxy
		dynamics. MNRAS, 501:5408-5423, Mar. 2021

.. [petersen2022] M. S. Petersen, M. D. Weinberg, and N. Katz.
		  EXP: N-body integration using basis function
		  expansions. MNRAS, 510:6201-6217, Mar. 2022
		  
