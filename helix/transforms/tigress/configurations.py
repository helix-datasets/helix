"""Constant string values."""
bool_str = "bool"
boolspec_str = "boolspec"
float_str = "float"
fracspec_str = "fracspec"
identspec_str = "identspec"
inputspec_str = "inputspec"
int_str = "int"
intspec_str = "intspec"
localspec_str = "localspec"
regex_str = "regex"
string_str = "string"
tuple_str = "tuple"


"""argument_specification (dict): 

    Dictionary that maps the string representing an argument specification to it's valid values and the format
    of those values. Said format is used by tigress.utils._validate() to determine the method that will be used
    to verify the validity of the user input.

    Example:
    To represent a specification that takes bool values we define:
        bool_str: {
            "valid": ("true", "false"),
            "format": tuple_str,
        }

    Note:
        * If "format" = tuple_str: valid user input must be one of the elements in the tuple
        * If "format" = regex_str: valid user input needs to match one of the specified rgx
        * If "format" and "valid" = None: specification takes as input any string
        * If "format" = float_str: user input needs to be able to be transformed from str -> float
"""
argument_specification = {
    bool_str: (("true", "false"), tuple_str),
    boolspec_str: (("?", "true", "false"), tuple_str),
    float_str: (None, float_str),
    fracspec_str: (["\*", "[0-9]+", "[0-9]+\?[0-9]+", "%[0-9]+"], regex_str),
    identspec_str: (None, None),
    inputspec_str: (None, None),
    int_str: (["[0-9]+"], regex_str),
    intspec_str: (["\?", "[0-9]+\?[0-9]+", "[0-9]+"], regex_str),
    localspec_str: (None, None),
    string_str: (None, None),
}


"""Declaration of valid configurations for top-level and each transform in the format:
    <transform> = {
        <specification> : <valid_format>,
        ...
    }

    Note:
        Some specifications define their own valid_format different than the hardcoded ones
        under the argument_specification dictionary. The current other formats are:
            * type tuple: valid user input must be an element of the tuple
            * type list: valid user input must be a '-' separated concatenation of elements in
            the list
            * bool value: represents a specification that is a flag
"""
top_level = {
    "environment": string_str,
    "file_prefix": string_str,
    "seed": intspec_str,
}

add_opaque = {
    "count": intspec_str,
    "kinds": ["bug", "call", "fake", "junk", "question", "true", "*"],
    "obfuscate": bool_str,
    "split_kinds": ["block", "deep", "inside", "level", "recursive", "top"],
    "split_level": intspec_str,
    "structs": ["array", "env", "input", "list", "*"],
}

anti_alias_analysis = {"obfuscate_index": boolspec_str, "bogus_entries": boolspec_str}

anti_branch_analysis = {
    "branch_fun_address_offset": int_str,
    "branch_fun_flatten": boolspec_str,
    "kinds": ["branchFuns", "goto2nopSled", "goto2call", "goto2push", "*"],
    "obfuscate_branch_fun_call": boolspec_str,
    "opaque_structs": ["list", "array", "input", "env", "*"],
}

anti_taint_analysis = {
    "kinds": ["argv", "sysCalls", "vars", "*"],
    "implicit_flow": string_str,
    "sys_calls": ["getpid", "scanf", "*"],
}

checksum = {
    "addressing": ("absolute", "relative"),
    "call_checkers_to_be_inserted_where": string_str,
    "do_not_insert_segment_checkers_in_these_functions": string_str,
    "function_priority": string_str,
    "functions_to_be_checked_at_calls_site": string_str,
    "hash_functions_file": string_str,
    "hash_function_kinds": ("add", "linear", "mul", "quadratic", "random", "xor"),
    "hash_value_types": ["int32", "int64"],
    "insert_segment_checkers_in_these_functions": identspec_str,
    "obfuscate_body": boolspec_str,
    "protect_segments": ["const", "cstring", "data", "text"],
    "random_hash_function_size": intspec_str,
    "response_kinds": ("abort", "global", "plugin", "random"),
    "require_number_of_segment_checkers": intspec_str,
    "segment_checkers_to_be_inserted_where": (
        "annotations",
        "first" "randomly",
        "randomlyNoLoops",
        "topLevel",
    ),
    "trace_kinds": ["check", "start", "step", "stop"],
}

clean_up = {
    "do_not_remove": string_str,
    "dump_call_graph": boolspec_str,
    "kinds": [
        "annotations",
        "compress",
        "constants",
        "names",
        "noExterns",
        "noMain",
        "randomize",
        "removeUnusedFunctions",
        "*",
    ],
    "roots": string_str,
}

copy = {"name": string_str}

