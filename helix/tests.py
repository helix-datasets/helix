import os
import abc
import ctypes
import shutil
import tempfile
import unittest

from . import blueprint
from . import component
from . import transform
from . import build
from . import utils
from . import exceptions


class UnitTestCase(unittest.TestCase):
    """The base class for all Blueprint, Component, and Transform tests.

    Provides utilities for safely generating builds during unit tests.
    """

    def setUp(self):
        self.working = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.working)

    def build(self, configuration):
        """Build a given configuration in the current working directory.

        Tests may make use of the build artifacts to determine success/failure
        by using ``utils.run`` as necessary.

        Args:
            configuration: A build configuration dictionary.

        Returns:
            A list of build artifacts from the successful build.
        """

        return build.build(configuration, self.working)


class BlueprintTestCaseMixin(object, metaclass=abc.ABCMeta):
    """Provides testing utilities and minimal tests for Blueprints.

    Note:
        Requires a base class of ``UnitTestCase``.
    """

    @property
    @abc.abstractmethod
    def blueprint(self):
        """The Blueprint name."""

        return ""

    def test_build_success(self):
        """Tests that this Blueprint builds successfully.

        Builds this Blueprint on its own with no Components or Transforms. As
        long as no errors are raised in building, this test will pass.
        """

        self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [],
                "transforms": [],
            }
        )


class ComponentTestCaseMixin(object, metaclass=abc.ABCMeta):
    """Provides testing utilities and minimal tests for Components.

    Note:
        Requires a base class of ``UnitTestCase``.
    """

    @property
    @abc.abstractmethod
    def blueprint(self):
        """The Blueprint that this Component should be built with."""

        return ""

    @property
    @abc.abstractmethod
    def component(self):
        """The Component name."""

        return ""

    configuration = {}
    """Optional configuration parameters for building.

    If the Component requires configuration for a basic build, specify an
    example configuration here.
    """

    def test_build_success(self):
        """Tests that this Component builds successfully.

        Builds this Component on its own with the configured Blueprint and
        nothing else. As long as no errors are raised in building, this test
        will pass.
        """

        self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [
                    {"name": self.component, "configuration": self.configuration}
                ],
                "transforms": [],
            }
        )

    def test_duplicate_build(self):
        """Tests that duplicating this Component builds successfully.

        Attempts a minimal build with only this Component, duplicated.
        This is a useful test to determine if the Component has been
        parameterized successfully. If not, the build will likely fail with
        errors complaining about duplicated functions or globals.
        """

        self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [
                    {"name": self.component, "configuration": self.configuration},
                    {"name": self.component, "configuration": self.configuration},
                ],
                "transforms": [],
            }
        )


class TransformTestCaseMixin(object, metaclass=abc.ABCMeta):
    """Provides testing utilities and minimal tests for Transforms.

    Note:
        Requires a base class of ``UnitTestCase``.
    """

    @property
    @abc.abstractmethod
    def blueprint(self):
        """The Blueprint that this Transform should be built with."""

        return ""

    @property
    @abc.abstractmethod
    def transform(self):
        """The Transform name."""

        return ""

    configuration = {}
    """Optional configuration parameters for building.

    If the Transform requires configuration for a basic build, specify an
    example configuration here.
    """

    def test_build_success(self):
        """Tests that this Transform builds successfully.

        Builds this Transform on its own with the configured Blueprint and
        nothing else. As long as no errors are raised in building, this test
        will pass.
        """

        self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [],
                "transforms": [
                    {"name": self.transform, "configuration": self.configuration}
                ],
            }
        )


class ConfigurationTests(unittest.TestCase):
    """Test the configuration specification system."""

    def test_simple_configuration(self):
        class Test(utils.Configurable):
            options = {"test": {}}

        test = Test()
        test.configure(test="value")

        self.assertTrue(hasattr(test, "configuration"))
        self.assertEqual(test.configuration["test"], "value")
        self.assertTrue(hasattr(test, "configured"))
        self.assertTrue(test.configured)

    def test_required_configuration_parameter(self):
        class Test(utils.Configurable):
            options = {"test": {}}

        test = Test()

        with self.assertRaises(exceptions.ConfigurationError):
            test.configure()

        self.assertFalse(test.configured)

    def test_configuration_parameter_default(self):
        class Test(utils.Configurable):
            options = {"test": {"default": "value"}}

        test = Test()
        test.configure()

        self.assertEqual(test.configuration["test"], "value")

    def test_unconfigured_configuration_access(self):
        class Test(utils.Configurable):
            options = {"test": {}}

        test = Test()

        with self.assertRaises(exceptions.NotConfigured):
            test.configuration


