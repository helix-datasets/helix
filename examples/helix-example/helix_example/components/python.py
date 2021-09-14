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
""",
        """from datetime import datetime

def ${now}():
    print(datetime.now())
""",
    ]
    calls = {"startup": ["${example}()"], "loop": ["${now}()"]}
    globals = ["example", "now"]
