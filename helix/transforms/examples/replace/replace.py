import os

from .... import utils
from .... import tests
from .... import transform
from .... import exceptions


class ReplaceExampleTransform(transform.Transform):
    """An example source transform that replaces text

    This also demonstrates a transform that requires configuration.
    """

    name = "replace-example"
    verbose_name = "Replace Example"
    type = transform.Transform.TYPE_SOURCE
    version = "1.0.0"
    description = "An example source transform that replaces text"

    options = {"old": {}, "new": {}}

    def transform(self, source, destination):
        """Replace configured strings."""

        if not self.configured:
            raise exceptions.NotConfigured(
                "cannot apply this transform without configuration (hint: did you remember to call ``configure``?)"
            )

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)

        with open(source, "r") as f:
            data = f.read()

        data = data.replace(self.configuration["old"], self.configuration["new"])

        with open(destination, "w") as f:
            f.write(data)


class ReplaceExampleTransformTests(tests.UnitTestCase, tests.TransformTestCaseMixin):
    blueprint = "cmake-cpp"
    transform = "replace-example"

    configuration = {"old": "hello", "new": "goodbye"}

    def test_transform_successful_rewrite(self):
        artifacts, _ = self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [
                    {
                        "name": "configuration-example",
                        "configuration": {"second_word": "world"},
                    }
                ],
                "transforms": [
                    {"name": self.transform, "configuration": self.configuration}
                ],
            }
        )

        output, _ = utils.run(artifacts[0], self.working)

        self.assertNotIn(b"hello", output)
        self.assertIn(b"goodbye", output)