class DependencyTests(unittest.TestCase):
    """Test the dependency specification/installation system."""

    class InstallableDependency(utils.Dependency):
        _installed = False

        def install(self, verbose=False):
            self._installed = True

        def installed(self):
            return self._installed

    class InstalledDependency(InstallableDependency):
        _installed = True

    def test_single_installed_dependency(self):
        class Test(utils.Dependable):
            dependencies = [self.InstalledDependency()]

        self.assertTrue(Test.installed())
        Test()

    def test_single_uninstalled_dependency_init(self):
        class Test(utils.Dependable):
            dependencies = [self.InstallableDependency()]

        self.assertFalse(Test.installed())

        with self.assertRaises(exceptions.NotInstalled):
            Test()

    def test_single_uninstalled_dependency_install(self):
        class Test(utils.Dependable):
            dependencies = [self.InstallableDependency()]

        self.assertFalse(Test.installed())
        Test.install()
        self.assertTrue(Test.installed())

    def test_multiple_mixed_installation_status_dependencies_init(self):
        class Test(utils.Dependable):
            dependencies = [self.InstalledDependency(), self.InstallableDependency()]

        self.assertFalse(Test.installed())

        with self.assertRaises(exceptions.NotInstalled):
            Test()

    def test_multiple_uninstalled_dependencies_install(self):
        class Test(utils.Dependable):
            dependencies = [self.InstallableDependency(), self.InstallableDependency()]

        self.assertFalse(Test.installed())
        Test.install()
        self.assertTrue(Test.installed())

    def test_manual_path_dependency(self):
        class Test(utils.Dependable):
            dependencies = [
                utils.ManualPATHDependency(name="not-a-valid-binary", help="test")
            ]

        self.assertFalse(Test.installed())

        with self.assertRaises(exceptions.DependencyInstallationFailure):
            Test.install()

    @unittest.skipUnless(os.name == "nt", "test not supported on this platform")
    def test_manual_windows_registry_dependency(self):
        import winreg

        class Test(utils.Dependable):
            dependencies = [
                utils.ManualWindowsRegistryDependency(
                    "test",
                    help="test",
                    registry=winreg.HKEY_LOCAL_MACHINE,
                    key=r"SOFTWARE\Microsoft\Windows",
                )
            ]

        self.assertTrue(Test.installed())

    @unittest.skipUnless(os.name == "nt", "test not supported on this platform")
    def test_windows_chocolatey_dependency_installed(self):
        class Test(utils.Dependable):
            dependencies = [utils.WindowsChocolateyDependency("chocolatey")]

        self.assertTrue(Test.installed())

    @unittest.skipUnless(os.name == "nt", "test not supported on this platform")
    def test_windows_chocolatey_dependency_invalid(self):
        class Test(utils.Dependable):
            dependencies = [utils.WindowsChocolateyDependency("not-a-valid-package")]

        self.assertFalse(Test.installed())

    @unittest.skipUnless(
        os.name == "nt" and ctypes.windll.shell32.IsUserAnAdmin(),
        "test only supported on Windows and when running as an Admin",
    )
    def test_windows_chocolatey_dependency_install(self):
        class Test(utils.Dependable):
            dependencies = [utils.WindowsChocolateyDependency("chocolatey")]

        Test.install()

    @unittest.skipUnless(
        os.name == "nt" and ctypes.windll.shell32.IsUserAnAdmin(),
        "test only supported on Windows and when running as an Admin",
    )
    def test_windows_chocolatey_dependency_install_invalid(self):
        class Test(utils.Dependable):
            dependencies = [utils.WindowsChocolateyDependency("not-a-valid-package")]

        with self.assertRaises(exceptions.DependencyInstallationFailure):
            Test.install()

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_linux_apt_dependency_installed(self):
        class Test(utils.Dependable):
            dependencies = [utils.LinuxAPTDependency("apt")]

        self.assertTrue(Test.installed())

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_linux_apt_dependency_invalid(self):
        class Test(utils.Dependable):
            dependencies = [utils.LinuxAPTDependency("not-a-valid-package")]

        self.assertFalse(Test.installed())

    @unittest.skipUnless(
        os.name == "posix" and os.getuid() == 0,
        "test only supported on Linux and when running as root",
    )
    def test_linux_apt_dependency_install(self):
        class Test(utils.Dependable):
            dependencies = [utils.LinuxAPTDependency("apt")]

        Test.install()

    @unittest.skipUnless(
        os.name == "posix" and os.getuid() == 0,
        "test only supported on Linux and when running as root",
    )
    def test_linux_apt_dependency_install_invalid(self):
        class Test(utils.Dependable):
            dependencies = [utils.LinuxAPTDependency("not-a-valid-package")]

        with self.assertRaises(exceptions.DependencyInstallationFailure):
            Test.install()


