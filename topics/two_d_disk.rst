Two-dimensional cylindrical bases
=================================

The latest version of EXP includes support for two-dimensional
cylindrical disk bases with three-dimensional potential theory.  This
allows full gravitational couples between two- and three-dimensional
components.

Implementation
--------------


Discussion
----------
The upside of the current strategy is:

1. One can condition the biorthgonal Bessel-function basis on any
   target density, similar to the three-dimensional case

2. The Hankel transform over the basis is very accurate so the whole
   thing is accurate.

The downsides are:

1. The Hankel transformation for an infinite domain is numerically
   challenging.  However, it can be done very accurate with the
   quasi-discrete Hankel transformation on a finite domain (QDHT,
   [guizar04]_).  This algorithm exploits the special properties of
   the Bessel functions.  However, this restricts the application to
   finite-domain basis.  In practice, this is not a problem.

2. The Bessels are wiggly and if one looks closely they leave their
   wiggly imprint at larger radii.  Of course, we generally don't care
   about larger radii.

But the reason that I can't condition on 2d Clutton-Brock (say) is
that computation of the vertical potential is much harder.  It can be
written just fine as a Hankel transform but the computation of the
transform is more numerically challenging.
