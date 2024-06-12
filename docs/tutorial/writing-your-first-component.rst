.. _writing-your-first-component:

Writing Your First Component
----------------------------

.. _building-a-python-package:

Building a Python Package
*************************

HELIX makes use of Python `entrypoints
<https://packaging.python.org/specifications/entry-points/>`_ to discover
installed Blueprints, Components, and Transforms. Additional Blueprints,
Components, and Transforms can be installed by bundling them in a Python
package with an entrypoint in one of the following groups:

- ``helix.blueprints``
- ``helix.components``
- ``helix.transforms``

The name of the entrypoint should correspond with the name of the Blueprint,
Component, or Transform, and the object reference should refer to the class of
its implementation.

To start, create a basic python package named ``helix-example`` by creating the
following directory structure:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── __init__.py
    └── setup.py

The ``__init__.py`` file should be blank and ``setup.py`` should consist of the
following:

.. code-block:: python

    # setup.py

    from setuptools import setup
    from setuptools import find_packages

    setup(
        name="helix-example",
        version="1.0.0",
        author="Your Name Here",
        author_email="you@your-domain",
        description="An example external HELIX package",
        url="http://your-domain",
        packages=find_packages(),
        python_requires=">=3.5",
        install_requires=[],
        include_package_data=True,
        zip_safe=False,
        entry_points={
            "helix.blueprints": [],
            "helix.components": [],
            "helix.transforms": [],
            "helix.tests": []
        },
    )

This is the basic layout of a Python package - in later sections, we will
create Components and Transforms and register them as entrypoints. You can
install the package with:

.. code-block:: bash

    pip install .


.. note:: For ease of development, it can be useful to install the Python
    package in `editable mode
    <https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs>`_ to
    avoid having to reinstall the package every time you make changes.  You can do
    this by instead running:

    .. code-block:: bash

        pip install -e .

Writing the Component
*********************

Components are simply Python classes that implement the
:class:`Component<helix.component.Component>` interface. To write a simple
component, all you need to do is subclass this base class and implement the
required abstract methods.

Let's start by adding a ``components`` directory to our Python package with an
``example`` module for our new Component. The package directory structure
should look like the following:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── components/
    │   │   ├── example.py
    │   │   ├── __init__.py
    │   ├── __init__.py
    └── setup.py

Inside of ``example.py`` we'll create a simple Component by subclassing
:class:`Component<helix.component.Component>`:

.. code-block:: python

    # example.py

    from helix import component
    
    
    class ExampleComponent(component.Component):
        """A simple example component."""
    
        name = "example-component"
        verbose_name = "Example Component"
        type = "example"
        version = "1.0.0"
        description = "A simple example component"
        date = "2020-10-20 12:00:00.000000"
        tags = (("group", "example"),)

        blueprints = ["cmake-c", "cmake-cpp"]

        functions = [r"""
            #include <stdio.h>

            void ${hello_world}() {
                printf("hello world\n");
            }
        """]
        calls = {
            "main": [
                r'${hello_world}();'
            ]
        }
        globals = ["hello_world"]

We start by defining required metadata
(:attr:`name<helix.component.Component.name>`,
:attr:`verbose_name<helix.component.Component.verbose_name>`,
:attr:`type<helix.component.Component.type>`, etc.). Next, we need to define
which Blueprints this Component is designed to work with - since we're writing
code that could be compiled as either C or C++ code, we support both
:class:`CMakeCBlueprint<helix.blueprints.CMakeCBlueprint>` and
:class:`CMakeCBlueprint<helix.blueprints.CMakeCppBlueprint>` by name. Next, we
define a simple function ``hello_world`` that simply prints ``"hello world"``
by adding it to the the :attr:`functions<helix.component.Component.functions>`
list for the Component.  Note that the function name is surrounded in template
parameters (``${...}``).  These template parameters tell the build system how
to finalize Components so that duplicate function names do create conflicts.
Any template parameters like these that need to be deduplicated by the build
system should be included in the
:attr:`globals<helix.component.Component.globals>` property.

