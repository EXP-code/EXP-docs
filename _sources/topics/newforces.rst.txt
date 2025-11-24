.. _newforces:

How to make a new EXP force
===========================

First, decide whether your new force is self-consistent (intended to
compute the acceleration by computing a force field from a particle
distribution) or external or auxiliary (intended to manipulate the
phase space but not through a mean force field).  Both types of forces
must be derived from the `PotAccel` class, the base class for
all forces, or one of its children.

By *first-class*, I mean writing your own C++ classes that inherit the
properties of an EXP base class other than `PotAccel` and become part
of the code base.  If you need to manipulate or process phase space
for diagnostic reasons, it makes more sense (and is easier) to add a
user module (see :ref:`user modules <usermodules>`).  Many times, one
can get what one needs by adding a `User` routine, but not always.  If
your new class is a basis, it should be derived from `Basis`,
`AxisymmetricBasis`, or `SphericalBasis` which is every is the most
specific for your new force.  Forces which are not bases, inherit from
`PotAccel` directly.  For example, your new class header should look
something like:

.. code-block: c++

   class MyNewForce : public PotAccel
   { . . .  };

   
There are gray areas in the API.  For example, the `Cube`
class is a simple Fourier basis but it can not use any of the methods
that `Basis` implements to make inheritance meaningful.  The
direct n-body ring code, `Direct`, is not a basis and inherits
from \texttt{PotAccel}.

Second, implement the virtual members from `PotAccel` in your
new class.  At the very least you need to implement a constructor that
accepts the force parameters as a YAML node as input and a member
function that computes the acceleration:

.. code-block: c++

    class MyNewForce : public PotAccel
    {
      .
      .
      .
    public:
    
    //! Constructor
    MyNewForce(const YAML::Node& conf);

    //! The main force call
    void get_acceleration_and_potential(Component*);
  
    };

As most developers have discovered, it is helpful to find another
implemented class and follow it as an example for your own
implementation.

Thirdly, you need to *teach* EXP about your new class.
For self-consistent forces, this is done in `Component` whose
implementation is in \texttt{src/Com\-po\-nent.cc}.  The
`initialize()` method for `Component` contains a simple
if-block parser to instantiate forces specified in the YAML
configuraton for each component.  For external forces, there is an
equivalent if-block parser in the
`ExternalCollection::initialize()` member.  In each case,
include your new header file, in the preamble for either
`Component.cc` or `ExternalCollection.cc`, as
appropriate.  For example, when adding to
`ExternalCollection.cc`, your entry might look something like:

.. code-block: c++

   #include <tidalField.H>
   #include <externalShock.H>
   #include <generateRelaxation.H>
   #include <ScatterMFP.H>
   #include <HaloBulge.H>
   #include <MyClass.H> // My new class!!!

Finally, add a compile dependency for your new class in
`src/CMakeLists.txt` by adding its source file name,
e.g. `MyClass.cc``, to the \texttt{exp\_SOURCE} variable.  And
compile!

