.. _news:

Release notes
=============

.. _release-7.7.26:


EXP 7.7.26 (2023-10-02)
-----------------------

General changes
~~~~~~~~~~~~~~~

- Added code to enforce a sign convention on SL eigenfunctions
  (`SphericalSL`) and EOF eigenvectors (`Cylindrical`). The
  eigenfunctions from numerical methods can have either sign and still
  be good eigenvectors. This change ensures a consistent sign even if
  the basis needs to be remade or slightly tweaked (e.g. remade with
  larger nmax).  Note, however, that older bases will still have
  arbitrary signs.

  You have two options to deal with this:
  
  1. You can make a new basis and remake your coefficients to take
     advantage of the new sign convention
  2. Retain and reuse your old bases (see note for `SphericalSL`
     below)

- Check the orthgonality of adaptive bases on creation and throw
  exception if they are not sufficiently biorthogonal

- Throw exceptions for SL solutions that fall below a reasonable error
  threshold

- Implemented both OpenMP and MPI parallel FieldGenerator evaluation for
  improved throughput

- Improve logged output readability for user with additional
  formatting

- Fixed an error in expMSSA for OpenMP threading on Macs


Cylindrical basis
~~~~~~~~~~~~~~~~~

- The `density` flag is now inactive and deprecated.  The density
  field for cylindrical bases is always computed.

- Fixed missing factor of 1/(4*pi) in density field; correct return
  matrix so the diagonal is 1 for both m=0 and m>0.  This was a true
  bug that would not have affected coefficient computation but would
  give density fields too large by 4*pi

Spherical Basis
~~~~~~~~~~~~~~~

- Rename `rs` to `rmapping` in pyEXP and EXP

- Note the difference between `scale` and `rmapping`:

  * The `rmapping` parameter is a radial scale is used to map large
    or infinite ranges to the unit segment for tables.

  * The `scale` parameter is linear rescaling of the radius to the
    original basis.  This would be used for tidal truncation, for
    example.

    You can convert an existing basis file, say `SLGridSph.cache.tmp`
    to the new attributes with the following Python code:

.. code-block:: python

   #!/usr/bin/env python
   import h5py

   # This will add a new attribute 'rmapping" with the same value as
   # 'rs' and update the file.

   f = h5py.File('SLGridSph.cache.tmp', 'r+')
   f.attrs['rmapping'] = f.attrs['rs']
   f.close()


.. _release-7.6.0:

EXP 7.6.0 (2023-02-02)
----------------------

- The stable main branch is merged from the 7.7.18 development branch

- This branch will only be updated for bug fixes moving forward

.. _release-7.7.18:

EXP 7.7.18 (2023-01-29)
-----------------------

- 'sphereSL' in pyEXP.basis updated to use rmin from the input table by
  default

- Devel branch and Main now reflect the new versioning policy

New features
~~~~~~~~~~~~

-  Implemented the proposed versioning policy

Bug fixes
~~~~~~~~~

-  pyEXP basis factory for a spherical basis will now use the model
   table minimum as the default ``rmin`` value

.. _release-7.7.17:

EXP 7.7.17 (2022-12-05)
-----------------------

New features
~~~~~~~~~~~~

-   Project is now hosted by github

Bug fixes
~~~~~~~~~

-   Many minor pyEXP bug fixes

Documentation
~~~~~~~~~~~~~

-   Sphinx/ReadTheDocs writing in progress

Quality assurance
~~~~~~~~~~~~~~~~~