class UtilityTests(unittest.TestCase):
    """Test various utility methods."""

    def test_substitute_simple(self):
        template = "${test}"

        result = utils.substitute(template, test="value")

        self.assertEqual(result, "value")

    def test_substitute_missing_parameter(self):
        template = "${test}-${value}"

        result = utils.substitute(template, test="value")

        self.assertEqual(result, "value-${value}")

    def test_substitute_unsafe_missing_parameter(self):
        template = "${test}-${value}"

        with self.assertRaises(KeyError):
            utils.substitute(template, safe=False, test="value")

    def test_substitute_extra_parameter(self):
        template = "test"

        result = utils.substitute(template, test="value")

        self.assertEqual(result, "test")

    def test_substitute_unsafe_invalid_template(self):
        template = "${test"

        with self.assertRaises(ValueError):
            utils.substitute(template, safe=False, test="value")

    def test_substitute_invalid_template(self):
        template = "${test"

        with self.assertRaises(ValueError):
            utils.substitute(template, test="value")

    def test_find_environment(self):
        env = "TEST_BINARY_PATH"
        path = tempfile.NamedTemporaryFile()

        os.environ[env] = path.name

        result = utils.find("test-binary", environment=env)

        self.assertEqual(result, path.name)

    def test_find_path(self):
        result = utils.find("python")

        self.assertIsNotNone(result)

    def test_find_guess(self):
        path = tempfile.NamedTemporaryFile()

        result = utils.find("test-binary", guess=[path.name])

        self.assertEqual(result, path.name)

    def test_find_does_not_exist(self):
        result = utils.find("test-binary")

        self.assertIsNone(result)

    def test_find_quotes(self):
        path = tempfile.NamedTemporaryFile(prefix="test binary")

        result = utils.find("test-binary", guess=[path.name])

        self.assertEqual(result, '"{}"'.format(path.name))

    def test_find_priority(self):
        env = "TEST_BINARY_PATH"
        guess = tempfile.NamedTemporaryFile()
        environment = tempfile.NamedTemporaryFile()

        os.environ[env] = environment.name

        result = utils.find("test-binary", environment=env, guess=[guess.name])

        self.assertEqual(result, environment.name)

    def test_simple_specification_parse(self):
        specification = "name:parameter=value"

        result = utils.parse(specification)

        self.assertEqual(result["name"], "name")
        self.assertIn("parameter", result["configuration"].keys())
        self.assertEqual(result["configuration"]["parameter"], "value")
        self.assertEqual(len(result["configuration"]), 1)

    def test_specification_parse_mutliple_parameters(self):
        specification = "name:parameter=value,other=second"

        result = utils.parse(specification)

        self.assertIn("parameter", result["configuration"].keys())
        self.assertEqual(result["configuration"]["parameter"], "value")
        self.assertIn("other", result["configuration"].keys())
        self.assertEqual(result["configuration"]["other"], "second")
        self.assertEqual(len(result["configuration"]), 2)

    def test_specification_parse_quotes(self):
        specification = "name:parameter='first value',other=\"second value\""

        result = utils.parse(specification)

        self.assertIn("parameter", result["configuration"].keys())
        self.assertEqual(result["configuration"]["parameter"], "first value")
        self.assertIn("other", result["configuration"].keys())
        self.assertEqual(result["configuration"]["other"], "second value")
        self.assertEqual(len(result["configuration"]), 2)

    def test_specification_parse_name_only(self):
        specification = "name"

        result = utils.parse(specification)
        self.assertEqual(result["name"], "name")
        self.assertEqual(result["configuration"], {})


class TestComponent(component.Component):
    name = "test"
    verbose_name = "Test"
    description = "test"
    version = "0.1.0"
    date = "2000-01-01 12:00:00.00"
    type = "test"

    tags = (("test", "component-test"),)

    blueprints = ["test"]

    options = {"test": {"default": "test"}}

    TEMPLATE = "${global}-${test}"

    def generate(self):
        content = utils.substitute(self.TEMPLATE, **self.configuration)

        self.functions = [content]
        self.calls = {"test": ["${global}"]}
        self.globals = ["global"]


