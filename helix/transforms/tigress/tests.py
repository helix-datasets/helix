import os
import re
import unittest

from .configurations import argument_specification
from .utils import _validate, _to_dict
from ... import exceptions
from ... import tests


def run_validation(transform, option, choices):
    invalid_choices = []

    for c in choices:
        config = {option: c}
        _, result = _validate(transform, config)
        invalid_choices.extend(result)
    return [c for _, _, c in invalid_choices]


class TigressUtilityTests(tests.UnitTestCase):
    def test_valid_int(self):
        transform = "top_level"
        option = "verbosity"
        choices = ["0", "1", "10", "100", "1000"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_int(self):
        transform = "top_level"
        option = "verbosity"
        choices = ["0.1", "-1", "10.0", "100.00"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_intspec(self):
        transform = "top_level"
        option = "seed"
        choices = ["?", "1?2", "10?20", "100"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_instspec(self):
        transform = "top_level"
        option = "seed"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_bool(self):
        transform = "virtualize"
        option = "short_idents"
        choices = ["true", "false"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_bool(self):
        transform = "virtualize"
        option = "short_idents"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_boolspec(self):
        transform = "virtualize"
        option = "optimize_body"
        choices = ["true", "false"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_boolspec(self):
        transform = "virtualize"
        option = "optimize_body"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_fracspec(self):
        transform = "virtualize"
        option = "dynamic_block_fraction"
        choices = ["*", "1", "2?20", "%20"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_fracspec(self):
        transform = "virtualize"
        option = "dynamic_block_fraction"
        choices = ["1.0", "100?", "+1", "-1", "string"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_identspec(self):
        transform = "top_level"
        option = "global_variables"
        choices = ["*", "?1", "%20", "[0-9]+", "test"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_valid_inputspec(self):
        transform = "top_level"
        option = "input"
        choices = ["1", "?20", "100?", "10?20", "+1", "-45", "int", "string", "lenght"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_valid_string(self):
        transform = "top_level"
        option = "prefix"
        choices = ["any"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_valid_specifications_from_list(self):
        transform = "virtualize"
        option = "performance"
        choices = [
            "IndexedStack",
            "PointerStack",
            "AddressSizeShort",
            "AddressSizeInt",
            "AddressSizeLong",
            "CacheTop",
        ]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_specification_from_list(self):
        transform = "virtualize"
        option = "performance"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_specification_as_list(self):
        transform = "split"
        option = "kinds"
        choices = ["top-block-deep", "deep-recursive-top", "inside-top-block"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_specification_as_list(self):
        transform = "split"
        option = "kinds"
        choices = ["top-top-deep", "1", "recursive-top-recursive", "top-block-test"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_valid_float(self):
        transform = "virtualize"
        option = "virtualize_ops_ration"
        choices = ["1.2", "0.0001"]
        self.assertEquals(run_validation(transform, option, choices), [])

    def test_invalid_float(self):
        transform = "virtualize"
        option = "virtualize_ops_ration"
        choices = ["*", "1.0?2", "1?2.0", "test"]
        self.assertEquals(run_validation(transform, option, choices), choices)

    def test_to_dict(self):
        transforms = "split:kinds=block-level-recursive,name=first;split;split:kinds=level-recursive-block,name=third"

        result = _to_dict(transforms)
        parsed = {
            "transform-1": {
                "transform_name": "split",
                "kinds": "block-level-recursive",
                "name": "first",
            },
            "transform-2": {"transform_name": "split"},
            "transform-3": {
                "transform_name": "split",
                "kinds": "level-recursive-block",
                "name": "third",
            },
            "all_transforms": ["split", "split", "split"],
        }
        self.assertEqual(result, parsed)


class TigressTests(tests.UnitTestCase):
    blueprint = "cmake-c"
    transform = "tigress"


#     @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
#     def test_missing_transformation_fails(self):
#         with self.assertRaises(exceptions.ConfigurationError) as error:
#             self.build(
#                 {
#                     "name": "test",
#                     "blueprint": {"name": self.blueprint},
#                     "components": [],
#                     "transforms": [{"name": self.transform}],
#                 }
#             )

#         self.assertIn("missing transformation", str(error.exception))

#     @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
#     def test_invalid_configuration_fails(self):
#         with self.assertRaises(exceptions.ConfigurationError) as error:
#             self.build(
#                 {
#                     "name": "test",
#                     "blueprint": {"name": self.blueprint},
#                     "components": [],
#                     "transforms": [
#                         {
#                             "name": self.transform,
#                             "configuration": {
#                                 "Flatten": "true",
#                                 "FlattenDispatch": "dummy",
#                             },
#                         }
#                     ],
#                 }
#             )

#         self.assertIn("invalid configuration", str(error.exception))

# @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
# def test_single_transform(self):
#     transforms = ["Flatten", "Split"]

#     for tr in transforms:
#         self.build(
#                 {
#                     "name": "test",
#                     "blueprint": {"name": self.blueprint},
#                     "components": [{"name": "fibonacci"}],
#                     "transforms": [
#                         {
#                             "name": self.transform,
#                             "configuration": {
#                                 tr: "true",
#                                 "Verbosity": "1",
#                             },
#                         }
#                     ],
#                 }
#             )

#         with open(self.working + "/source.c", "r") as f:
#             source = f.read()
#             all_functions = extract_fnames(source)

#             d1 = {}
#             for f in all_functions:
#                 d1[f] = tr

#             print(d1)


#         with open(self.working + "/log.txt", "r") as f:
#             log = f.read()
#             transformed_functions = re.findall("BEGIN TRANSFORM \((.*)\)", log)
#             transformations = re.findall("transformationKind=(.*?);", log)
#             transformations = list(filter(lambda x: x != "Ident", transformations))

#             d2 = {}
#             for f, t in zip(transformed_functions, transformations):
#                 d2[f] = t

#             print(d2)


#         self.assertDictEqual(d1, d2)
