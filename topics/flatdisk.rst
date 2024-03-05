.. _flatdisk_config:

How to configure a razor-thin disk?
===================================

.. index:: YAML

  This stanza defines the phase-space components with associated
  parameters and force methods as a list.  Each list element starts
  with '-' and has four fields:

  ==========     ===========
  Key word       Explanation
  ==========     ===========
  name           the mnemonic name for the component
  parameters     a list of key: value pairs
  bodyfile       the name of the ascii phase-space file to initialize this component
  force          the method for computing the potential and acceleration
  ==========     ===========

  
  The mnemonic name may contain spaces.  The body file is in EXP
  native formation.  EXP has its own hierarchical phase space
  structure that we call :ref:`PSP <exp-phase-space>`.  EXP provides a
  number of standalone routines to manipulate, visualize and summarize
  the content of PSP files.  EXP uses the list index internally to
  describe the component. However, there is support for reflection by
  mnemonic name.

