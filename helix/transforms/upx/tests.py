import os
import unittest

from ... import tests
from ... import exceptions


class UPXTests(tests.UnitTestCase):
    blueprint = "cmake-cpp"
    transform = "upx"

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_build_too_small_fails(self):
        with self.assertRaises(exceptions.BuildFailure) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [],
                    "transforms": [{"name": self.transform}],
                }
            )

        self.assertIn("unsupported", str(error.exception))
