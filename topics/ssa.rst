.. _mssa:

Singular Spectrum Analysis
==========================

Singular Spectrum Analysis (SSA) is a non-parametric analysis tool for
for time series analysis.  It has been used for a wide variety of
primarily Earth-science problems where finite data sets that may be
censored are prevalent.  It makes no strong prior assumptions about
the spectrum.  There is a natural multivariate extension (called
*multichannel* in the literature) that we will use below.

In most applications, the time series is a direct observable.  The
main extension here is to use the spatial summary provided by our
biorthogonal-function coefficients as the multichannel data.  The
subsequent analysis is then a combined spatio-temporal filter and
reconstruction of the dynamics.  This is exactly what we need and want
for n-body dynamical analysis.

SSA algorithms and methodology
------------------------------

SSA analysis separates the observed time series into the sum of
interpretable components with no a priori information about the time
series structure. We begin with a statement of the underlying
algorithm for a single time series.  Think: one particular
coefficient :math:`a_j(t)` from equation (\ref{eq:coefdef}) at a
particular time step.  Let us simply denote the coefficient at time
step :math:`k` as :math:`a_{j,k} = a_j(t_o+hk)` where :math:`h` is the time-step
interval.

Algorithm of SSA analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

Now, consider the real-valued time series of coefficients
:math:`\mathbf{a}_N=(a_1,\ldots,a_{N})` of length :math:`N`.  Since we
are considering a single coefficient :math:`a_j(t)`, we will drop the
coefficient index :math:`j` for now.  Define the \emph{window length}
:math:`L` and let :math:`K=N-L+1`. The SSA algorithm (1) decomposes the
temporal cross-correlation matrix by an eigenfunction analysis into
uncorrelated components and then (2) reconstructs relevant parts of
the time series.  We will now consider each step in detail.

Decomposition
^^^^^^^^^^^^^

**Embedding**
"""""""""""""

We *embed* the original time series into a sequence of lagged vectors
of size :math:`L` by forming :math:`K=N-L+1` *lagged vectors*

.. math::
   A_i=(a_{i},\ldots,a_{i+L-1})^\top, \quad i=1\ldots,K.

The *trajectory matrix* of the series :math:`A_N` is:

.. math::
   \begin{equation}
   \label{eq:traj_m}
   \mathbf{T} = [A_1:\ldots:A_K]=(T_{ij})_{i,j=1}^{L,K}=
   \left(
   \begin{array}{lllll}
   a_1&a_2&a_3&\ldots&a_{K}\cr
   a_2&a_3&a_4&\ldots&a_{K+1}\cr
   a_3&a_4&a_5&\ldots&a_{K+2}\cr
   \vdots&\vdots&\vdots&\ddots&\vdots\cr
   a_{L}&a_{L+1}&a_{L+2}&\ldots&a_{N}\cr
   \end{array}
   \right).
   \end{equation}

There are two important properties of the trajectory matrix: the rows
and columns of :math:`\mathbf{T}` are subseries of the original series,
and :math:`\mathbf{T}` has equal elements on anti-diagonals and therefore
the trajectory matrix is has the Hankel property.

From the trajectory matrix, we can form the *lag-covariance*
matrix:

.. math::
   \begin{equation}
   \label{eq:lagcovar}
   \mathbf{C} = \frac{1}{K} \mathbf{T}^\top\cdot\mathbf{T}.
   \end{equation}

