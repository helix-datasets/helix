Developing a New Blueprint
--------------------------

Blueprints are at the core of how HELIX generates a build. A properly written
Blueprint is generic, reusable, and flexible - designed to work well with many
or few Components in many different configurations. Good Blueprints do not
define program behavior other than some minimal control flow to set up
callsites - that is left to the Components integrated with a Blueprint in a
build.

Most developers will not need to write a Blueprint for HELIX - making use of
the existing Blueprints built in to HELIX is sufficient for most usecases.
However, HELIX is flexible enough to support practically any programming
language and any build system - developers simply need to write a Blueprint for
their target platform. To demonstrate this, this tutorial will guide you
through the process of writing a new Blueprint to support Python.

Prior to following this tutorial, you'll need to have a python package set up
to extend HELIX (see :ref:`building-a-python-package`).

Writing the Blueprint
*********************

Similar to Components and Transforms, Blueprints are simply Python classes that
implement the :class:`Blueprint<helix.blueprint.Blueprint>` interface.

Let's start by adding a ``blueprints`` directory to our Python package with a
``python`` module for our new Blueprint. The package directory structure should
look like the following:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── blueprints/
    │   │   ├── python.py
    │   │   ├── __init__.py
    │   ├── __init__.py
    └── setup.py 

Inside of ``python.py`` we'll create a simple Blueprint by subclassing
:class:`Blueprint<helix.blueprint.Blueprint>`:

.. code-block:: python

    # python.py

    import os

    from helix import blueprint
    from helix import utils


    class ExamplePythonBlueprint(blueprint.Blueprint):
        """An example Python blueprint."""
    
        name = "example-python"
        verbose_name = "Example Python Blueprint"
        type = "python"
        version = "1.0.0"
        description = "A simple Python blueprint"
    
        CALLSITE_STARTUP = "startup"
        """Called at program startup.
    
        Calls at this callsite are called once and expected to return.
        """
    
        callsites = [CALLSITE_STARTUP]
    
        TEMPLATE = """${functions}
    
    if __name__ == "__main__":
        ${startup}
    """
    
        def filename(self, directory):
            """Generate a build file name in the given directory.
    
            Args:
                directory (str): The path to the build directory.
    
            Returns:
                The file path of the build file.
            """
    
            return os.path.join(directory, "{}.py".format(self.build_name))
    
        def generate(self, directory):
            functions = "\n".join(self.functions)
    
            startup = self.calls.pop(self.CALLSITE_STARTUP, [])
            startup = "\n    ".join(startup) or "pass"
    
            source = utils.substitute(self.TEMPLATE, functions=functions, startup=startup)
    
            with open(self.filename(directory), "w") as f:
                f.write(source)
    
        def compile(self, directory, options):
            """Nothing to do here.
    
            Python is an interpreted language, so we don't really need to do
            anything in the ``compile()`` step. We still need to pass the build
            artifacts to the output, however.
            """
    
            return [self.filename(directory)]

Blueprints have three main components:

1. A set of :attr:`callsites<helix.blueprint.Blueprint.callsites>` - where
components may register calls to functions that they define.

2. A :meth:`generate<helix.blueprint.Blueprint.generate>` method which
generates source code from the collection of Components provided, using the
:attr:`functions<helix.blueprint.Blueprint.functions>` and
:attr:`calls<helix.blueprint.Blueprint.calls>` properties of the Blueprint
class. These properties aggregate functions and calls provided by all of the
included Components. Source code is written to the given directory path and a
list of source files is returned.

3. A :meth:`compile<helix.blueprint.Blueprint.compile>` method which compiles
the given directory of source files and returns a list of build artifacts. In
this case, since Python is not compiled, this simply returns the path to the
generated Python file.

This simple Python Blueprint defines a single callsite called ``startup`` and
generates a single python file in the target directory with all included
functions and calls to ``startup`` functions in ``__main__``.

Note that the Blueprint does not need to be concerned with how or when
Transforms are applied. HELIX will apply Transforms automatically during build
based on their type - Blueprints simply need to know how to generate valid
source code from Components and compile that source code into build artifacts.

.. note:: It's generally good practice to define callsite names as constants on
    the Blueprint class for easier use by Components (e.g., ``CALLSITE_STARTUP``).

Registering the Blueprint
*************************

Similar to Components and Transforms, Blueprints must be added to the
entrypoint group ``helix.blueprints`` in our Python package's ``setup.py``.
Make the following change to ``setup.py``:

.. code-block:: python

    # setup.py

    ...
    entry_points={
        ...
        "helix.blueprints": [
            "example-python = helix_example.blueprints.python:ExamplePythonBlueprint"
        ]
        ...
    }
    ...

.. note:: Similar to Components and Transforms, the ``name`` property of our
    new Blueprint *must* match the name of the entrypoint.

To update the entrypoint list, reinstall the Python package (even if you
installed it in editable mode):

.. code-block:: bash

    pip install .

Check that our new Blueprint is registered with the HELIX CLI:

.. code-block:: bash

    Available Blueprints
        ...
        Example Python Blueprint (1.0.0) [example-python]
        ...

Finally, build an empty ``example-python`` Blueprint to make sure that it
works:

.. code-block:: bash

    helix build blueprint example-python ./example