class ComponentTests(unittest.TestCase):
    """Test core component functionality."""

    def test_successful_finalize(self):
        test = TestComponent()

        test.configure()
        test.generate()
        test.finalize()

        self.assertIsNotNone(test.functions)
        self.assertIsNotNone(test.calls)

    def test_finalize_before_generate(self):
        test = TestComponent()

        with self.assertRaises(exceptions.NotConfigured):
            test.finalize()

    def test_finalize_uniqueness(self):
        first = TestComponent()

        first.configure()
        first.generate()
        first.finalize()

        second = TestComponent()

        second.configure()
        second.generate()
        second.finalize()

        self.assertNotEqual(first.functions[0], second.functions[0])
        self.assertNotEqual(first.calls["test"][0], second.calls["test"][0])

    def test_finalize_complete_substitute(self):
        first = TestComponent()

        first.configure()
        first.generate()
        first.finalize()

        self.assertNotIn("$", first.functions[0])
        self.assertNotIn("$", first.calls["test"][0])


class TestTransform(transform.Transform):
    name = "test"
    verbose_name = "Test"
    description = "test"
    version = "0.1.0"
    type = transform.Transform.TYPE_SOURCE

    tags = (("test", "transform-test"),)

    options = {"test": {"default": "test"}}

    def transform(self, source, destination):
        pass


class TransformTests(unittest.TestCase):
    """Test core transform functionality.

    The transform interface is not currently sufficiently complicated to
    require unit testing - but if/when they it is, this is where they should
    go.
    """

    pass


class TestBlueprint(blueprint.Blueprint):
    name = "test"
    verbose_name = "Test"
    description = "test"
    version = "0.1.0"
    type = "test"

    CALLSITE_TEST = "test"

    callsites = [CALLSITE_TEST]

    def generate(self, output):
        return []

    def compile(self, directory, options):
        return []


class BlueprintTests(unittest.TestCase):
    """Test core blueprint functionality."""

    def test_unconfigured_component(self):
        component = TestComponent()

        transform = TestTransform()
        transform.configure()

        with self.assertRaises(exceptions.BlueprintNotSane):
            TestBlueprint("test", components=[component], transforms=[transform])

    def test_unconfigured_blueprint(self):
        component = TestComponent()
        component.configure()

        transform = TestTransform()

        with self.assertRaises(exceptions.BlueprintNotSane):
            TestBlueprint("test", components=[component], transforms=[transform])

    def test_tag_aggregation(self):
        component = TestComponent()
        component.configure()
        component.generate()
        component.finalize()

        transform = TestTransform()
        transform.configure()

        blueprint = TestBlueprint(
            "test", components=[component], transforms=[transform]
        )

        for tag in component.tags:
            self.assertIn(tag, blueprint.tags)

        for tag in transform.tags:
            self.assertIn(tag, blueprint.tags)

    def test_unsupported_component(self):
        class UnsupportedComponent(TestComponent):
            blueprints = ["none"]

        component = UnsupportedComponent()
        component.configure()
        component.generate()
        component.finalize()

        with self.assertRaises(exceptions.BlueprintNotSane):
            TestBlueprint("test", components=[component])

    def test_duplicate_components(self):
        first = TestComponent()
        first.configure()
        first.generate()
        first.finalize()

        second = TestComponent()
        second.configure()
        second.generate()
        second.finalize()

        blueprint = TestBlueprint("test", components=[first, second])

        self.assertIn(first, blueprint.components)
        self.assertIn(second, blueprint.components)

    def test_duplicate_finalized_components(self):
        first = TestComponent()
        first.configure()
        first.generate()
        first.finalize()

        with self.assertRaises(exceptions.BlueprintNotSane):
            TestBlueprint("test", components=[first, first])

    def test_duplicate_transforms(self):
        """Duplicate transforms are supported.

        It's possible to imagine a transform that could be applied multiple
        times consecutively. Duplicate transform instances should be supported
        too but we won't test that.
        """

        component = TestComponent()
        component.configure()
        component.generate()
        component.finalize()

        first = TestTransform()
        first.configure()

        second = TestTransform()
        second.configure()

        blueprint = TestBlueprint(
            "test", components=[component], transforms=[first, second]
        )

        self.assertIn(first, blueprint.transforms)
        self.assertIn(second, blueprint.transforms)

    def test_function_aggregation(self):
        first = TestComponent()
        first.configure()
        first.generate()
        first.finalize()

        second = TestComponent()
        second.configure()
        second.generate()
        second.finalize()

        blueprint = TestBlueprint("test", components=[first, second])

        self.assertIn(first.functions[0], blueprint.functions)
        self.assertIn(second.functions[0], blueprint.functions)

    def test_call_aggregation(self):
        first = TestComponent()
        first.configure()
        first.generate()
        first.finalize()

        second = TestComponent()
        second.configure()
        second.generate()
        second.finalize()

        blueprint = TestBlueprint("test", components=[first, second])

        self.assertIn(first.calls["test"][0], blueprint.calls["test"])
        self.assertIn(second.calls["test"][0], blueprint.calls["test"])

    def test_unsupported_callsite(self):
        class UnsupportedCallsiteComponent(TestComponent):
            def generate(self):
                super().generate()
                self.calls["unsupported"] = ["test"]

        component = UnsupportedCallsiteComponent()
        component.configure()
        component.generate()
        component.finalize()

        with self.assertRaises(exceptions.BlueprintNotSane):
            TestBlueprint("test", components=[component])

    def test_unsupported_transform(self):
        class UnsupportedSourceTransform(TestTransform):
            type = transform.Transform.TYPE_SOURCE

            def supported(self, target):
                return False

        t = UnsupportedSourceTransform()
        t.configure()

        blueprint = TestBlueprint("test", transforms=[t])

        with self.assertRaises(exceptions.BuildFailure):
            blueprint.transform(transform.Transform.TYPE_SOURCE, ["test"])


