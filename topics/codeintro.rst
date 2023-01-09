.. code-intro:

==========
Code intro
==========

This code uses :index:`object-oriented` (o-o) design patterns to
exploit the similarity in overall structure of all biorthogonal
expansions for ease of development and maintenance.  The o-o class
hierarchy enables reuse and reconfiguration for any number of
phase-space components whose gravity may be represented by a
appropriate biorthgonal bases and direct gravity methods.  The
object-oriented design enforces minimal consistency while retaining
flexibility.

Although the core code is intended to be maintained by developers,
users may write, compile and contribute new phase space operators for
applying perturbations, new force methods, etc. without changing or
recompiling the base code.  This is accomplished using dynamically
loadable libraries (see :ref:`user modules <usermodules>` for
details and a simple example).

The harmonic basis-function expansion (BFE) technique has been used to
both study and compare simulations to theoretical predictions, owing
to its natural relationship with analytic perturbation theory
([weinberg07a]_, [weinberg07b]_}. To use the BFE approach for $n$-body
simulations, one uses the :index:`biorthogonal` nature of the
appropriately chosen basis functions to solve the :index:`Poisson
equation` using separable azimuthal harmonics at the same time as the
expansion.  A biorthogonal system is a pair of indexed families of
vectors in some topological vector space such that the inner product
of the pair is the Kronecker delta.  The BFE method constructs a
biorthongal system :math:`d_j(\mathbf{x}), p_k(\mathbf{c})\) such that
\(\nabla^2 p_i = 4\pi G d_i\) and \(\int d\mathbf{x}\, d_j(\mathbf{x})
p_k(\mathbf{x}) = 4\pi G\delta_{jk}.` Let the density of our particle
distribution of :math`N` points with masses :math:`m_i` described by

.. math::

   \tilde{\rho}(\mathbf{x}) = \sum_{i=1}^N m_i \delta\left(\mathbf{x} - \mathbf{x_i}\right).

Then, approximations for the density and potential fields are

.. math::

  \text{density:} &&
  \hat{\rho}(\mathbf{x}) &= \sum_{j=1}^n a_i d_j(\mathbf{x}), & \\
  \text{potential:}&&
  \hat{\Phi}(\mathbf{x}) &= \sum_{j=1}^n a_i p_j(\mathbf{x}), & \\

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

In the remainder of this chapter, I will give a brief introduction to
the mathematics of the BFE method which then motivates the overall
software design. This should provide enough review of the background
to begin using the code (:ref:`EXP tutorial <intro-EXP-tutorial>` and
:ref:`pyEXP tutorial <intro-pyEXP-tutorial>`).  Additional technical
details will be summarized in later chapters.

.. [weinberg07a] M. D. Weinberg and N. Katz. The bar-halo
		 interaction - I. From funda- mental dynamics to
		 revised N-body requirements. MNRAS, 375:425–459,
		 Feb. 2007

.. [weinberg07b] M. D. Weinberg and N. Katz. The bar-halo
		 interaction - II. Secular evolution and the religion
		 of N-body simulations. MNRAS, 375:460–476, Feb. 2007.

.. [cluttonbrock72] M. Clutton-Brock. The Gravitational Field of Flat
		    Galaxies. APSS, 16:101–119, Apr. 1972.

.. [cluttonbrock73] M. Clutton-Brock. The Gravitational Field of Three
		    Dimensional Galaxies. APSS, 23:55–69, July 1973.

.. [earn96] D. J. D. Earn. Potential-Density Basis Sets for Galactic
	     Disks. ApJ, 465:91, July 1996.

.. [hernquist92] L. Hernquist and J. P. Ostriker. A self-consistent
		 field method for galactic dynamics. ApJ, 386:375–397,
		 Feb. 1992.

.. [kalnajs76] A. J. Kalnajs. Dynamics of Flat
	       Galaxies. II. Biorthonormal Surface Density-Potential
	       Pairs for Finite Disks. ApJ, 205:745–750, May 1976.

.. [weinberg99] M. D. Weinberg. AJ, 117:629, 1999.

.. [weinberg21] M. D. Weinberg and M. S. Petersen. Using multichannel
		singular spectrum analysis to study galaxy
		dynamics. MNRAS, 501:5408-5423, Mar. 2021