encode_arithmetic = {
    "dump_file_name": string_str,
    "kinds": ("integer"),
    "max_level": intspec_str,
    "max_transforms": intspec_str,
}

encode_data = {"codecs": ["add", "poly1", "xor", "*"]}

encode_external = {"obfuscate_index": boolspec_str, "symbols": string_str}

encode_literals = {
    "encoder_name": string_str,
    "integer_kinds": ("opaque", "split"),
    "kinds": ["integer", "string", "*"],
    "max_level": intspec_str,
    "max_transforms": intspec_str,
}

flatten = {
    "conditional_kinds": ("branch", "compute", "flag"),
    "dispatch": ("call", "goto", "indirect", "switch", "*"),
    "dump_blocks": boolspec_str,
    "implicit_flow": string_str,
    "implicit_flow_next": bool_str,
    "number_of_blocks_per_function": intspec_str,
    "obfuscate_next": boolspec_str,
    "opaque_structs": ("array", "list", "*"),
    "randomize_blocks": boolspec_str,
    "split_basic_blocks": boolspec_str,
    "split_name": string_str,
    "trace": boolspec_str,
}

ident = {}

info = {
    "globals_file_name": string_str,
    "kind": (
        "alias",
        "cfg",
        "CG",
        "DG",
        "fun",
        "globals",
        "linear",
        "src",
        "universe",
        "WS",
    ),
    "universe_file_name": string_str,
}

init_branch_funs = {"count": int_str}

init_opaque = {
    "count": intspec_str,
    "size": intspec_str,
    "structs": ["array", "env", "input", "list", "*"],
    "trace": boolspec_str,
}

inline = {
    "dump_call_graph": boolspec_str,
    "keep_functions": string_str,
    "optimize_kinds": ["constProp", "copyProp", "gotos", "mergeLocals"],
}

jit = {
    "annotate_tree": boolspec_str,
    "copy_kinds": [
        "bitcopy_loop",
        "bitcopy_signal",
        "bitcopy_unrolled",
        "counter",
        "counter_signal",
        "*",
    ],
    "dump_binary": boolspec_str,
    "dump_CFG": boolspec_str,
    "dump_intermediate": boolspec_str,
    "dump_opcodes": intspec_str,
    "dump_tree": boolspec_str,
    "encoding": ("hard", "soft"),
    "frequency": intspec_str,
    "implicit_flow": string_str,
    "implicit_flow_handle": boolspec_str,
    "obfuscate_arguments": boolspec_str,
    "obfuscate_handle": boolspec_str,
    "optimize_binary": intspec_str,
    "randomize_blocks": boolspec_str,
    "trace": intspec_str,
    "trace_exec": boolspec_str,
}

jit_dynamic = {
    "annotate_tree": boolspec_str,
    "block_fraction": fracspec_str,
    "codecs": (
        "ident",
        "ident_loop",
        "none",
        "stolen_byte",
        "stolen_short",
        "stolen_word",
        "xor_byte_loop",
        "xor_call",
        "xor_call_trace",
        "xor_qword_loop",
        "xor_transfer",
        "xor_word_loop",
        "xtea",
        "xtea_trace",
    ),
    "compile_command": string_str,
    "dump_CFG": boolspec_str,
    "dump_intermediate": boolspec_str,
    "dump_opcodes": intspec_str,
    "dump_tree": boolspec_str,
    "encoding": ("hard", "soft"),
    "frequency": intspec_str,
    "implicit_flow": string_str,
    "implicit_flow_handle": boolspec_str,
    "key_types": ("code", "data"),
    "obfuscate_arguments": boolspec_str,
    "obfuscate_handle": boolspec_str,
    "optimize": boolspec_str,
    "optimize_binary": intspec_str,
    "randomize_blocks": boolspec_str,
    "re_encode": boolspec_str,
    "trace": intspec_str,
    "trace_block": string_str,
    "trace_exec": intspec_str,
}

init_encode_external = {"symbols": string_str}

init_entropy = {
    "kinds": ["thread", "vars", "*"],
    "thread_name": string_str,
    "thread_sleep": intspec_str,
    "trace": boolspec_str,
}

