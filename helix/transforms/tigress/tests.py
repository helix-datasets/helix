import os
import unittest

from .utils import validate, to_dict, build_command
from ... import exceptions
from ... import tests


def run_option_validation(transform, option):
    config = {option: ""}
    io, _ = validate(transform, config)
    return [o for _, o in io]


def run_choice_validation(transform, option, choices):
    result = list()

    for c in choices:
        config = {option: c}
        _, ic = validate(transform, config)
        result.extend(ic)

    return [c for _, _, c in result]


class TigressUtilityTests(tests.UnitTestCase):
    def test_valid_bool(self):
        transform = "virtualize"
        option = "short_idents"
        choices = ["true", "false"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_bool(self):
        transform = "virtualize"
        option = "short_idents"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_boolspec(self):
        transform = "virtualize"
        option = "optimize_body"
        choices = ["true", "false"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_boolspec(self):
        transform = "virtualize"
        option = "optimize_body"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_float(self):
        transform = "virtualize"
        option = "super_ops_ratio"
        choices = ["1.2", "0.0001"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_float(self):
        transform = "virtualize"
        option = "super_ops_ratio"
        choices = ["*", "1.0?2", "1?2.0", "test"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_fracspec(self):
        transform = "virtualize"
        option = "dynamic_block_fraction"
        choices = ["*", "1", "2?20", "%20"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_fracspec(self):
        transform = "virtualize"
        option = "dynamic_block_fraction"
        choices = ["1.0", "100?", "+1", "-1", "string"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_identspec(self):
        transform = "top_level"
        option = "global_variables"
        choices = ["*", "?1", "%20", "[0-9]+", "test"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_valid_inputspec(self):
        transform = "top_level"
        option = "input"
        choices = ["1", "?20", "100?", "10?20", "+1", "-45", "int", "string", "lenght"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_valid_int(self):
        transform = "anti_branch_analysis"
        option = "branch_fun_address_offset"
        choices = ["0", "1", "10", "100", "1000"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_int(self):
        transform = "anti_branch_analysis"
        option = "branch_fun_address_offset"
        choices = ["0.1", "-1", "10.0", "100.00"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_intspec(self):
        transform = "top_level"
        option = "seed"
        choices = ["?", "1?2", "10?20", "100"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_instspec(self):
        transform = "top_level"
        option = "seed"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_string(self):
        transform = "top_level"
        option = "prefix"
        choices = ["any"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

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
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_specification_from_list(self):
        transform = "virtualize"
        option = "performance"
        choices = ["*", "1.0?2", "1?2.0", "10.0"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_specification_as_list(self):
        transform = "split"
        option = "kinds"
        choices = ["top-block-deep", "deep-recursive-top", "inside-top-block"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(len(invalid_choices), 0)

    def test_invalid_specification_as_list(self):
        transform = "split"
        option = "kinds"
        choices = ["top-top-deep", "1", "recursive-top-recursive", "top-block-test"]
        invalid_choices = run_choice_validation(transform, option, choices)
        self.assertEquals(invalid_choices, choices)

    def test_valid_flag(self):
        transform = "optimize"
        option = "dump_interference_graph"
        invalid_option = run_option_validation(transform, option)
        self.assertEquals(len(invalid_option), 0)

    def test_invalid_flag(self):
        transform = "optimize"
        option = "test"
        invalid_option = run_option_validation(transform, option)
        self.assertEqual(len(invalid_option), 1)
        self.assertEquals(invalid_option[0], option)

    def test_valid_option(self):
        transform = "add_opaque"
        option = "count"
        invalid_option = run_option_validation(transform, option)
        self.assertEquals(len(invalid_option), 0)

    def test_invalid_option(self):
        transform = "add_opaque"
        option = "test"
        invalid_option = run_option_validation(transform, option)
        self.assertEqual(len(invalid_option), 1)
        self.assertEquals(invalid_option[0], option)

    def test_to_dict(self):
        transforms = "split:kinds=block-level-recursive,flag,name=first;split;split:kinds=level-recursive-block,name=third"

        result = to_dict(transforms)
        parsed = {
            "transform-1": {
                "transform_name": "split",
                "kinds": "block-level-recursive",
                "flag": "",
                "name": "first",
            },
            "transform-2": {"transform_name": "split"},
            "transform-3": {
                "transform_name": "split",
                "kinds": "level-recursive-block",
                "name": "third",
            },
            "transforms_lst": ["split", "split", "split"],
        }
        self.assertEqual(result, parsed)

    def test_build_command(self):
        configurations = {
            "environment": "x86_64:Linux:Gcc:4.6",
            "seed": "0",
            "file_prefix": "NONE",
            "transforms": "",
        }
        transforms = (
            "virtualize:conditional_kinds=flag,reentrant,dynamic_re_encode=true;"
        )
        "split;split:kinds=level-recursive-block,name=third"

        parsed = to_dict(transforms)
        configurations["transforms"] = parsed

        result = build_command(configs=configurations, source="/path/to/source.c")
        cmd = "--Environment=x86_64:Linux:Gcc:4.6 --Seed=0 --FilePrefix=NONE "
        "--Transform=Virtualize --VirtualizeConditionalKinds=flag --VirtualizeReentrant "
        "--VirtualizeDynamicReEncode=true --Functions=* --Transform=Split --Functions=* "
        "--Transform=Split --SplitKinds=level,recursive,block --SplitName=third --Functions=* "
        "/path/to/source.c --out=result.c"
        self.assertIn(cmd, result)


class TigressTests(tests.UnitTestCase):
    blueprint = "cmake-c"
    transform = "tigress"
    component = "fibonacci"

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_missing_transforms_fails(self):
        with self.assertRaises(exceptions.ConfigurationError) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [{"name": self.component}],
                    "transforms": [{"name": self.transform}],
                }
            )

        self.assertIn(
            "missing required configuration parameter: transforms", str(error.exception)
        )

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_invalid_transform_fails_1(self):
        with self.assertRaises(exceptions.ConfigurationError) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [{"name": self.component}],
                    "transforms": [
                        {
                            "name": self.transform,
                            "configuration": {"transforms": "fail"},
                        }
                    ],
                }
            )

        self.assertIn("no valid transform was provided", str(error.exception))

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_invalid_transform_fails_2(self):
        with self.assertRaises(exceptions.ConfigurationError) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [{"name": self.component}],
                    "transforms": [
                        {
                            "name": self.transform,
                            "configuration": {
                                "transforms": "split;invalid_transform1;flatten;invalid_transform2"
                            },
                        }
                    ],
                }
            )
        invalid = ["invalid_transform1", "invalid_transform2"]
        for t in invalid:
            self.assertIn(t, str(error.exception))

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_invalid_option_fails(self):
        with self.assertRaises(exceptions.ConfigurationError) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [{"name": self.component}],
                    "transforms": [
                        {
                            "name": self.transform,
                            "configuration": {
                                "transforms": "split:countss=2,kinds=block-level-inside",
                            },
                        }
                    ],
                }
            )
        self.assertIn("transform:split invalid_option=countss", str(error.exception))

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_invalid_choice_fails(self):
        with self.assertRaises(exceptions.ConfigurationError) as error:
            self.build(
                {
                    "name": "test",
                    "blueprint": {"name": self.blueprint},
                    "components": [{"name": self.component}],
                    "transforms": [
                        {
                            "name": self.transform,
                            "configuration": {
                                "transforms": "split:kinds=block-level-inside-block",
                            },
                        }
                    ],
                }
            )
        self.assertIn(
            "transform:split option:kinds invalid_choice=block-level-inside-block",
            str(error.exception),
        )

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_tigress_recipe_1(self):
        # source: https://tigress.wtf/recipes.html
        hlx_transforms = "init_entropy:kinds=vars;init_opaque:structs=list-array-env;init_branch_funs:count=1;add_opaque:structs=list,kinds=true;anti_branch_analysis:kinds=branchFuns,obfuscate_branch_fun_call=false,branch_fun_flatten=true;encode_arithmetic"

        artifacts, _ = self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [{"name": self.component}],
                "transforms": [
                    {
                        "name": self.transform,
                        "configuration": {
                            "transforms": hlx_transforms,
                        },
                    }
                ],
            }
        )
        self.assertIsNotNone(artifacts)

    @unittest.skipUnless(os.name == "posix", "test not supported on this platform")
    def test_tigress_recipe_2(self):
        # source: https://tigress.wtf/recipes.html
        hlx_transforms = "init_entropy:kinds=vars;init_opaque:structs=list-array-env;virtualize:dispatch=ifnest;self_modify:sub_expressions=false,bogus_instructions=10"

        artifacts, _ = self.build(
            {
                "name": "test",
                "blueprint": {"name": self.blueprint},
                "components": [{"name": self.component}],
                "transforms": [
                    {
                        "name": self.transform,
                        "configuration": {
                            "transforms": hlx_transforms,
                        },
                    }
                ],
            }
        )
        self.assertIsNotNone(artifacts)