*Decomposition*
"""""""""""""""

We may analyze the lag-covariance matrix using the standard singular
value decomposition (SVD). \index{singular value decomposition (SVD)}
From the form of equation (\ref{eq:lagcovar}), we observe that
:math:`\mathbf{C}` is real, symmetric and positive definite, so the SVD
yields a decomposition of the form: :math:`\mathbf{C} =
\mathbf{U}\cdot\mathbf{\Lambda}\cdot\mathbf{V}^\top` where
:math:`\mathbf{\Lambda}` is diagonal. The symmetry properties imply that
the left- and right-singular vectors are the same, or
:math:`\mathbf{E}\equiv\mathbf{U}=\mathbf{V}`.  We may then write

.. math::
   \begin{equation}
   \mathbf{\Lambda} = \mathbf{E}^\top\cdot\mathbf{C}\cdot\mathbf{E}.
   \end{equation}

The matrix :math:`\mathbf{\Lambda}` is a diagonal matrix of eigenvalues,
:math:`\lambda_k` and the columns of :math:`\mathbf{E}` are the eigenvectors,
:math:`\mathbf{E}^k`.

An alternative decomposition is based on the eigenvectors of the
Toeplitz matrix :math:`\mathbf{C}` whose entries are

.. math::
   c_{ij}=\frac{1}{N-|i-j|} \sum_{n=1}^{N-|i-j|}a_n a_{n+|i-j|}, \quad
   1\leq i,j\leq L.

In both cases the eigenvectors are ordered so that the corresponding
eigenvalues are placed in the decreasing order.  The Toeplitz
formulation reduces approximately to the covariance form for
stationary time series with zero mean.  Since this is not the case for
most of our simulations, we will adopt Choice 1. The pair
:math:`(\sqrt{\lambda_k}, \mathbf{E}^k)` will be called :math:`k`th
\emph{eigenpair}.  I will assume that the eigenpairs are sorted in
order of decreasing value of :math:`\lambda_k>0`, which is traditional for
SVD.  As before, we may write this decomposition in *elementary
matrix* form as

.. math::
   \begin{equation}
   \mathbf{C} = \sum_k \lambda_k \mathbf{E}^k \mathbf{E}^{k\top}
   = \sum_k \lambda_k \mathbf{E}^k \otimes \mathbf{E}^{k}   
   = \sum_k \mathbf{C}_k
   \end{equation}

where :math:`\mathbf{a}\otimes\mathbf{b}` denotes the outer or Kronecker
product of the vectors :math:`\mathbf{a}` and :math:`\mathbf{b}` and
:math:`\mathbf{C}_k \equiv \lambda_k \mathbf{E}^k\otimes\mathbf{E}^k`.
Clearly, the :math:`\mathbf{C}_k` have dimension :math:`K\times K`.

Reconstruction
^^^^^^^^^^^^^^

**Eigenpair grouping**
""""""""""""""""""""""

Let :math:`d=\max\{j:\ \lambda_j \neq \epsilon\}`, where :math:`\epsilon` is
some threshold for the eigenvector to be in the null space.  From the
decomposition in equation \ref{eq:elem_matr}, the grouping procedure
partitions the set of indices :math:`\{1,\ldots,d\}` into :math:`m` disjoint
subsets :math:`I_1,\ldots,I_m`.

Define :math:`\mathbf{C}_I=\sum_{k\in I} \mathbf{C_k}`.
Equation \ref{eq:elem_matr} leads to the decomposition

.. math::

   \begin{equation}
   \label{eq:mexp_g}
   \mathbf{C}=\mathbf{C}_{I_1}+\ldots+\mathbf{C}_{I_m}.
   \end{equation}

The procedure of choosing the sets :math:`I_1,\ldots,I_m` is called
*eigenpair grouping*. If :math:`m=d` and :math:`I_k=\{k\}`,
:math:`k=1,\ldots,d`, then the corresponding grouping is called
*elementary*.  The choice of several leading eigentriples corresponds
to the approximation of the time series in view of the well-known
optimality property of the SVD.

