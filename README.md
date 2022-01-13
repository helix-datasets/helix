![logo-title-banner]

# HELIX

[![code-style-image]][black]
[![documentation-image]][readthedocs]
[![latest-version-image]][pypi]
[![python-versions-image]][python]
[![license-image]][mit]

A source code mutation/transformation framework.

## Description

HELIX defines three major primitives:

###### Blueprints

Core project layouts including templated boilerplate and methods for generating
and building artifacts from a set of Components and Transforms.

###### Components

Small, configurable pieces of source code that represent a specific
implementation of a specific functionality along with associated metadata.

###### Transforms

Modifications of either source code or a built artifact along with associated
metadata.

Blueprints are configured with a collection of Components to include and
Transforms to apply and then built to generate build artifacts.

## Installation

Install HELIX from PyPI with pip, run:

```bash
pip install helix
```

### Dependencies

Some Blueprints, Components, and Transforms include additional, non-python
dependencies that must be installed separately. These can be installed
automatically (if supported) with the `install` command. For example, to
install dependencies for the `upx` Transform, run:

```bash
helix install transforms upx
```

To install all dependencies for all installed Blueprints, Components, and
Transforms, run:

```bash
helix install
```

Note: some Blueprints, Components, and Transforms include dependencies which
must be manually installed. Using the `install` command for these will instead
list the dependencies that must be installed manually.

## Usage

To list currently installed parts of HELIX:

```bash
helix list
```

To generate a single build, use the `build` command. For example, to generate a
build using the `cmake-cpp` blueprint, with the `configuration-example`
component (setting the `second_word` parameter to `foo`), and apply the `strip`
transform (on supported platforms), writing output files to `./example`:

```bash
helix build blueprint cmake-cpp ./example \
    -c configuration-example:second_word=foo \
    -t strip
```

The `build` command also supports loading a configuration from a JSON file and
HELIX is fairly scriptable. See the `examples/` directory or take a look at the
full documentation for more.

## Contributing

HELIX is designed to be easily extensible via [entry
points](https://packaging.python.org/tutorials/packaging-projects/#entry-points).
Blueprints, Components, and Transforms simply need to conform to their
respective abstract base classes and be exposed under their respective entry
point (see the Getting Started section of the documentation for more details
and a tutorial). External Blueprints, Components, and Transforms that are
correctly exposed are usable in all normal HELIX commands.

### Development

To set up a development environment, first clone this repo. Next, it is useful
to install HELIX in editable mode with extras for development and testing:

```bash
pip install -e .[development,testing]
```

When developing new components it can be helpful to use HELIX's `build` command
in verbose mode so that you can see compiler and linker output and correct any
errors you may encounter:

```bash
helix build blueprint cmake-cpp novel-component -c novel-component -v
```

### Documentation

To build the full HELIX documentation, after installing HELIX with
`development` extras enabled, from the `docs/` directory, run:

```bash
make html
```

Or other [supported Sphinx output
formats](https://www.sphinx-doc.org/en/master/usage/builders/index.html).

### Testing

You can expose tests for your Components and Transforms by adding a subclass of
`helix.tests.UnitTestCase` to the entrypoint `helix.tests`. Some useful testing
mixins are provided in `helix/tests.py` and for some examples see the tests
referenced in `setup.py`.

To test the HELIX interfaces and utilities, run:

```bash
helix test system
```

To test Components, Blueprints, and Transforms, run:

```bash
helix test unit
```

## Disclaimer

DISTRIBUTION STATEMENT A. Approved for public release: distribution unlimited.

© 2021 Massachusetts Institute of Technology

- Subject to FAR 52.227-11 – Patent Rights – Ownership by the Contractor (May 2014)
- SPDX-License-Identifier: MIT

This material is based upon work supported by the Department of Defense under
Air Force Contract No. FA8721-05-C-0002 and/or FA8702-15-D-0001. Any opinions,
findings, conclusions or recommendations expressed in this material are those
of the author(s) and do not necessarily reflect the views of the Department of
Defense.

[MIT License](LICENSE.txt)

[logo-title-banner]: /images/logo-title-banner-white.png

[code-style-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black]: https://github.com/psf/black
[documentation-image]: https://img.shields.io/readthedocs/helix-datasets
[readthedocs]: https://helix-datasets.readthedocs.io/
[latest-version-image]: https://img.shields.io/pypi/v/helix
[pypi]: https://pypi.org/project/helix/
[python-versions-image]: https://img.shields.io/pypi/pyversions/helix
[python]: https://www.python.org/
[license-image]: https://img.shields.io/pypi/l/helix
[mit]: ./LICENSE.txt