Finally, we'll add a single call at the ``main`` callsite (defined by the
``cmake`` Blueprints - see
:attr:`helix.blueprints.CMakeCBlueprint.CALLSITE_MAIN`) which calls our
``hello_world`` function.
:attr:`callsites<helix.blueprint.Blueprint.callsites>` are defined by each
individual Blueprint and provide a way for Components to invoke their
functions. The ``cmake`` Blueprints' ``main`` callsite, as the name suggests,
allows Components to call functions inside of the generated binary's ``main``
function. We can make use of this callsite by adding it to the
:attr:`calls<helix.component.Component.calls>` property for the Component.

.. note:: Because the ``printf`` function is a part of the ``stdio`` library,
    we have to add an include that references it. We can simply add this to our
    function definition.

Our Component definition is now complete.

Registering the Component
*************************

To register the component so that HELIX can find it, we need to add an
entrypoint in the group ``helix.components`` to our Python package's
``setup.py``. Make the following change to ``setup.py``:

.. code-block:: python

    # setup.py

    ...
    entry_points={
        ...
        "helix.components": [
            "example-component = helix_example.components.example:ExampleComponent"
        ],
        ...
    }
    ...

.. note:: The ``name`` property of our new Component *must* match the name of
    the entrypoint.

To update the entrypoint list, reinstall the Python package (even if you
installed it in editable mode):

.. code-block:: bash

    pip install .

Check that our new Component is registered with the HELIX CLI:

.. code-block:: bash

    helix list

The output should include our new example Component:

.. code-block::

    Available Components:
      ...
      Example Component (1.0.0) [example-component]
      ...

Finally, build a ``cmake-cpp`` Blueprint with our Component to make sure that
it works:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example -c example-component

Run the generated artifact binary - it should simply print "hello world" and
exit.

.. note:: While developing a new component, it can be useful to build in
    verbose mode (``-v/--verbose``) to see the full output of the build
    commands to assist in debugging.


.. _adding-configuration-options:

Adding Configuration Options
****************************

Configuration options may be specified for Components in the
:attr:`options<helix.component.Component.options>` property. Make the following
changes to the ``ExampleComponent`` class to define an optional configuration
parameter ``message`` which will be printed to the console:

.. code-block:: python

    # example.py

    from helix import utils

    ...

    class ExampleComponent(component.Component):
        ...
        options = {"message": {"default": "hello world"}}
        ...

        # The following lines may be removed:

        # functions = [r"""
        #     #include <stdio.h>

        #     void ${hello_world}() {
        #         printf("hello world\n");
        #     }
        # """]
        # calls = {
        #     "main": [
        #         r'${hello_world}();'
        #     ]
        # }
        # globals = ["hello_world"]

        TEMPLATE = r"""
            #include <stdio.h>

            void ${hello_wolrd}() {
                printf("${message}\n");
            }
        """

        def generate(self):
            function = utils.substitute(self.TEMPLATE, message=self.configuration["message"])

            self.functions = [function]
            self.calls = {
                "main": [
                    r'${hello_world}();'
                ]
            }
            self.globals = ["hello_world"]


Components can choose to define their
:attr:`functions<helix.component.Component.functions>`,
:attr:`calls<helix.component.Component.calls>`, and
:attr:`globals<helix.component.Component.globals>` properties inside of a
:meth:`generate<helix.component.Component.generate>` method. This method is run
after configuration parameters are parsed and these parameters are available in
the :attr:`configuration<helix.component.Component.configuration>` property as
a dict and can be used in the
:meth:`generate<helix.component.Component.generate>` method as above.

Reinstall the Python package (if not installed in editable mode) and then
create a new HELIX build, supplying the new configuration parameter:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example -c example-component:message="goodbye world"

Run the generated artifact binary - it should now print "goodbye world" and
exit.

Using External Template Files
*****************************

Once a Component becomes relatively complex, it can be a good idea to move the
templated function code belonging to the Component into its own file so that it
is easier to track changes and so that syntax highlighting can be enabled for
ease of development. HELIX includes a couple of utilities to help you do that.
In this section, we'll move the source code for our ``ExampleComponent`` to an
external ``example.c`` file.

To start, we'll need to configure our Python package so that it includes
non-python files when it is compressed into its distributable form. To do this,
add a file named ``MANIFEST.in`` to the root of your python package with the
following contents:

.. code-block:: bash

    # MANIFEST.in

    recursive-include helix_example *.c

This tells the Python package manager that any files with the extension ``.c``
should be included with the package.