**The principal components**
""""""""""""""""""""""""""""

We may now project the original time series represented in the
trajectory matrix in to the new basis represented by :math:`\mathbf{E}`:
:math:`\mathbf{P} = \mathbf{E}^\top\cdot \mathbf{T}`. The columns of
:math:`\mathbf{P}` are known as the \emph{principal components}, following
the terminology of standard Principal Component Analysis (PCA).  In
components, the :math:`k` eigenpair yields at time step :math:`j` is

.. math::
   \begin{equation}
   \label{eq:pc1d}
   P^k_j = \sum_{l=1}^L E^k_l T_{lj}  = \sum_{l=1}^L E^k_l a_{j+l-1} 
   \end{equation}

The principal components are uncorrelated (i.e. orthogonal) by
construction.

**The reconstructed components**
""""""""""""""""""""""""""""""""

At this step, project the principle components back to the original
basis and then diagonally average the result, imposing the Hankel
property of the original trajectory matrix to get an approximation to
the contribution to the coefficients.  Specifically, the transformed
principle components corresponding to the eigenpair :math:`k` are:
:math:`\tilde{\mathbf{T}}^k = \mathbf{P}^\cdot\cdot\mathbf{E}^k`.
Making the *diagonal average* to get the reconstructed coefficients,
we have:

.. math::
   \begin{equation}
   \tilde{a}^k_j =
   \begin{cases} \displaystyle
   \frac{1}{j} \sum_{n=1}^{j} P^k_{n-j+1} E^k_n & \mbox{if}\ 1\le j < L-1, \\
   \displaystyle
   \frac{1}{L} \sum_{n=1}^{L} P^k_{n-j+1} E^k_n & \mbox{if}\ L\le j \le N - L + 1 \, \\
   \displaystyle
    \frac{1}{N-j+1} \sum_{n=N-L+1}^{N} P^k_{n-j+1} E^k_l & \mbox{if}\ N-L+2\le j \le N. \\
   \end{cases}
   \end{equation}


Separability and choice of parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of grouping into sets :math:`\{I_j\}` is the separation of the
time series into distinct dynamical components.
Distinct time series components can be
identified based on their similar temporal properties.  For example,
if the underlying dynamical signals are periodic, then the eigenvectors
will reflect that by producing sine- and cosine-like pairs with
distinct frequencies.
Thus, graphs of eigenvectors or discrete Fourier transforms can help 
identify like components.

Very helpful information for separation is contained in the so-called
:math:`\mathbf{W}`-correlation matrix. This is the matrix consisting of
weighted correlations between the reconstructed time series
components. The weights reflects the number of entries of the time
series terms into its trajectory matrix. Well separated components
have small correlation whereas badly separated components have large
correlation. Therefore, looking at the :math:`\mathbf{W}`-correlation
matrix one can find groups of correlated elementary reconstructed
series and use this information for the consequent grouping. One of
the rules is not to include into different groups the correlated
components.

Multichannel SSA (M-SSA)
------------------------

We can now generalize the SSA to :math:`M` time series, here assume to be
:math:`M` particular coefficients from equation (\ref{eq:coefdef}): the
set :math:`\mathcal{M} = \{j_1, \ldots\, \j_M\}`.  Following the
previous section, denote each time series for the coefficient :math:`a_j`
as:

.. math::
   A_{ji}=(a_{j,i},\ldots,a_{j,i+L-1})^\top, \quad i=1\ldots,K.

where

.. math::
   \mathbf{A}_j = [A_{j1} : A_{j2} : \ldots : A_{jK}].

Then, the multichannel trajectory matrix :math:`\mathbb{T}` may be defined
as

.. math::
   \mathbb{T}_M = \left[\mathbf{A}_1, \mathbf{A}_2, \ldots,
   \mathbf{A}_M\right].

The multichannel trajectory matrix has :math:`KL` columns with length :math:`K
= N - L - 1` (rows).  The covariance matrix of this multichannel
trajectory matrix is

.. math::

   \begin{equation}
   \mathbf{C}_M = \frac{1}{K} \mathbb{T}_M^\top\cdot\mathbb{T}_M
   = \left(
   \begin{array}{lllll}
    \mathbf{C}_{1,1} & \mathbf{C}_{1,2} & \mathbf{C}_{1,3} &\ldots& \mathbf{C}_{1,M}\cr
    \mathbf{C}_{2,1} & \mathbf{C}_{2,2} & \mathbf{C}_{2,3} &\ldots& \mathbf{C}_{2,M}\cr
    \mathbf{C}_{3,1} & \mathbf{C}_{3,2} & \mathbf{C}_{3,3} &\ldots& \mathbf{C}_{3,M}\cr
    \vdots&\vdots&\vdots&\ddots&\vdots\cr
    \mathbf{C}_{M,1} & \mathbf{C}_{L,2} & \mathbf{C}_{L,3} &\ldots& \mathbf{C}_{M,M}\cr
  \end{array}
  \right)
  \end{equation}

where each submatrix is

.. math::
   \begin{equation}
   \mathbf{C}_{j,k} =
   \frac{1}{K}\mathbf{A}_j^\top\cdot\mathbf{A}_k.
   \end{equation}

Each submatrix :math:`\mathbf{C}_{j,k}` has dimension :math:`K\times K` as in
the one-dimensional SSA case.

The SVD step is the same as
in the one-dimensional SSA.  However, each eigenvector now has a block
of length :math:`K` that corresponds to each series.  Let us denote this
as

.. math::
   \mathbf{E}^k = \left[\mathbf{E}^k_1 : \mathbf{E}^k_2 : \ldots :
   \mathbf{E}^k_M\right].


As for standard SSA, we obtain the principle components by projecting
the trajectory matrix into the new basis as follows:

.. math::
   \begin{equation}
   P^k_i = \sum_{m=1}^M \sum_{j=1}^L a_{m,i+j-1} E^k_{m, j}.
   \end{equation}

The principle components are single orthongonal time series that
represent a mixture of all the contributions from the original time
series.

Finally, the last step of the process reconstructs the original time
series of index :math:`m\in[1,\ldots, M]` from the principle components as
follows:

.. math::

   \begin{equation}
   \tilde{a}^k_{m,j} =
   \begin{cases} \displaystyle
   \frac{1}{j} \sum_{n=1}^{j} P^k_{n-j+1} E^k_{m,n} & \mbox{if}\ 1\le j < L-1, \\
   \displaystyle
    \frac{1}{L} \sum_{n=1}^{L} P^k_{n-j+1} E^k_{m,n} & \mbox{if}\ L\le j \le N - L + 1 \, \\
    \displaystyle
    \frac{1}{N-j+1} \sum_{n=1-N+M}^{N} P^k_{n-j+1} E^k_m & \mbox{if}\ N-L+2\le j \le N. \\
    \end{cases}
    \end{equation}

If we sum up all of the individual principle components, no
information is lost; that is:

.. math::
   \begin{equation}
   a_{m,i} \rightarrow \sum_{k=1}^d \tilde{a}^k_{m,i}
   \end{equation}

In practice, we often want to sum up the reconstructions for specific
groupings:

.. math::
   \begin{equation}
   \label{eq:recongroup}
   \tilde{a}_{m,i}^{I_j} = \sum_{k\in I_j} \tilde{a}^k_{m,i}
   \end{equation}

which gives us the parts of of each coefficient :math:`a_l(t)` that
correspond to each dynamical component :math:`I_j`.

Applications of M-SSA
---------------------

- *Compression.* In many cases, a small number of
    eigenpairs relative to the total number :math:`MK` have the lion's
    share of the variance; that is:

    .. math::
       \frac{\sum_{k=1}^d\lambda_k}{\sum_{k=1}^{MK}\lambda_k} \approx 1

    for :math:`d\ll MK`.  Therefore, we can reconstruct most of the
    dynamics with a small number of eigenpairs.

- *Diagnostics.*  Similarly, we can use the
      :math:`\tilde{a}_{m,i}^{I_j}` to reconstruct the underlying
      potential or density fields in physical space using the standard 
      BFE series.

- *Channel contributions.* One can use the reconstructions to an
      estimate of the fraction of each coefficient in any particular
      eigenpair or group.  Specifically, let us measure the
      contribution of the :math:`k`th eigenpair to the :math:`j`th
      coefficient by: \begin{equation} f^k_j \equiv
      \frac{||\tilde{\mathbf{a}}^k_j||_F}{||\mathbf{a}_j||_F},
      \end{equation} where the Frobenius norm :math:`||\cdot||_F` is
      equivalent to the Euclidean norm in this context:
      :math:`||\mathbf{x}||_F = \sqrt{\mathbf{x}\cdot\mathbf{x}}`.  By
      definition :math:`0<f^k_j<1` and :math:`\sum_k f^k_j=1`. Thus,
      :math:`f^k_j` tells us the fraction of time series :math:`j`
      that is in principal component :math:`k`.  Alternatively, we
      compute measure: \begin{equation} g^k_j \equiv
      \frac{||\tilde{\mathbf{a}}^k_j||_F}{\sum_{j=1}^M||\mathbf{a}^k_j||_F},
      \end{equation} which is the fraction of principal component in
      series :math:`j`.  Thus, the histogram :math:`g^k_j` reflects
      the partitioning of power in the principal component :math:`k`
      into the input coefficient channels :math:`j`.

      So, we can think of this representation as a single matrix,
      normed on rows in the case of :math:`f` and normed on columns in the
      case of :math:`g`.

      In both cases, the norm over the time series may be restricted
      to some window smaller than the total time series.

- *Dynamical correlations.* This application is motivated by the
      structure of the biorthogonal expansion described in
      :ref:`theory <bfetheory>`.  For example, we have found
      (Petersen et al. 2019c) that strong perturbations couple
      harmonic subspaces that would be uncoupled at linear order.  By
      selecting particular coefficients from various harmonics
      (:math:`m=1, 2` in our case), we can look for the joint mode.
  
