Extensions
----------

HELIX is intended to be highly modular and support external, downstream
libraries fairly transparently. Libraries can expose Blueprints, Components,
and Transforms via Python `entrypoints
<https://packaging.python.org/specifications/entry-points/>`_. Additionally,
the HELIX CLI supports external Component loading from a file in many of its
commands via the ``-l/--load`` argument. Downstream libraries can support this
behavior by implementing the :class:`helix.component.Loader` interface.

Existing, open-source extensions to HELIX which provide additional Blueprints,
Components, or Transforms include:

Blind HELIX
***********

`Blind HELIX <https://github.com/helix-datasets/blind-helix>`_ is a Component
harvesting tool that extracts Components from existing libraries via program
slicing. It supports `VCPKG <https://github.com/microsoft/vcpkg>`_ for
automatically extracting Components from well over 1000 open-source libraries.
Harvested Components should only be used for static analysis, however.
