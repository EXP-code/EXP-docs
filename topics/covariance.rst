.. role:: python(code)
       :language: python
       :class: highlight

.. _covariance:

Coefficient covariance and signal-to-noise estimates
====================================================

.. attention::

   The `exp` interface described below is under development in the
   `OutSample` branch.  You will need to ``git checkout OutSample``
   and recompile to use these features in the `exp` N-body code. The
   `pyEXP` interface is currently available in the `main` branch.
   

Overview
--------

`exp` and `pyEXP` compute both the empirical covariance matrices and
compute coefficients in *partitions* or *batches* that may be used to
estimate statistical consistency of coefficients.

.. _covariance_theory:

Theory
------

Setup and notation
^^^^^^^^^^^^^^^^^^

Let :math:`\{c_i\}_{i=1}^N\subset\mathbb{R}^d` be the contribution to
the coefficient vector from Particle :math:`i`.  Specifically, if the
potential basis function is :math:`\Phi_k(\cdot)`, then
:math:`c_i=\{\Phi_1(\mathbf{x}_i), \Phi_1(\mathbf{x}_i), \ldots,
\Phi_d(\mathbf{x}_i)\}` where :math:`\mathbf{x}_i` is the position
vector for Particle :math:`i`.  Denote the empirical mean for the
entire ensemble of :math:`N` particles as

.. math::

   \bar{c} \;=\; \frac{1}{N}\sum_{i=1}^N c_i

and the sample covariance as

.. math::

   \Sigma \;=\; \frac{1}{N}\sum_{i=1}^N (c_i-\bar{c})(c_i-\bar{c})^{\!\top}.

Partition the particles into :math:`K` disjoint subsamples or _blocks_
with sizes :math:`n_k` so that :math:`\sum_{k=1}^K n_k = N`. For block
:math:`k` define

.. math:

   \bar{c}_k \;=\; \frac{1}{n_k}\sum_{i\in\text{block }k} c_i,
   \qquad S_k \;=\; \sum_{i\in\text{block }k}
   (c_i-\bar{c}_k)(c_i-\bar{c}_k)^{\!\top},

where :math:`S_k` is the within‑block scatter.

Overall mean and within and between blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The overall mean is the weighted average of block means:

.. math::

   \bar{c} \;=\; \frac{1}{N}\sum_{k=1}^K n_k \bar{c}_k.

The total scatter is

.. math::

   T \;=\; \sum_{i=1}^N (x_i-\bar{c})(x_i-\bar{c})^{\!\top},

and the exact decomposition is

.. math::

   T \;=\; \underbrace{\sum_{k=1}^K S_k}_{W} \;+\;
   \underbrace{\sum_{k=1}^K
   n_k(\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top}}_{B}.

The two terms are the *in block* and *between block* scatter.  Hence
the population covariance is

.. math::

   \Sigma \;=\; \frac{1}{N}T \;=\; \frac{1}{N}\sum_{k=1}^K S_k \;+\;
   \sum_{k=1}^K
   \frac{n_k}{N}(\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top} \;=\;
   \frac{W}{N} + \frac{B}{N}.

The between term :math:`B/N` can be computed from the
:math:`\{\bar{c}_k\}` and :math:`\{n_k\}` alone; the within aggregate
:math:`W` requires the :math:`S_k` or additional assumptions.

Special case: equal-size blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assume each block has the same size :math:`m`, so :math:`n_k = m` for
all :math:`k`, and :math:`N = Km`.  Define the block‑means covariance
as

.. math::

   S_{\bar{c}}^{\mathrm{pop}} \;=\; \frac{1}{K}\sum_{k=1}^K
   (\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top}.

Then the *between scatter* contribution is

.. math::

   B \;=\; \sum_{k=1}^K m(\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top}
    \;=\; m \sum_{k=1}^K (\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top},

and therefore

.. math::

   \frac{B}{N} \;=\; \frac{m}{Km}\sum_{k=1}^K
   (\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top} \;=\;
   \frac{1}{K}\sum_{k=1}^K
   (\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top} \;=\;
   S_{\bar{c}}^{\mathrm{pop}}.

