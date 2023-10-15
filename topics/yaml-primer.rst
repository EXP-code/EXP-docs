.. _yaml-primer:

=============
A YAML primer
=============

Why use YAML rather than a simple list of key words or stanzas like the
commonly used Microsoft Windows INI?  There are two main reasons:

- YAML is expressive: one can encode data, maps (or
  dictionaries), arrays, matrices and import them into standard
  containers.  YAML is a conceptual generalization of the Windows
  INI and true superset of JSON (that is, all JSON is YAML).

- YAML is a standard: YAML documents can be viewed and
  manipulated with a wide variety of stand-alone editors and has
  syntactical support in vim and emacs.

- YAML has library support: there are libraries for most major
  programming languages including C/C++, Python, Golang, Perl, etc.
  The `YAML website <https://yaml.org>` maintains a nice list of links
  to available packages.  EXP uses the `yaml-cpp library
  <https://github.com/jbeder/yaml-cpp>` which is packaged in most
  Linux repositories and included in the EXP source.  For Python
  support, I use `PyYAML <https://pyyaml.org>`.  For example, this
  enables Python-based control scripts that generate initial
  conditions, configuration files, etc. and archive or manipulate
  \textsc{EXP} output.  This level of support tipped the balance for
  me when deciding on upgrading from my home-brewed INI-like parsing
  class.

You may wish to skip back to the `EXP YAML example <yamlconfig>` if
you are already familiar with YAML.

Quick introduction to YAML
--------------------------

.. index:: pair: YAML; syntax

YAML is a data serialization language designed to be easily readable.
It can store any type of data, ascii, binary, unicode, etc.

.. code-block:: yaml

   name: Sally
   # this is a comment
   # the key 'name' has value 'Sally'
   # So this means: "name = Sally"

.. index:: pair: YAML; scalars
.. index:: pair: YAML; sequences
.. index:: pair: YAML; mappings

YAML has three basic structures: scalars, sequences and mappings. A
*document* is formed by several nodes (or objects, if you prefer),
that can be a scalar node, that holds information, or a map or
sequence node, that hold other nodes. In analogy to diadic graphs,
YAML nodes can be branch or leaf nodes.  Scalars are simple values.
These can be strings, integers, float values, etc.  For example:

.. code-block:: yaml

   name: Sally # simple string
   age: 42 # an integer scalar
   description: Researcher # This is a string
   extraordinaire # that spans two lines


A *sequence* is a an indexed list of nodes:

.. code-block:: yaml

   # a sequence of strings
   cities: ['Cambridge', 'London', 'New York', 'Berkeley']

Mappings, also referred to as hashes and dictionaries (Python), is a
structure that allows you to relate identifiers and their data
directly.  These identifiers (also referred to as keys) are usually a
simple string name and the information in them can be of any type.  In
C++, these are implemented by `std::map` or `std::multimap` if the
keys are duplicated.

For example, we can are actually a map, where I give names to values.

.. code-block:: yaml

   person:
     name: Sally # this is a simple string
     age: 42 # this is an integer scalar field
     description: Sally was this age once # This is a string but that was a long time ago # that spans two lines
     # this is a string sequence
     cities:  ['Cambridge', 'London', 'New York', 'Berkeley'] 
     # this is a sequence of sequences
     durations:
       [[Sep, 1990], [Aug, 1994]]
       [[Sep, 1994], [Jul, 1998]]
       [[Aug, 1998], [Jan, 2004]]
       [[Feb, 2004], [Aug, 2010]]
       [[Aug, 2010], [Sep, 2014], [Aug, 2018]]
       # sizes do not have to be the same

We could describe a group of people, too:

.. code-block:: yaml

   people:
     - name: Sally
       age: 42
       description: Sally was this age once
     - name: Mark
       age: 39
       description: Mark and Sally are friends
     - name: Alice
       age: 55
       description: a new person in our group

This would produce a YAML node `people` which is an indexed list or
sequence.  For example, the node with info about Mark would be index
1.  E.g. if we loaded this trivial YAML document in Python using PyYAML,
we could get Mark's data as follows:

.. code-block:: python

   import yaml

   file = open('trivial.yml')
   data = yaml.load(file)
   print(data['people'][1])

which would print the node a dictionary.  PyYAML has pretty print
options as well.  Running this little Python snippet should give:

.. code-block:: bash

   {'name': 'Mark', 'age': 39, 'description': 'Mark and Sally are friends'}

Of course, these can be used together to create more and more complex
documents that can be used to store any kind of information. 

The language itself has some neat features, such key indicators
denoted by a leading `?` and variables denoted by the `&` and `*`
characters.

.. code-block:: yaml

   ?  [dark, halo]  # A complex, compound identifier
   :
      data_file: dark.psp
      # data_folder is a reusable reference
      psp_data_folder: &data_folder /home/weinberg/data
   ? [disk, star] # Another compound identifier
   :
      data_file: star.psp
      psp_data_folder: *data_folder #reusing the string

In this example, I use a sequence (denoted by `[ ]`) which allows me
to use, for example [halo, dark] or [disk, star] later, when I want to
store different types of data. This complex key feature is extremely
useful.  Caveat emptor: not all valid YAML syntax is parsed well by
PyYAML without additional decoration to identify the Python object
type.  For the example above, we would need to preface the complex key
by `!!python/tuple`.  This is one reason that the EXP configuration
currently avoids the key indicator syntax.

In principle, using reference variables might be useful when you need
to change a variable on several items. In this example, if I change
the folder where I hold my data, all I need to do is change that one
single line, instead of editing every object that reference that
variable.  I am not current using this feature of YAML in my \textsc{exp}
configurations, but the parser will parse these features correctly, in
case you want to use these features.

Some key features of YAML syntax:

- No tabs allowed. The blocks in YAML are all defined
  by indentation, and they banned tabs. More info on this here.

- White space is meaningful when starting a line and are used to identify
  blocks (through indentation).

- A colon followed by a space isn't necessarily just a colon. While
  `name: Sally` means that `name` is an scalar node and its value is
  `Sally`, `name:Sally` is an identifier with a Null value.  This
  allows colons inside values like date/time fields: `time_created:19:03`.


How to check your syntax?
-------------------------

For those who want to try YAML in all its forms, there's an online
syntax checker called `YAMLlint <https://www.yamllint.com/>`_. It
validates your text and outputs the result in various formats.  The
important part is just checking the syntax validity.  A commonly used
downloadable version in Python can be installed with

.. code-block:: bash

   $ python3 -m pip install --user yamllint		

.. note:: Python's `yamllint` routine is more conservative then the YAML
	  standard

The EXP n-body installation provides a simple EXP-specific YAML
checker, `expyaml` implemented using the `yaml-cpp
<https://github.com/jbeder/yaml-cpp>`_ library. This will be installed
in the same directory as `exp` if you have specified `ENABLE_NBODY` in
your CMake configuration (see :ref:`compile-features`).  Since it uses
the same parser as the EXP code, a successful check implies that the
YAML syntax is correct.  It does not provide detailed syntax
diagnostics like `yamllint`.  You can optionally print the parsed YAML
database tree to standard output or a file and turn off EXP stanza
detection using the `--noEXP` flag.  Some typical examples are shown
below:


.. code-block:: bash

   expyaml config.yml     # Quick syntax check
   expyaml -v config.yml  # Syntax check, parsed data to stdout
   expyaml -o test.yml config.yml  # Parsed data to file 'test.yml'
   

The `expyaml` code will warn you by default if any necessary map
entries are missing or duplicated.

You can include entries that are not part of the EXP YAML convention
and they will be ignored by EXP.  For example, you can include a
`Comment` stanza as follows:

.. code-block:: YAML

   Comment:
     - Project: This is Run0 for the tidal interaction project
     - Author: Martin Weinberg
     - Date: June 23, 2022
   # EXP will ignore the above stanza
   Global:
   .
   .
   .