class BuildTests(unittest.TestCase):
    """Test the build-from-configuration system.

    This mostly consists of testing that particular build configurations either
    build successfully or fail - other testing should be a part of more focused
    unit tests.
    """

    def test_minimal_build(self):
        configuration = {
            "name": "test",
            "blueprint": {"class": TestBlueprint},
            "components": [],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        artifacts, tags = build.build(configuration, working.name)

        self.assertIsNotNone(artifacts)

    def test_example_build(self):
        configuration = {
            "name": "example",
            "blueprint": {"class": TestBlueprint},
            "components": [
                {"class": TestComponent, "configuration": {}},
                {
                    "class": TestComponent,
                    "configuration": {"test": "example"},
                },
            ],
            "transforms": [
                {
                    "class": TestTransform,
                    "configuration": {"test": "value"},
                },
            ],
        }

        working = tempfile.TemporaryDirectory()

        artifacts, tags = build.build(configuration, working.name)

        self.assertIsNotNone(artifacts)

    def test_missing_name(self):
        configuration = {
            "blueprint": {"class": TestBlueprint},
            "components": [],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_missing_blueprint(self):
        configuration = {"name": "test", "components": [], "transforms": []}

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_missing_components(self):
        configuration = {
            "name": "test",
            "blueprint": {"class": TestBlueprint},
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_missing_transforms(self):
        configuration = {
            "name": "test",
            "blueprint": {"class": TestBlueprint},
            "components": [],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_missing_configuration(self):
        configuration = {
            "name": "example",
            "blueprint": {"class": TestBlueprint},
            "components": [
                {
                    "class": TestComponent,
                },
            ],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        artifacts, tags = build.build(configuration, working.name)

        self.assertIsNotNone(artifacts)

    def test_malformed_component(self):
        configuration = {
            "name": "test",
            "blueprint": {"class": TestBlueprint},
            "components": [{"test": "test"}],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_malformed_transform(self):
        configuration = {
            "name": "test",
            "blueprint": {"class": TestBlueprint},
            "components": [],
            "transforms": [{"test": "test"}],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.ConfigurationError):
            build.build(configuration, working.name)

    def test_specification_by_both_name_and_class(self):
        configuration = {
            "name": "example",
            "blueprint": {"class": TestBlueprint},
            "components": [{"name": "invalid-component", "class": TestComponent}],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        artifacts, tags = build.build(configuration, working.name)

        self.assertIsNotNone(artifacts)

    def test_specification_invalid_name(self):
        configuration = {
            "name": "example",
            "blueprint": {"class": TestBlueprint},
            "components": [{"name": "invalid-component"}],
            "transforms": [],
        }

        working = tempfile.TemporaryDirectory()

        with self.assertRaises(exceptions.EntrypointNotFound):
            build.build(configuration, working.name)


SYSTEM_TESTS = [
    ConfigurationTests,
    DependencyTests,
    UtilityTests,
    BlueprintTests,
    ComponentTests,
    TransformTests,
    BuildTests,
]

INTEGRATION_TESTS = []