Thus, deterministically,

.. math::

   \Sigma \;=\; \frac{W}{N} + S_{\bar{c}}^{\mathrm{pop}},
   \qquad\text{where } W=\sum_{k=1}^K S_k.

IID block-sampling model
^^^^^^^^^^^^^^^^^^^^^^^^

If additionally each block is formed by :math:`m` independent draws
from the same distribution with mean :math:`\bar{c}` and covariance
:math:`\Sigma` (block independent), then

.. math::

   \mathbb{E}[\bar{c}_k] = \bar{c},\qquad
   \operatorname{Cov}(\bar{c}_k) = \frac{\Sigma}{m}.

This is generally true for `exp` simulations and can be made true for
any simulation by selecting particles from the entire particle
ensemble randomly.  Consequently,

.. math::

   \mathbb{E}\!\big[ S_{\bar{c}}^{\mathrm{pop}} \big] \;=\;
   \frac{\Sigma}{m}.

Therefore an estimator of :math:`\Sigma` based on the
block means is

.. math::

   \widehat{\Sigma}_{\bar{c}} \;=\; m\,S_{\bar{c}},

where :math:`S_{\bar{c}}` is a chosen empirical covariance of the block
means. Two common choices:

-   Population-style (divide by :math:`K`):

    .. math::

       S_{\bar{c}}^{(K)} \;=\; \frac{1}{K}\sum_{k=1}^K
       (\bar{c}_k-\bar{c})(\bar{c}_k-\bar{c})^{\!\top},

    for which :math:`\mathbb{E}[S_{\bar{c}}^{(K)}]=\Sigma/m` when the true
    mean :math:`\bar{c}` is used (i.e., if :math:`\bar{c}` is known). Then
    :math:`\widehat{\Sigma}=m S_{\bar{c}}^{(K)}` is unbiased (when
    :math:`\bar{c}` is the true mean).

-   Sample-style (divide by :math:`K-1` using the sample mean
    :math:`\bar{\bar{c}}=(1/K)\sum_k \bar{c}_k`):

    .. math::

       S_{\bar{c}}^{(K-1)} \;=\; \frac{1}{K-1}\sum_{k=1}^K
       (\bar{c}_k-\bar{\bar{c}})(\bar{c}_k-\bar{\bar{c}})^{\!\top}.
    
    This satisfies

    .. math::

       \mathbb{E}\!\big[S_{\bar{c}}^{(K-1)}\big] \;=\; \frac{\Sigma}{m},

    so the estimator

    .. math::

       \widehat{\Sigma} \;=\; m\; S_{\bar{c}}^{(K-1)}

    is unbiased for :math:`\Sigma` under the iid block model.

Relation of the Finite-sample to the full covariance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Under the iid model, the expected within aggregate satisfies

.. math::

   \mathbb{E}[S_k] = (m-1)\Sigma, \qquad \mathbb{E}[W] = K(m-1)\Sigma,

hence

.. math::

   \mathbb{E} \left[\frac{W}{N}\right] = \frac{K(m-1)\Sigma}{Km} = \frac{m-1}{m}\Sigma,

and

.. math::

   \mathbb{E} \left[\frac{B}{N}\right] = \frac{\Sigma}{m}.

Adding these gives :math:`\mathbb{E}[\Sigma_{\mathrm{emp}}] = \Sigma`,
verifying unbiasedness of the global empirical covariance.

Summary
^^^^^^^

- If you have only the block means :math:`\{\bar{c}_k\}` and you know that each block is an average of :math:`m` iid draws, then :math:`\widehat{\Sigma}=m\,S_{\bar{c}}^{(K-1)}` is an unbiased estimator of the full covariance :math:`\Sigma`.

- If blocks are not iid samples (e.g. they are clusters with internal
  structure), then multiplying block-mean covariance by $m$ is not
  generally valid; additional modeling or within-block information is
  required.

- If you have both the full empirical covariance
  :math:`\Sigma_{\mathrm{emp}}` and the block means, you can compute
  the aggregate within scatter as

  .. math::

      W \;=\; N\Sigma_{\mathrm{emp}} - B,

  and therefore recover the sum of the within-block scatters even
  without individual :math:`S_k`.


