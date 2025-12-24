.. role:: python(code)
       :language: python
       :class: highlight

.. _units:

Coefficient covariance estimates
================================

.. attention::

   The `exp` interface described below is under development in the
   `OutSample` branch.  You will need to ``git checkout devel`` and
   recompile to use these features in the `exp` N-body code. The
   `pyEXP` interface is currently available in the `main` branch.
   

Overview
--------

`exp` and `pyEXP` compute both the empirical covariance matrices and
coefficients in _partitions_ or _batches_ that may be used to estimate
statistical consistence of coefficients.

.. _unit-schema:

