Testing
-------

HELIX includes three different categories of tests:

``system``
    Unit tests for HELIX's core system functionality - these are typically only
    run by core HELIX developers.

``unit``
    Unit tests for individual Blueprints, Components, and Transforms - these
    are written by internal and external developers and can be used to test
    custom Blueprints, Components, and Transforms as well as those built into
    HELIX.

``integration``
    Integration tests for running multiple sets of Blueprints, Components, and
    Transforms together to ensure they work in concert.

These test suites can be run with the the ``test`` CLI command. For example, to
run all unit tests for Blueprints, Components, and Transforms, run:

.. code-block:: bash

    helix test unit