.. _coefficient_SN:

Signal-to-noise estimates
-------------------------

.. _outsample:

Using `OutSample` with `exp`
----------------------------

Covariance data generation within `exp` is a two step process:

1. The force method computes the subsample coefficient and covariance
   estimates every `nint` steps.  The configuration parameter `nint`
   is zero by default; no subsamples or sample covariance is computed
   by default.

2. You need to instantiate an `outsamp` output routine in the `Output`
   collection with the `name` parameter to match the name of the
   component whose force has a non-zero `nint` value.

The covariance files are written in HDF5 format and take the form:
`coefcovar.{component name}.{runtag}`.

   
.. _pyEXP_covariance:

Covariance examples in `pyEXP`
------------------------------

The `pyEXP` interface is split between the creation and the reading of
HDF5 covariance files as follows:

1. Similar to the `exp` force methods, the `pyEXP.basis.BiorthBasis`
   classes can be configured to produce subsample and covariance data
   that get written to an HDF5 file.

2. The utility class `pyEXP.basis.BasisClasses.SubsampleCovariance`
   reads the HDF5 covariance files and returns sample information,
   subsample coefficients and covariance information in `numpy`
   compatible format.

The controlling configuration YAML keys are:

- `pcavar: true` -- This enables the covariance computation
  
- `samplesz: 100` -- This sets the number of subsamples to `100`.  The
  value `1` is also valid.

- `totalCovar: true` -- Computes a single covariance matrix for the
  entire ensemble.

- `fullCovar: true` -- Computes a covariance matrix for each subsample

Assume that you have created a basis instance using pyEXP named
`basis`.  After reading and generating coefficients for a particular
snapshot in the usual way, the call

.. code-block:: python

   compname = 'halo'
   runtag   = 'run1'
   time     = 3.14
   basis.writeCoefCovariance(compname, runtag, time)

will write covariance data to file named `coefcovar.halo.run1`,
creating the new file if it does not already exist, and store the
covariance data for time `3.14`.

You can read and HDF5 covariance file with the following code:

.. code-block: python

   compname = 'halo'
   runtag   = 'run1'
   covar = pyEXP.basis.CovarianceReader('coefcovar.{}.{}'.format(compname, runtag))


A typical use case might be as follows:

.. code-block: python

   # This gets the list of available snapshot times
   times  = covar.Times()
   ntimes = len(times)

   # As an example, let's look at the data for the final time
  indx   = -1
  time   = times[indx]

  # Get all the subsample data for time
  counts, masses, coefs, covrs = covar['dark'].getCoefCovariance(time)

  # The counts array contains the number of particles in each sample

  # The masses array contains the mass of the particles in each sample

  # The coefs is an ndarray of coefficient vectors indexed by sample
  # number and harmonic order

  # The coefs is an ndarray of covariance matrices indexed by sample
  # number and harmonic order

  # Following code shows how to visualize the covariance matrices
  # using pcolormesh
  

  numb   = np.sum(counts)
  mass   = np.sum(masses)
  nsamp  = counts.shape[0]

  # For pcolormesh below
  x = np.arange(0, nmaxh)
  y = np.arange(0, nmaxh)
  X, Y = np.meshgrid(x, y)

  for l in range(3):
    for m in range(l+1):
        L = basis['dark'].I(l, m)
        sumCof = np.zeros((nmaxh), dtype=np.complex128)
        sumVar = np.zeros((nmaxh, nmaxh), dtype=np.complex128)
        for T in range(nsamp):
            sumCof += coefs[T, L, :]/mass
            sumVar += covrs[T, L, :, :]/mass
        sumVar -= np.outer(sumCof, sumCof)
        # sumVar is not the full normalized covariance
        plt.pcolormesh(X, Y, np.log10(np.abs(sumVar)), cmap='viridis')
        plt.colorbar()
        plt.title('Halo covariance for l={} m={} T={}'.format(l, m, times[-1]))
        plt.show()

