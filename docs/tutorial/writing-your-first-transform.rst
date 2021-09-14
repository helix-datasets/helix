Writing Your First Transform
----------------------------

Prior to following this tutorial, you'll need to have a python package set up
to extend HELIX (see :ref:`building-a-python-package`).

Writing the Transform
*********************

Similar to Components, Transforms are simply Python classes that implement the
:class:`Transform<helix.transform.Transform>` interface.

Let's start by adding a ``transforms`` directory to our Python package with an
``example`` module for our new Transform. The package directory structure
should look like the following:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── transforms/
    │   │   ├── example.py
    │   │   ├── __init__.py
    │   ├── __init__.py
    └── setup.py 

Inside of ``example.py`` we'll create a simple Transform by subclassing
:class:`Transform<helix.transform.Transform>`:

.. code-block:: python
    
    # example.py

    import os
    import shutil
    import base64
    
    from helix import transform
    
    
    class ExampleTransform(transform.Transform):
        """A simple example transform."""
    
        name = "example-transform"
        verbose_name = "Example Transform"
        type = transform.Transform.TYPE_ARTIFACT
        version = "1.0.0"
        description = "A simple example transform"
        tags = (("group", "example"),)
    
        def transform(self, source, destination):
            """Print the contents of the binary.
    
            This transform doesn't actually do anything, it is just a simple
            example that prints the contents of the input file, base64 encoded.
            """
    
            source = os.path.abspath(source)
            destination = os.path.abspath(destination)
    
            with open(source, "rb") as f:
                print(base64.b64encode(f.read()))
    
            shutil.copy(source, destination)

This simple transform just prints the base64 encoding of the built artifact and
does not modify it at all. There are a couple of things to note:

1. The transform :attr:`type<helix.transform.Transform.type>` is
:attr:`TYPE_ARTIFACT<helix.transform.Transform.TYPE_ARTIFACT>` - this indicates
that the transform should be applied to artifacts after the Blueprint is built,
as opposed to :attr:`TYPE_SOURCE<helix.transform.Transform.TYPE_SOURCE>` which
is applied to source files before they are built.

2. The required :meth:`transform<helix.transform.Transform.transform>` method
must *always* write a resulting file from ``source`` to ``destination``, even
if it does not modify the contents.

Registering the Transform
*************************

Similar to Components, Transforms must be added to the entrypoint group
``helix.transforms`` in our Python package's ``setup.py``. Make the following
change to ``setup.py``:

.. code-block:: python

    # setup.py

    ...
    entry_points={
        ...
        "helix.transforms": [
            "example-transform = helix_example.transforms.example:ExampleTransform"
        ]
        ...
    }
    ...

.. note:: Similar to Components, the ``name`` property of our new Component
    *must* match the name of the entrypoint.

To update the entrypoint list, reinstall the Python package (even if you
installed it in editable mode):

.. code-block:: bash

    pip install .

Check that our new Transform is registered with the HELIX CLI:

.. code-block:: bash

    helix list

The output should include our new example Transform:

.. code-block:: bash

    Available Transforms
        ...
        Example Transform (1.0.0) [example-transform]
        ...

Finally, build a ``cmake-cpp`` Blueprint with our Transform to make sure that
it works:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example -t example-transform

.. note:: The generated binary will not do anything, but during generation you
    should see our Transform print the base64 encoding of the resulting
    artifact.

Adding Configuration Options
****************************

Adding and using configuration options to Transforms can be done in the same
way as adding configuration options to Components (see
:ref:`adding-configuration-options`).

Adding Dependencies
*******************

Specifying Transform dependencies can be done in the same way as specifying
Component dependencies (see :ref:`adding-dependencies`).

Testing the Transform
*********************

Writing unit tests for Transforms can be done in the same way as writing
unit tests for Components (see :ref:`testing-the-component`).
