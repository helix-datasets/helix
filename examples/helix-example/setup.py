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
        "helix.blueprints": [
            "example-python = helix_example.blueprints.python:ExamplePythonBlueprint"
        ],
        "helix.components": [
            "example-component = helix_example.components.example:ExampleComponent",
            "example-python-component = helix_example.components.python:ExamplePythonComponent",
        ],
        "helix.transforms": [
            "example-transform = helix_example.transforms.example:ExampleTransform"
        ],
        "helix.tests": [
            "example-component = helix_example.components.example:ExampleComponentTests"
        ],
    },
)
