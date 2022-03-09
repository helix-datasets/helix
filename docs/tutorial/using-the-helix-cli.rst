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

HELIX also includes some simple dataset generation tools. To generate a dataset
of 25 samples consisting of 3 Components each using the ``random`` strategy and
selecting Components from a few different configurations of the example
Components, run:

.. code-block:: bash

    helix dataset-similarity random dataset \
        --sample-count 25 \
        --component-count 3 \
        -c minimal-example \
        configuration-example:first_word=hello,second_word=world \
        configuration-example:first_word=bonjour,second_word='le monde' \
        configuration-example:first_word=ciao,second_word=mondo \
        configuration-example:first_word=hola,second_word=mundo \
        configuration-example:first_word=hallo,second_word=welt \
        -t strip

.. note:: For more detail on the ``dataset`` commands and additional examples,
    see :ref:`datasets`.
