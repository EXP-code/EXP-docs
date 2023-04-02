.. _saving-coefficients:

How to save and reuse your newly generated coefficients 
=======================================================

Saving the coefficients
-----------------------

At this point, it makes sense to save the coefficients that you have
just created. This is sone with the following call:

.. code:: ipython3

    coefs.WriteH5Coefs('test_better')

We now have a EXP HDF5 coefficient file called ``test_better.h5``. As an
example, let’s try reading the newly created file into another
coefficient container, ``coefs2``. The container has a member function
called ``CompareStanzas`` which will check on the contents. Let’s do it.

.. code:: ipython3

    # Now try reading it in
    #
    coefs2 = pyEXP.coefs.Coefs.factory('test_better.h5')
    print("Type is", coefs2.getGeometry())
    
    # Now compare with the original
    #
    coefs2.CompareStanzas(coefs)


.. parsed-literal::

    Type is sphere




.. parsed-literal::

    True



.. parsed-literal::

    Times are the same, now checking parameters at each time
    Parameters are the same, now checking coefficients


This member function will print differences. No differenced should be
printed, of course.