init_implicit_flow = {
    "file_cache_size": intspec_str,
    "handler_count": intspec_str,
    "jit_count": intspec_str,
    "jit_function_body": string_str,
    "kinds": [
        "bitcopy_loop",
        "bitcopy_signal",
        "bitcopy_unrolled",
        "branchPrediction_time",
        "counter_float",
        "counter_int",
        "counter_signal",
        "file_cache_time",
        "file_cache_thread_1",
        "file_cache_thread_2",
        "file_write",
        "jit_time",
        "mem_cache_time",
        "mem_cache_thread_1",
        "mem_cache_thread_2",
        "trivial_clock",
        "trivial_counter",
        "trivial_thread_1",
        "trivial_thread_2",
        "*",
    ],
    "time": boolspec_str,
    "training_kind": ("gap", "resend"),
    "training_parameter_range": string_str,
    "trace": boolspec_str,
    "train": boolspec_str,
    "training_times_clock": intspec_str,
    "training_times_thread": intspec_str,
    "training_gap_max_failure_rate_clock": intspec_str,
    "training_gap_max_failure_rate_thread": intspec_str,
    "training_gap_min_gap": intspec_str,
    "training_resend_confidence_level": float_str,
    "training_resend_target_error_rate": float_str,
    "training_data": string_str,
}

init_plugins = {
    "initialize_prefix": string_str,
    "invariant_prefix": string_str,
    "responder_prefix": string_str,
    "update_prefix": string_str,
}

leak = {
    "debug": bool_str,
    "kind": ("dynamic", "dynamic_byte", "static"),
    "secret_functions": string_str,
    "value": intspec_str,
    "variable": string_str,
}

measure = {"kind": ("time"), "times": intspec_str}

merge = {
    "conditional_kinds": ("branch", "compute", "flag"),
    "flatten": boolspec_str,
    "flatten_dispatch": ("goto", "indirect", "switch", "?"),
    "name": string_str,
    "obfuscate_select": boolspec_str,
    "opaque_structs": ("list", "array", "*"),
    "randomize_blocks": boolspec_str,
    "split_basic_blocks": boolspec_str,
}

optimize = {
    "dump_interference_graph": False,
    "kinds": ["constProp", "copyProp", "mergeLocals"],
    "short_merged_names": False,
}

random_funs = {
    "activation_code": int_str,
    "activation_code_check_count": int_str,
    "basic_block_size": intspec_str,
    "bool_size": intspec_str,
    "code_size": intspec_str,
    "control_structures": string_str,
    "dummy_failure": boolspec_str,
    "failure_kind": ["abort", "assign", "message", "random", "segv"],
    "for_bound": ["boundedAny", "boundedInput", "constant", "input"],
    "function_count": intspec_str,
    "global_dynamic_state_size": intspec_str,
    "global_static_state_size": intspec_str,
    "input_kind": ("argv", "stdin"),
    "input_size": intspec_str,
    "input_type": ("int", "float", "string"),
    "local_dynamic_state_size": intspec_str,
    "local_static_state_size": intspec_str,
    "loop_size": intspec_str,
    "name": string_str,
    "operators": [
        "BAnd",
        "BOr",
        "BXor",
        "Div",
        "Eq",
        "Ge",
        "Gt",
        "Le",
        "Lt",
        "MinusA",
        "Mod",
        "Mult",
        "Ne",
        "PlusA",
        "Shiftlt",
        "Shiftrt",
        "*",
    ],
    "output_size": intspec_str,
    "password": string_str,
    "password_check_count": int_str,
    "point_test": bool_str,
    "security_check_count": int_str,
    "security_check_values": string_str,
    "time_check_count": int_str,
    "trace": intspec_str,
    "trace_assets": boolspec_str,
    "type": ("char", "double", "float", "int", "long", "short"),
}

rnd_args = {"bogus_no": intspec_str}

self_modify = {
    "bogus_instructions": intspec_str,
    "bogus_operators": (
        "Div",
        "Eq",
        "Ge",
        "Gt",
        "Le",
        "Lt",
        "MinusA",
        "Mod",
        "Mult",
        "Ne",
        "PlusA",
        "Shiftlt",
        "Shiftrt",
        "*",
    ),
    "fraction": fracspec_str,
    "kinds": ("arithmetic", "comparisons", "indirectBranch"),
    "sub_expressions": boolspec_str,
}

software_metrics = {
    "file_name": string_str,
    "json_file_name": string_str,
    "kind": ["halstead", "mccabe", "raw"],
}

split = {
    "count": intspec_str,
    "kinds": ["block", "deep", "inside", "top", "level", "recursive"],
    "level": intspec_str,
    "locals_as_formals": boolspec_str,
    "name": string_str,
}

update_entropy = {
    "kinds": ["annotations", "thread", "vars", "*"],
    "trace": boolspec_str,
    "vars": identspec_str,
}

update_opaque = {
    "allow_add_nodes": bool_str,
    "count": intspec_str,
    "trace": boolspec_str,
}