Take a look at the generated Python script - it's not particularly interesting
right now but we'll add a Component for our new Blueprint next.

Writing a Component for the Blueprint
*************************************

Let's create a minimal Component to test our new Blueprint in much the same way
we created our first Component in :ref:`writing-your-first-component`.

First, let's add a new module to the ``components`` directory of our Python
package called ``python`` to house our new Component. The package directory
structure should look like the following:

.. code-block:: bash

    .
    ├── helix_example/
    │   ├── components/
    │   │   ├── example.py
    │   │   ├── python.py
    │   │   ├── __init__.py
    │   ├── __init__.py
    └── setup.py 

Inside of ``python.py`` we'll create a simple Component:

.. code-block:: python

    # python.py

    from helix import component
    
    
    class ExamplePythonComponent(component.Component):
        """An example Python component."""
    
        name = "example-python-component"
        verbose_name = "Example Python Component"
        type = "example"
        version = "1.0.0"
        description = "An example Python component"
        date = "2020-10-20 12:00:00.000000"
        tags = (("group", "example"),)
    
        blueprints = ["example-python"]
    
        functions = [
            """def ${example}():
        print("hello world")
    """
        ]
        calls = {"startup": ["${example}()"]}
        globals = ["example"]

This is a very simple Component that defines one function that prints "hello
world" and registers a call to it at the ``startup`` callsite.

Next, we need to register the new Component with the ``helix.components``
entrypoint group. Make the following change to ``setup.py``:

.. code-block:: python

    # setup.py

    ...
    entry_points={
        ...
        "helix.components": [
            ...
            "example-python-component = helix_example.components.python:ExamplePythonComponent",
            ...
        ]
        ...
    }
    ...

To update the entrypoint list, resintall the Python package (even if you
installed it in editable mode):

.. code-block:: bash

    pip install .

Check that the new Component is registerd with the HELIX CLI:

.. code-block:: bash

    helix list

The output should include the new Component:

.. code-block:: bash

    Available Components:
        ...
        Example Python Component (1.0.0) [example-python-component]
        ...

Now we can test our new Blueprint with the new Component:

.. code-block:: bash
    
    helix build blueprint example-python ./example -c example-python-component

The generated Python script should simply print "hello world" and exit.

Adding Another Callsite
***********************

Blueprints are not limited to exposing only a single, trivial callsite.
Blueprints can evoke very sophistocated behavior from their Components by
exposing multiple different types of callsites. To demonstrate this, let's add
another callsite to our Blueprint called ``loop`` which is called repeatedly
inside of a loop defined in the Blueprint.

Make the following changes to the Blueprint:

.. code-block:: python

    # blueprints/python.py

    ...

    Class ExamplePythonBlueprint(blueprint.Blueprint):
        ...

        CALLSITE_LOOP = "loop"
        """Called every five seconds, indefinitely.

        Calls this callsite repeatedly, inside of a loop, until the program is
        terminated.
        """

        callsites = [CALLSITE_STARTUP, CALLSITE_LOOP]

        ...

        TEMPLATE = """import time

    ${functions}

    if __name__ == "__main__":
        ${startup}

        while True:
            ${loop}

            time.sleep(5)
    """

    def generate(self, directory):
        ...

        loop = self.calls.pop(self.CALLSITE_LOOP, [])
        loop = "\n        ".join(loop) or "break"

        ...

        source = utils.substitute(
            self.TEMPLATE, functions=functions, startup=startup, loop=loop
        )

        ...

Note that we've chosen to set the ``loop`` template parameter to ``break`` if
no calls are registered at that callsite. This makes our Blueprint more
flexible - if no calls are registered for the ``loop`` callsite the Blueprint
will simply break out of its infinte loop.

Next, let's update the simple testing Component for this Blueprint to make use
of the new callsite. Make the following changes to the Component:

.. code-block:: python

    # components/python.py

    ...

    class ExamplePythonComponent(component.Component):
        ...

        functions = [
            ...
            """from datetime import datetime

    def ${now}():
        print(datetime.now())
    """,
            ...
        ]

        ...

        calls = {
            ...
            "loop": ["${now}()"],
            ...
        }
        
        ...

        globals = ["example", "now"]

This adds a single function which prints the current date and time and adds a
call at the ``loop`` callsite to that new function.

After reinstalling the python package (if not installed in editable mode), we
can now create a new build with our updated Blueprint and Component:

.. code-block:: bash
    
    helix build blueprint example-python ./example -c example-python-component

You should now have a Python script that prints "hello world" once and then
repeatedly prints the current time every five seconds indefinitely.

.. note:: **Blueprint Flexibility**: When developing new Blueprints, it can be
    tempting to add a lot of project structure and even some core program
    functionality to Blueprints by implementing various callsites. A best practice
    is to limit the functionality inside of a Blueprint to only control flow and
    ensure that all callsites are optional. Remember: callsites must be able to
    support *zero or more* calls from components. A generic Blueprint is a reusble
    Blueprint.

Adding Dependencies
*******************

Specifying Blueprint dependencies can be done in the same way as specifying
Component dependencies (see :ref:`adding-dependencies`).

Testing the Blueprint
*********************

Writing unit tests for Transforms can be done in the same way as writing unit
tests for Components (see :ref:`testing-the-component`).
