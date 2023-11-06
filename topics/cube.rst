Three-dimensional rectangular bases
===================================

.. index:: periodic cube

The latest version of EXP includes support for a three-dimensional
rectangular prism using the classic trigonometric basis with periodic
or reflective boundary conditions.  This basis is ideal for
investigating various aspects of gravitational kinetics or secular
theory.  There is no loss of generality in assuming that the prism is
the unit cube and we will do that here.  A rectangle prism is with
arbitrary lengths in each dimension an always be scaled to the unit
cube.

The basis
---------

Most will be familiar with the standard separation of the Poisson
equation in Cartesian coordinates.  Assume that the potential is

.. math::
   \Phi_{\mathbf{k}} = C_{\mathbf{k}} e^{i\mathbf{k} \cdot \mathbf{x}}

where :math:`\mathbf{k}=2\pi\mathbf{n}` where :math:`\mathbf{n}` is
a triple of natural integers and :math:`C_{\mathbf{k}}` is a
normalization constant to be determined. Then:

.. math::
   \nabla^2 \Phi_{\mathbf{k}} = -k_n ^2\Phi_{\mathbf{k}} = 4\pi
   G\rho_{\mathbf{k}}.

This Sturm-Liouville equation has complete and orthogonal
eigenfunctions--the trigonometric functions periodic in the unit
cube--that we are using as our basis.  The orthogonality condition
demands that:

.. math::
   (\rho_{\mathbf{n}^\prime}, \Phi_{\mathbf{n}}) = -\frac{k_n^2
   C_n^2}{4\pi G} \delta_{\mathbf{n}^\prime \mathbf{n}}.

Assuming :math:`G=1` implies that :math:`C_n = 1/\sqrt{2n^2}`.

We can think of this periodic cube as tiling all of space as a special
case of the infinite homogeneous system.  Therefore, the equilibrium
has a constant density and constant potential.  The constant (or _DC_)
term :math:`\Phi_{0,0,0}` exerts no force and does not consistently
satisfy the Poisson equation (see [bt08]_ for more discussion of the
so-called **Jeans swindle**).


Implementation
--------------

As described in :ref:`bfedefs`, a particle ensemble immediately yields
a set of coefficients: :math:`a_{\mathbf{n}}`.  They take complex
values but any physical quantity is real by construction.
Numerically, the coefficients are accumulated by constructing the
basis functions by recursion.  For example, since

.. math::
   e^{i2\pi(j+1) x} = e^{i2\pi j x} e^{i2\pi x},

we only need the expensive evaluation of :math:`e^{i2\pi x}`,
:math:`e^{i2\pi y}`, :math:`e^{i2\pi z}` for each particle position
:math:`(x, y, z)` and all the basis functions follow by successive
multiplication.

Boundary conditions
-------------------

.. index:: pair: boundary conditions; cube

Your particles *only* contribute to the density if they are inside the
unit cube.  Specifically, the `Cube` routine *does not* wrap the
positions periodically into the unit cube.  If you would like
phase-space positions to be wrapped into the unit cube, use the
`PeriodicBC` external routine with origin at zero, lengths of one, and
periodic boundary conditions (these are the defaults).  The
`PeriodicBC` allows periodic ('p'), reflecting ('r'), and vacuum ('v')
boundary conditions.  The boundary-condition-type parameter are passed
as a string to the `Cube` routine with desired boundary conditions for
'xyz'.  For example, periodic boundary conditions in each dimension is
'rrr'.  Boundary condition type may be different in each
axis.
