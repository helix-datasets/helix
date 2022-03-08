.. _building:

Building
--------

There are a couple of supported ways to build a Blueprint and a collection of
Components and Transforms with the HELIX CLI. Namely, you can specify a
configuration via command line arguments or you can generate a build from a
JSON configuration file.

Building with CLI Arguments
***************************

A simple example (given elsewhere in this documentation) builds the
``cmake-cpp`` Blueprint with the ``configuration-example`` Component and the
``strip`` Transform and writes the output to ``./example``:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example \
        -c configuration-example:second_word=foo \
        -t strip 

It is also possible to specify multiple components and transforms to generate
an arbitrarily complex build. For example, using some of HELIX's built-in
Components and Transforms, we can generate a build that:

1. Downloads a remove file (https://www.google.com/).
2. Compresses the file using ``zlib``.
3. Encrypts the compressed file with ``aes`` and a fixed key.
4. Deletes the unencrypted file.
5. Deletes the uncompressed file.
6. Timestomps the compressed, encrypted download.

We can then strip and UPX compress this build, all using only built-in HELIX
Components and Transforms:

.. code-block:: bash

    helix build blueprint cmake-cpp example \
        -c linux-libcurl-remote-file-copy:url=https://www.google.com/,output=test.txt \
           linux-zlib-compress-data-compressed:input=test.txt,output=test.txt.gz \
           linux-openssl-aes-encrypt-data-encrypted:input=test.txt.gz,output=test.txt.gz.enc,key=abcdefghijklmnopqrstuvwxyzabcdef \
           linux-remove-file-deletion:path=test.txt \
           linux-remove-file-deletion:path=test.txt.gz \
           linux-utime-timestomp:path=test.txt.gz.enc,timestamp="2010-01-01 12:00:00" \
        -t strip upx

Building from JSON Configuration
********************************

The HELIX CLI can also take configuration from a JSON file. For example, we can
build the following configuration:

.. code-block:: json

    {
        "name": "example",
        "blueprint": {"name": "cmake-cpp"},
        "components": [
            {
                "name": "minimal-example",
                "configuration": {}
            },
            {
                "name": "configuration-example",
                "configuration": {
                    "second_word": "example"
                }
            }
        ],
        "transforms": [
            {
                "name": "replace-example",
                "configuration": {
                    "old": "hello",
                    "new": "goodbye"
                }
            },
            {
                "name": "strip"
            }
        ]
    }

by running the following command:

.. code-block:: bash

    helix build json configuration.json ./example

External Components
*******************

The build commands also support loading Components from external sources and
downstream libraries using the :class:`helix.component.Loader` interface.