Next, write create a file in the same directory as ``example.py`` called
``example.c``. The package directory structure should look like:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── components/
    │   │   ├── example.py
    │   │   ├── example.c
    │   │   ├── __init__.py
    │   ├── __init__.py
    └── setup.py

Add the following content to ``example.c``:

.. code-block:: cpp

    // example.c

    #include <stdio.h>

    void ${hello_world}() {
        printf("${message}\n");
    }

Finally, modify the ``ExampleComponent`` class in ``example.py`` as follows:

.. code-block:: python

    # example.py

    class ExampleComponent(component.Component):
        ...

        # The following lines may be removed:

        # TEMPLATE = r"""
        #     #include <stdio.h>
        #
        #     void ${hello_world}() {
        #         printf("${message}\n");
        #     }
        # """

        def generate(self):
            ...

            template = utils.source(__name__, "example.c")

            ...

            function = utils.substitute(template, message=formatted)

            ...

We make use of the :meth:`source<helix.utils.source>` function here to fetch
the source of the included template file, relative to the current package path.

You can now reinstall the package (if not installed in editable mode) and test
these Component changes. The Component should function exactly the same, but
the Python package is now a bit more maintainable.

.. _adding-dependencies:

Adding Dependencies
*******************

HELIX includes a dependency installation/management system for Blueprints,
Components, and Transforms for managing external dependencies that cannot be
installed with ``pip``. Lets add a simple ``apt`` dependency to our Component -
``cowsay`` to improve the visual output of our printed message.

.. note:: From here on, this tutorial only works on a Linux platform. There are
    dependency types defined for Windows, however, and you can find examples of
    their use in HELIX source.

Add the following to the ``ExampleComponent`` class:

.. code-block:: python

    # example.py

    from helix import utils

    ...

    class ExampleComponent(component.Component):
        ...

        dependencies = [utils.LinuxAPTDependency("cowsay")]

        ...

        def generate(self):
            ...

            cowsay = utils.find("cowsay")
            output, _ = utils.run(
                "{} {}".format(cowsay, self.configuration["message"]), cwd="./"
            )
            formatted = repr(output.decode("utf-8")).replace("'", "")

            ...

            function = utils.substitute(template, message=formatted)

Reinstall the Python package (if not in editable mode) and install dependencies
for our Component:

.. code-block:: bash

    helix install components example-component


.. note:: You may need to run the above command as root/Administrator to
    successfully install dependencies.

Finally, build the ``cmake-cpp`` Blueprint again with our updated Component:

.. code-block:: bash

    helix build blueprint cmake-cpp ./example -c example-component

You should now get an output similar to the following when running the
generated artifact binary:

.. code-block::

     _____________
    < hello world >
     -------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||

.. note:: It's worth noting here that the binary generated by HELIX in this
    example does not actually make use of ``cowsay``. Instead, ``cowsay`` is
    invoked during configuration of the Component, and the ``cowsay`` string is
    injected into the generated source code. A more advanced approach, left as
    an exercise for the reader, would be to invoke ``cowsay`` from the
    generated artifact instead (e.g., with a Linux ``system`` call written in
    C/C++).

.. _testing-the-component:

Testing the Component
*********************

HELIX includes some minimal utilities for testing Components with the
``unittest`` framework. To write a unit test for our Component, add the
following to the ``example.py`` module:

.. code-block:: python

    # example.py

    from helix import tests

    ...

    class ExampleComponentTests(tests.UnitTestCase, tests.ComponentTestCaseMixin):
        blueprint = "cmake-cpp"
        component = "example-component"

This will create a couple of simple unit tests from
:class:`TestCaseMixin<helix.tests.ComponentTestCaseMixin>`.

.. note:: When developing Components, at a minimum it is recommended to define
    the simple testing class above. This will introduce simple build tests as
    well as a test that ensures that your Component's templated globals are
    configured correctly (for more details, see
    :class:`TestCaseMixin<helix.tests.ComponentTestCaseMixin>`).

To register this unit test with HELIX, add an entrypoint to the ``helix.tests``
group in the Python package's ``setup.py`` as follows:

.. code-block:: python

    # setup.py

    ...
    entry_points={
        ...
        "helix.tests": [
            "example-component = helix_example.components.example:ExampleComponentTests"
        ],
        ...
    },
    ...

Finally, to run unit tests for Blueprints, Components, and Transforms, run:

.. code-block:: bash

    helix test unit
