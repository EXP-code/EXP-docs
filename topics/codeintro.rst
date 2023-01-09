.. _code-intro:

==========
Code intro
==========

This code uses :index:`object-oriented` (o-o) design patterns to
exploit the similarity in overall structure of all biorthogonal
expansions for ease of development and maintenance.  The o-o class
hierarchy enables reuse and reconfiguration for any number of
phase-space components whose gravity may be represented by a
appropriate biorthgonal bases and direct gravity methods.  The
object-oriented design enforces minimal consistency while retaining
flexibility.

Although the core code is intended to be maintained by developers,
users may write, compile and contribute new phase space operators for
applying perturbations, new force methods, etc. without changing or
recompiling the base code.  This is accomplished using dynamically
loadable libraries (see :ref:`user modules <usermodules>` for
details and a simple example).  Additional software details can be
found in :ref:`extending EXP <extending>`.



