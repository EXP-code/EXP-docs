Three-dimensional periodic slab bases
=====================================

The latest version of EXP includes support for slab basis that is
periodic in the unit square with equilibrium self-gravity in the
vertical dimension. The coordinate system is Cartesian and Poisson
equation separates in Cartesian coordinates.  Since the equilibrium in
the horizontal directions is uniform, the natural basis is
trigonometric, e.g. :math:`e^{i2\pi (k_x x + k_y y)}` where
:math:`k_x, k_y\in\mathbb{Z}`.  The resulting unknown basis functions
satisfy

.. math::
   \frac{d^2\Psi(z)}{d^2z} - (k_x^2+k_y^2) \Psi(z) = 4\pi G
   \rho(z).
   
We assume an equilibrium solution :math:`d^2\Psi_o(z)/dz^2 = 4\pi
G\rho_o(z)` and write :math:`\Psi(z) = \Psi_o(z)u(z)`.  Substituting
this into the Poisson equation above and multiplying by
:math:`\Psi_o(z)`, we obtain a Sturm-Liouville differential equation,
eq. :eq:`sle`, with eigenfunctions :math:`u(z)` and eigenvalues
:math:`\lambda` with

.. math::

   p(z) &= \Psi_o(z)^2 \\\\
   q(z) &= [(k_x^2+k_y^2)\Psi_o(z) - \rho_o(z)]\Psi_o(z) \\\\
   \omega(z) &= \rho_o(z)\Psi_o(z)


Implementation
--------------

The SLE is straightforwardly solved using the shooting algorithm in
SLEDGE [pruess_fulton93]_. The boundary conditions for the spherical
solution are the natural ones for typical gravitational system at
large radii.  However, the potential and mass of our
periodically-infinite slab is unbounded, rising linearly to infinity
as :math:`|z|\rightarrow\infty`. Furthermore, our construction of the
weighed SLE from the Poisson equation requires a non-zero weighing
function :math:`\omega(z)`.  We accomplish this by

1. Choosing a maximum vertical extent :math:`z_{max}`
   
2. Evaluating the potential at some point outside this range,
   e.g. :math:`K\equiv\Psi_o(z_{max}[1+\delta])`
	 
3. Subtracting this value from the potential: :math:`\bar{\Psi}(z) =
   \Psi_o(z) - K`

Adding a constant to the potential will not change the physical
properties of the solution.  A basis with different values of
:math:`K` will differ in scale but remain biorthogonal and valid
solutions of the Poisson equation.  The value of :math:`\delta>0` is
unimportant as long as :math:`\bar{\Psi}(z)\not=0` in :math:`|z|\le
z_{max}`.  Finally, the SLE basis solutions are tabled on a fine grid
and interpolated as needed.  The horizontal, trigonometric part of
basis is constructed by recursion as needed.

Usage notes
-----------
The user accessible parameters that may be specified in the YAML
configuration (see the :ref:`YAML config example <yamlconfig>`) include:

- `nmaxx`: the maximum number order in the x direction. These basis
  functions are periodic in x and have wave number
  :math:`n_x=-n_{x\,max}` through :math:`n_x=n_{x\,max}`.
- `nmaxy`: the maximum number order in the y direction.
- `nmaxz`: the maximum number order in the z direction.  These are
  basis functions will be index from 0 to `nmaxz-1`.
- `nminx`: restrict the minimum wave number for x dimension  to :math:`n_x\geq
  n_{x\,nmin}`
- `nminy`: restrict the minimum wave number for y dimension
- `hslab`: scale height for slab basis
- `zmax`: maximum height for slab basis
- `ngrid`: number of grid points for basis table (default is 1000)
- `type`: the base model for the slab.  Choices are
  :math:`\rho(z)\propto\mbox{sech}^2(z/h), 1-(z/h)^2, \mbox{constant}` which
  are denoted as *isothermal*, *parabolic*, and *constant*,
  respectively.  The default is *isothermal* or (*iso* for short).

