.. _topics-contributing:

===================
Contributing to EXP
===================

.. important::

    Double check that you are reading the most recent version of this document at

There are many ways to contribute to EXP. Here are some of them:

* Blog about EXP. Cite the EXP published papers. Tell the world how
  you're using EXP. This will help newcomers with more examples and
  will help the EXP project to increase its visibility.

* Report bugs and request features in the `issue tracker`_, trying to follow
  the guidelines detailed in `Reporting bugs`_ below.

* Submit new examples to 


Reporting bugs
==============

Well-written bug reports are very helpful, so keep in mind the following
guidelines when you're going to report a new bug.

* check the :ref:`FAQ <faq>` first to see if your issue is addressed in a
  well-known question

* check the `open issues`_ to see if the issue has already been reported. If it
  has, don't dismiss the report, but check the ticket history and comments. If 
  you have additional useful information, please leave a comment, or consider
  :ref:`sending a pull request <writing-patches>` with a fix.

* write **complete, reproducible, specific bug reports**. The smaller the test
  case, the better. Remember that other developers won't have your project to
  reproduce the bug, so please include all relevant files required to reproduce
  it. See for example StackOverflow's guide on creating a
  `Minimal, Complete, and Verifiable example`_ exhibiting the issue.

* the most awesome way to provide a complete reproducible example is to
  send a pull request which adds a failing test case to the
  EXP testing suite (see :ref:`submitting-patches`).
  This is helpful even if you don't have an intention to
  fix the issue yourselves.

* include the output of ``exp -v`` so developers working on your bug
  know exactly which version and platform it occurred on, which is often very
  helpful for reproducing it, or knowing if it was already fixed.

.. _Minimal, Complete, and Verifiable example: https://stackoverflow.com/help/mcve

.. _writing-patches:

Writing patches
===============

The better a patch is written, the higher the chances that it'll get accepted and the sooner it will be merged.

Well-written patches should:

* contain the minimum amount of code required for the specific change. Small
  patches are easier to review and merge. So, if you're doing more than one
  change (or bug fix), please consider submitting one patch per change. Do not
  collapse multiple changes into a single patch. For big changes consider using
  a patch queue.

* pass all EXP basic example tests. See `Running tests`_ below.

* if you're adding or changing a public (documented) API, please include
  the documentation changes in the same patch.  See `Documentation policies`_
  below.

.. _submitting-patches:

Submitting patches
==================

The best way to submit a patch is to issue a `pull request`_ on GitHub,
optionally creating a new issue first.

Remember to explain what was fixed or the new functionality (what it is, why
it's needed, etc). The more info you include, the easier will be for core
developers to understand and accept your patch.

You can also discuss the new functionality (or bug fix) before creating the
patch, but it's always good to have a patch ready to illustrate your arguments
and show that you have put some additional thought into the subject. A good
starting point is to send a pull request on GitHub. It can be simple enough to
illustrate your idea, and leave documentation/tests for later, after the idea
has been validated and proven useful.

Sometimes there is an existing pull request for the problem you'd like to
solve, which is stalled for some reason. Often the pull request is in a
right direction, but changes are requested by EXP maintainers, and the
original pull request author hasn't had time to address them.
In this case consider picking up this pull request: open
a new pull request with all commits from the original pull request, as well as
additional changes to address the raised issues. Doing so helps a lot; it is
not considered rude as long as the original author is acknowledged by keeping
his/her commits.

You can pull an existing pull request to a local branch
by running ``git fetch upstream pull/$PR_NUMBER/head:$BRANCH_NAME_TO_CREATE``
(replace 'upstream' with a remote name for scrapy repository,
``$PR_NUMBER`` with an ID of the pull request, and ``$BRANCH_NAME_TO_CREATE``
with a name of the branch you want to create locally).
See also: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/checking-out-pull-requests-locally#modifying-an-inactive-pull-request-locally.

When writing GitHub pull requests, try to keep titles short but descriptive.
E.g. For bug #411: "EXP hangs if an exception raises in start_requests"
prefer "Fix hanging when exception occurs in start_requests (#411)"
instead of "Fix for #411". Complete titles make it easy to skim through
the issue tracker.

Finally, try to keep aesthetic changes (:pep:`8` compliance, unused imports
removal, etc) in separate commits from functional changes. This will make pull
requests easier to review and more likely to get merged.


.. _documentation-policies:

Documentation policies
======================

For reference documentation of API members (classes, methods, etc.)
use docstrings and make sure that the Sphinx documentation uses the
:mod:`~sphinx.ext.autodoc` extension to pull the docstrings. API
reference documentation should follow docstring conventions and may
provide short examples.

Other types of documentation, such as tutorials or topics, should be covered in
files within the ``docs/`` directory. This includes documentation that is
specific to an API member, but goes beyond API reference documentation.

In any case, if something is covered in a docstring, use the
:mod:`~sphinx.ext.autodoc` extension to pull the docstring into the
documentation instead of duplicating the docstring in files within the
``docs/`` directory.

Documentation updates that cover new or modified features must use Sphinx’s
:rst:dir:`versionadded` and :rst:dir:`versionchanged` directives. Use
``VERSION`` as version, we will replace it with the actual version right before
the corresponding release. When we release a new major or minor version of
EXP, we remove these directives if they are older than 3 years.

Documentation about deprecated features must be removed as those features are
deprecated, so that new readers do not run into it. New deprecations and
deprecation removals are documented in the :ref:`release notes <news>`.

Running tests
-------------

Writing examples
----------------

All functionality (including new features and bug fixes) must include a test
case to check that it works as expected, so please include tests for your
patches if you want them to get accepted sooner.


.. _issue tracker: https://github.com/scrapy/scrapy/issues
.. _tests/: https://github.com/scrapy/scrapy/tree/master/tests
.. _open issues: https://github.com/scrapy/scrapy/issues
.. _pull request: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request
