Two-dimensional cylindrical bases
=================================

The latest version of EXP includes support for two-dimensional
cylindrical disk bases with three-dimensional potential theory.  This
allows full gravitational couples between two- and three-dimensional
components.

Implementation
--------------

We construct two-dimensional polar bases using the same empirical
orthogonal function (EOF) technique used to compute the three
dimensional cylindrical basis (see :ref:`empirical orthogonal
functions <EOF>`).  The user has the choice to two possible input
basis:

1. The cylindrical Bessel functions of the first kind,
   :math:`J_m(\alpha_{m,n}R/R_{max})` where :math:`\alpha_{m,n}` is the
   nth root of :math:`J_m` and :math:`R_{max}` is an outer boundary.
   Thus, orthogonality is defined over a finite domain by construction.

2. The Clutton-Brock two-dimensional basis ([cluttonbrock72]_) which
   orthogonal over the semi-infinite domain.  

The user then chooses a conditioning density.  Currently, these must
be one of: exponential disk, Kuzmin (Toomre) disk, or Mestel disk
([bt08]_).  The code was written to allow for a user-defined density
function and this will be implemented when needed in a future release.

The coupling between the two-dimensional disk and other
three-dimensional components (e.g. the dark-matter halo or a bulge)
requires evaluating the gravitational potential and its gradient
everywhere in space.  The three-dimensional gravitational potential is
not *automatically* provided by the two-dimensional recursion
relations that define the biorthogonal functions but must be evaluated
by Hankel transform.  This can be done very accurately over a finite
domain with the quasi-discrete Hankel transformation on a finite
domain (QDHT, [guizar04]_).  This algorithm exploits the special
properties of the Bessel functions.

The EOF basis solutions are tabled on a fine grid and interpolated as
needed.  This is numerically efficient and accurate. While the
in-plane density, potential and force fields are one-dimensional
functions for each azimuthal order :math:`m` and radial order
:math:`n`, the potential and force fields for :math:`|z|>0` require
two-dimensional tables.  Like the one-dimensional functions, these are
finely-grided an interpolated using bilinear interpolation.


Discussion
----------
The upside of the current strategy is:

1. One can condition the biorthgonal Bessel-function basis on any
   target density, similar to the three-dimensional case

2. The Hankel transform over the basis is very accurate so the whole
   thing is accurate.

The downsides are:

1. The Hankel transformation for an infinite domain is numerically
   challenging and we have had good success using QDHT, so we
   recommend the finite basis for this reason.  This restriction to a
   finite-domain is not a problem in practice; all of the numerical
   implementations are finite.

2. The Bessels are wiggly and if one looks closely they leave their
   wiggly imprint at larger radii.  Of course, we generally don't care
   about larger radii.

While the code allows the conditioning on the 2d Clutton-Brock basis,
the computation of the vertical potential is less accurate for the
same computational work using QDHT. This could be improved by
truncating the basis and implementing Neumann boundary conditions with
appropriate outgoing eigenfunctions.  That has not been done here.
Another solution might be an asymptotic numerical evaluation of the
Hankel transform at large cylindrical radii patched onto a brute force
quadrature at small radii.  At this point, we recommend the Bessel
basis for accuracy if you need to couple to another three-dimensional
component.  If you only need the two-dimensional in-plane evaluations
(e.g. a two-dimensional disk in a fixed halo), both basis choices will
be good.
