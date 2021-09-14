.. image:: ../images/logo-title.png
    :width: 400
    :align: center
    :alt: HELIX Logo

HELIX at a Glance
-----------------

The problem of malware similarity (and, more broadly, software similarity) is
very difficult to assess. Measuring relative performance of malware similarity
solutions is very difficult without a large dataset of malware and high-quality
ground truth about the software similarity among samples of the dataset and
acquiring this ground truth for malware in the wild is nearly impossible at
scale. Enter HELIX.

HELIX is a source code generation, mutation, and transformation framework
primarily geared toward generating large, synthetic datasets of functional
malware with known, measurable software similarity. HELIX primarily consists of
three main primitives:

**Blueprints**
    Core project layouts including templated boilerplate and methods for
    generating and building artifacts from a set of Components and Transforms.
    For example, a C++ project build with CMake.

**Components**
    Small, configurable pieces of source code that represent a specific
    implementation of a specific functionality along with associated metadata.
    For example, a specific implementation of downloading a file from a given
    URL using the cURL library.

**Transforms**
    Modifications of either source code or a built artifact along with
    associated metadata. For example, the Linux binutil ``strip`` which removes
    debugging symbols from a compiled binary.

A HELIX build is made up of exactly one Blueprint, zero or more configured
Components, and zero or more configured Transforms. The result of a HELIX build
is one or more artifacts (for example, a compiled binary build from all of the
Components and transformed by all of the Transforms) and a collection of
metadata, aggregated from the included Blueprints, Components, and Transforms.

While developing individual Components and Transforms for HELIX is initially
time-consuming, the effort scales well, as the more Components and Transforms
are written for HELIX the larger dataset it is capable of generating.
