Using the HELIX CLI
-------------------

Once HELIX is installed, you can use the HELIX CLI by simply running:

.. code-block:: bash
    
    helix <command>

You can list all of the installed Blueprints, Components, and Transforms with:

.. code-block:: bash

    helix list

After installing the required dependencies (see :ref:`additional-dependencies`)
for Blueprints, Components, and Transforms, you can generate HELIX builds with
the ``build`` command. For example, to build the ``cmake-cpp`` Blueprint with
the ``configuration-example`` Component and the ``strip`` Transform and write
the output to ``./example``, run:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example \
        -c configuration-example:second_word=foo \
        -t strip

This should output a message listing the relevant metadata tags and the built
artifacts (in this case, a single, UPX-packed binary that simply prints "hello
foo").

.. note:: For more detail on the ``build`` command and additional examples, see
    :ref:`building`.
