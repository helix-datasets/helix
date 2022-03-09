.. _datasets:

Dataset Generation
------------------

HELIX includes a few utilities for generating simple datasets with known ground
truth from a library of Blueprints, Components, and Transforms. These datasets
fall into two categories:

Similarity Datasets
    Ground truth labels for these datasets consists of labels for individual
    samples gathered by aggregating the labels of the included Components. The
    "similarity" of any two samples can be computed by comparing their lists of
    labels. These datasets are useful for evaluating program similarity
    approaches.

Classification Datasets
    Samples in these datasets are assigned to a synthetic "class", where
    members of the class will be more similar to other members of the same
    class and different from members of other classes. These datasets are
    useful for evaluating classification approaches based on program
    similarity.

Generating Similarity Datasets
******************************

HELIX provides the aptly named ``dataset-similarity`` command for generating
similarity datasets using combinations of Components. There are a number of
different Component selection strategies available. In the simplest case, the
following command uses the ``simple`` strategy (where only a single Component
is included per sample), writing results to a directory named ``dataset``, for
a few different configurations of the ``configuration-example`` Component.

.. code-block:: bash

    helix dataset-similarity simple dataset \
        -c configuration-example:first_word=hello,second_word=world \
        configuration-example:first_word=bonjour,second_word='le monde' \
        configuration-example:first_word=ciao,second_word=mondo \
        configuration-example:first_word=hola,second_word=mundo \
        configuration-example:first_word=hallo,second_word=welt

The generated dataset consists of five samples, one for each included Component
configuration. Build output is logged to the sample directories in ``dataset``
and dataset labels are written to ``dataset/labels.json``.

The ``simple`` strategy isn't much more than a sanity check - more
sophisticated strategies are also supported: ``random`` which randomly selects
combinations of the provided Components and ``walk`` which randomly selects an
initial combination of Components, then randomly permutes a small portion of
them each time. Supported Transforms can also be applied to all samples in a
dataset. For example, the following command generates a dataset using the
``random`` strategy with the same Components and configurations above as well
as the ``minimal-example`` Component, including three Components per sample,
and applying the ``strip`` Transform to all samples:

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

Generating Classification Datasets
**********************************

Coming soon...

External Components
*******************

Dataset generation also supports loading Components from external sources and
downstream libraries using the :class:`helix.component.Loader` interface.