virtualize = {
    "add_opaque_to_bogus_funs": boolspec_str,
    "add_opaque_to_VPC": boolspec_str,
    "bogus_funs_generate_output": boolspec_str,
    "bogus_fun_kinds": ["arithSeq", "collatz", "trivial", "*"],
    "bogus_loop_iterations": intspec_str,
    "bogus_loop_kinds": ("arithSeq", "collatz", "trivial", "*"),
    "comment": bool_str,
    "conditional_kinds": ("branch", "compute", "flag"),
    "dispatch": (
        "binary",
        "call",
        "direct",
        "ifnest",
        "indirect",
        "interpolation",
        "linear",
        "switch",
        "?",
    ),
    "dump": [
        "array",
        "BC",
        "bytes",
        "calls",
        "input",
        "instrs",
        "ISA",
        "stack",
        "strings",
        "SuperOps",
        "tree",
        "types",
        "vars",
        "*",
    ],
    "dynamic_annotate_tree": boolspec_str,
    "dynamic_block_fraction": fracspec_str,
    "dynamic_bytecode": bool_str,
    "dynamic_codecs": (
        "ident",
        "ident_loop",
        "none",
        "stolen_byte",
        "stolen_short",
        "stolen_word",
        "xor_byte_loop",
        "xor_call",
        "xor_call_trace",
        "xor_transfer",
        "xor_qword_loop",
        "xor_word_loop",
        "xtea",
        "xtea_trace",
    ),
    "dynamic_compile_command": string_str,
    "dynamic_dump_CFG": boolspec_str,
    "dynamic_dump_tree": boolspec_str,
    "dynamic_encoding": ("hard", "soft"),
    "dynamic_key_types": ("code", "data"),
    "dynamic_optimize": boolspec_str,
    "dynamic_randomize_blocks": boolspec_str,
    "dynamic_re_encode": boolspec_str,
    "dynamic_trace": intspec_str,
    "dynamic_trace_block": boolspec_str,
    "dynamic_trace_exec": boolspec_str,
    "encode_byte_array": bool_str,
    "implicit_flow": string_str,
    "implicit_flow_PC": ("PCInit", "PCUpdate", "*"),
    "instruction_handler_split_count": intspec_str,
    "max_duplicate_ops": intspec_str,
    "max_merge_length": intspec_str,
    "number_of_bogus_funs": intspec_str,
    "obfuscate_decode_byte_array": bool_str,
    "opaque_structs": ["array", "env", "input", "list", "*"],
    "operands": ["mixed", "registers", "stack", "?"],
    "optimize_body": boolspec_str,
    "optimize_tree_code": boolspec_str,
    "performance": (
        "AddressSizeInt",
        "AddressSizeShort",
        "AddressSizeLong",
        "CacheTop",
        "IndexedStack",
        "PointerStack",
    ),
    "random_ops": bool_str,
    "reentrant": False,
    "short_idents": bool_str,
    "stack_size": intspec_str,
    "super_ops_ratio": float_str,
    "trace": ("args", "instr", "regs", "stack", "*"),
}

top_level_transform_specific = {
    "global_variables": identspec_str,
    "local_variables": localspec_str,
    "prefix": string_str,
    "seed": intspec_str,
}

configurations = {}
configurations["add_opaque"] = add_opaque
configurations["anti_alias_analysis"] = anti_alias_analysis
configurations["anti_branch_analysis"] = anti_branch_analysis
configurations["anti_taint_analysis"] = anti_taint_analysis
configurations["checksum"] = checksum
configurations["clean_up"] = clean_up
configurations["copy"] = copy
configurations["encode_arithmetic"] = encode_arithmetic
configurations["encode_data"] = encode_data
configurations["encode_external"] = encode_external
configurations["encode_literals"] = encode_literals
configurations["flatten"] = flatten
configurations["ident"] = ident
configurations["info"] = info
configurations["init_branch_funs"] = init_branch_funs
configurations["init_encode_external"] = init_encode_external
configurations["init_entropy"] = init_entropy
configurations["init_implicit_flow"] = init_implicit_flow
configurations["init_opaque"] = init_opaque
configurations["init_plugins"] = init_plugins
configurations["inline"] = inline
configurations["jit"] = jit
configurations["jit_dynamic"] = jit_dynamic
configurations["leak"] = leak
configurations["measure"] = measure
configurations["merge"] = merge
configurations["optimize"] = optimize
configurations["random_funs"] = random_funs
configurations["rnd_args"] = rnd_args
configurations["self_modify"] = self_modify
configurations["software_metrics"] = software_metrics
configurations["split"] = split
configurations["top_level"] = top_level
configurations["update_entropy"] = update_entropy
configurations["update_opaque"] = update_opaque
configurations["virtualize"] = virtualize


"""Add top_level_transform_specific configs to each transform."""
for transform in configurations.keys() - {"top_level"}:
    configurations[transform].update(top_level_transform_specific)

"""List of available transforms."""
tigress_transforms = configurations.keys()
