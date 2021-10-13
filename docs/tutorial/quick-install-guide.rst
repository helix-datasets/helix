Quick Install Guide
-------------------

Prerequisites
*************

HELIX is supported by `Python <https://www.python.org/downloads/>`_ (>=3.5) on
both Windows and Linux and is installed with
`pip <https://pip.pypa.io/en/stable/>`_. Both Python and pip must be installed on
your system before attempting to install HELIX.

Installation
************

To install HELIX from PyPI with pip, run:

.. code-block:: bash

    pip install helix

.. _additional-dependencies:

Additional Dependencies
***********************

Some HELIX Blueprints, Components, and Transforms include additional, external
dependencies which must be installed before they can be used in HELIX builds.
To install all of these dependencies, use the ``install`` HELIX CLI command
after installing HELIX with ``pip``:

.. code-block:: bash

    helix install

.. note:: Depending on your platform, the above command may require
    root/Administrator priveleges. Some dependencies may also need to be
    manually installed - these will be listed in the output of the above
    command.

Development
***********

To set up a development environment, first clone the HELIX repo. Next, install
additional, optional extensions for development and testing by running (from
the root of the repo):

.. code-block:: bash

    pip install .[development,testing]
