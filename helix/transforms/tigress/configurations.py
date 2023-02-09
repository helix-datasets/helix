"""Constant string values."""
int_str = "int"
intspec_str = "intspec"
bool_str = "bool"
boolspec_str = "boolspec"
fracspec_str = "fracspec"
identspec_str = "identspec"
inputspec_str = "inputspec"
localspec_str = "localspec"
string_str = "string"
regex_str = "regex"
tuple_str = "tuple"
float_str = "float"


"""List of argument specifications and their format."""
argument_specification = {
    int_str: (["[0-9]+"], regex_str),
    intspec_str: (["\?", "[0-9]+\?[0-9]+", "[0-9]+"], regex_str),
    bool_str: (("true", "false"), tuple_str),
    boolspec_str: (("?", "true", "false"), tuple_str),
    fracspec_str: (["\*", "[0-9]+", "[0-9]+\?[0-9]+", "%[0-9]+"], regex_str),
    identspec_str: ([], ""),
    inputspec_str: ([], ""),
    localspec_str: ([], ""),
    string_str: ([], ""),
    float_str: ([], float_str),
}


"""Declaration of valid configurations for top-level and each transform in the format:
    <transform> = {
        <specification> : <format>,
        ...
    }
"""
top_level = {
    "environment": string_str,
    "seed": intspec_str,
    "verbosity": int_str,
    "input": inputspec_str,
}

all_transforms = {
    "file_prefix": string_str,
    "prefix": string_str,
    "global_variables": identspec_str,
    "local_variables": localspec_str,
}

virtualize = {
    "short_idents": bool_str,
    "performance": (
        "IndexedStack",
        "PointerStack",
        "AddressSizeShort",
        "AddressSizeInt",
        "AddressSizeLong",
        "CacheTop",
    ),
    "optimize_body": boolspec_str,
    "optimize_tree_code": boolspec_str,
    "trace": ("instr", "args", "stack", "regs", "*"),
    "stack_size": intspec_str,
    "comments": bool_str,
    "dump": [
        "input",
        "tree",
        "ISA",
        "instrs",
        "types",
        "vars",
        "strings",
        "SuperOps",
        "calls",
        "bytes",
        "array",
        "stack",
        "*",
    ],
    "conditional_kinds": ("branch", "compute", "flag"),
    "dispatch": (
        "switch",
        "direct",
        "indirect",
        "call",
        "ifnest",
        "linear",
        "binary",
        "interpolation",
        "?",
    ),
    "operands": ["stack", "registers", "mixed", "?"],
    "max_duplicate_ops": intspec_str,
    "random_ops": bool_str,
    "virtualize_ops_ration": float_str,
    "max_merge_length": intspec_str,
    "instruction_handler_split_count": intspec_str,
    "add_opaque_to_VPC": boolspec_str,
    "implicit_flow_PC": ("PCInit", "PCUpdate", "*"),
    "implicit_flow": string_str,
    "add_opaque_to_bogus_funs": boolspec_str,
    "number_of_bogus_funs": intspec_str,
    "bogus_funs_generate_output": boolspec_str,
    "bogus_funs_kinds": ["trivial", "arithSeq", "collatz", "*"],
    "bogus_loop_kinds": ("trivial", "arithSeq", "collatz", "*"),
    "bogus_loop_iterations": intspec_str,
    "reentrant": False,
    "opaque_structs": ["list", "array", "input", "env", "*"],
    "enconde_byte_array": bool_str,
    "obfuscate_decode_byte_array": bool_str,
    "dynamic_bytecode": bool_str,
    "dynamic_encoding": ("hard", "soft"),
    "dynamic_optimize": boolspec_str,
    "dynamic_trace": intspec_str,
    "dynamic_trace_exec": boolspec_str,
    "dynamic_dump_tree": boolspec_str,
    "dynamic_annotate_tree": boolspec_str,
    "dynamic_codecs": (
        "none",
        "ident",
        "ident_loop",
        "xor_transfer",
        "xor_byte_loop",
        "xor_word_loop",
        "xor_qword_loop",
        "xor_call",
        "xor_call_trace",
        "xtea",
        "xtea_trace",
        "stolen_byte",
        "stolen_short",
        "stolen_word",
    ),
    "dynamic_key_types": ("data", "code"),
    "dynamic_block_fraction": fracspec_str,
    "dynamic_randomize_blocks": boolspec_str,
    "dynamic_re_encode": boolspec_str,
    "dynamic_dump_CFG": boolspec_str,
    "dynamic_trace_block": boolspec_str,
    "dynamic_compile_command": string_str,
}

jit = {
    "encoding": ("hard", "soft"),
    "frequency": intspec_str,
    "optimize_binary": intspec_str,
    "implicit_flow": string_str,
    "copy_kinds": [
        "counter",
        "counter_signal",
        "bitcopy_unrolled",
        "bitcopy_loop",
        "bitcopy_signal",
        "*",
    ],
    "obfuscate_handle": boolspec_str,
    "obfuscate_arguments": boolspec_str,
    "dump_opcodes": intspec_str,
    "trace": intspec_str,
    "trace_exec": boolspec_str,
    "dump_tree": boolspec_str,
    "annotate_tree": boolspec_str,
    "dump_intermediate": boolspec_str,
    "dump_binary": boolspec_str,
    "randomize_blocks": boolspec_str,
}

jit_dynamic = {
    "encoding": ("hard", "soft"),
    "frequency": intspec_str,
    "optimize_binary": intspec_str,
    "implicit_flow_handle": boolspec_str,
    "implicit_flow": string_str,
    "obfuscate_handle": boolspec_str,
    "obfuscate_arguments": boolspec_str,
    "dump_opcodes": intspec_str,
    "trace": intspec_str,
    "trace_exec": intspec_str,
    "dump_tree": boolspec_str,
    "annotate_tree": boolspec_str,
    "dump_intermediate": boolspec_str,
    "codecs": (
        "none",
        "ident",
        "ident_loop",
        "xor_transfer",
        "xor_byte_loop",
        "xor_word_loop",
        "xor_qword_loop",
        "xor_call",
        "xor_call_trace",
        "xtea",
        "xtea_trace",
        "stolen_byte",
        "stolen_short",
        "stolen_word",
    ),
    "key_types": ("data", "code"),
    "block_fraction": fracspec_str,
    "randomize_blocks": boolspec_str,
    "re_encode": boolspec_str,
    "optimize": boolspec_str,
    "dump_CFG": boolspec_str,
    "trace_block": string_str,
    "compile_command": string_str,
}

flatten = {
    "dump_blocks": boolspec_str,
    "split_basic_blocks": boolspec_str,
    "randomize_blocks": boolspec_str,
    "trace": boolspec_str,
    "dispatch": ("switch", "goto", "indirect", "call", "*"),
    "number_of_blocks_per_function": intspec_str,
    "split_name": string_str,
    "conditional_kinds": ("branch", "compute", "flag"),
    "obfuscate_next": boolspec_str,
    "opaque_structs": ("list", "array", "*"),
    "implicit_flow_next": bool_str,
    "implicit_flow": string_str,
}

split = {
    "kinds": ["top", "block", "deep", "recursive", "level", "inside"],
    "count": intspec_str,
    "name": string_str,
    "level": intspec_str,
    "locals_as_formals": boolspec_str,
}

merge = {
    "name": string_str,
    "obfuscate_select": boolspec_str,
    "opaque_structs": ("list", "array", "*"),
    "flatten": boolspec_str,
    "flatten_dispatch": ("switch", "goto", "indirect", "?"),
    "split_basic_blocks": boolspec_str,
    "randomize_blocks": boolspec_str,
    "conditional_kinds": ("branch", "compute", "flag"),
}

add_opaque = {
    "count": intspec_str,
    "kinds": ["call", "bug", "true", "junk", "fake", "question", "*"],
    "obfuscate": bool_str,
    "split_kinds": ["top", "block", "deep", "recursive", "level", "inside"],
    "split_level": intspec_str,
    "structs": ["list", "array", "input", "env", "*"],
}

encode_literals = {
    "kinds": ["integer", "string", "*"],
    "encoder_name": string_str,
    "max_level": intspec_str,
    "max_transforms": intspec_str,
    "integer_kinds": ("opaque", "split"),
}

encode_data = {"codecs": ["poly1", "xor", "add", "*"]}

encode_arithmetic = {
    "kinds": ("integer"),
    "max_level": intspec_str,
    "max_transforms": intspec_str,
    "dump_file_name": string_str,
}

init_encode_external = {"symbols": string_str}

encode_external = {"obfuscate_index": boolspec_str, "symbols": string_str}

anti_branch_analysis = {
    "kinds": ["branchFuns", "goto2call", "goto2push", "goto2nopSled", "*"],
    "opaque_structs": ["list", "array", "input", "env", "*"],
    "obfuscate_branch_fun_call": boolspec_str,
    "branch_fun_flatten": boolspec_str,
    "branch_fun_address_offset": int_str,
}

anti_alias_analysis = {"obfuscate_index": boolspec_str, "bogus_entries": boolspec_str}

anti_taint_analysis = {
    "kinds": ["argv", "sysCalls", "vars", "*"],
    "sys_calls": ["getpid", "scanf", "*"],
    "implicit_flow": string_str,
}

init_opaque = {
    "structs": ["list", "array", "input", "env", "*"],
    "count": intspec_str,
    "trace": boolspec_str,
    "size": intspec_str,
}

update_opaque = {
    "count": intspec_str,
    "trace": boolspec_str,
    "allow_add_nodes": bool_str,
}

init_entropy = {
    "kinds": ["thread", "vars", "*"],
    "thread_name": string_str,
    "thread_sleep": intspec_str,
    "trace": boolspec_str,
}

update_entropy = {
    "vars": identspec_str,
    "trace": boolspec_str,
    "kinds": ["thread", "vars", "annotations", "*"],
}

init_implicit_flow = {
    "handler_count": intspec_str,
    "jit_count": intspec_str,
    "file_cache_size": intspec_str,
    "jit_function_body": string_str,
    "kinds": [
        "counter_int",
        "counter_float",
        "counter_signal",
        "bitcopy_unrolled",
        "bitcopy_loop",
        "bitcopy_signal",
        "file_write",
        "trivial_clock",
        "trivial_thread_1",
        "trivial_thread_2",
        "trivial_counter",
        "file_cache_time",
        "file_cache_thread_1",
        "file_cache_thread_2",
        "mem_cache_time",
        "mem_cache_thread_1",
        "mem_cache_thread_2",
        "jit_time",
        "branchPrediction_time",
        "*",
    ],
    "training_kind": ("gap", "resend"),
    "training_parameter_range": string_str,
    "trace": boolspec_str,
    "train": boolspec_str,
    "time": boolspec_str,
    "training_times_clock": intspec_str,
    "training_times_thread": intspec_str,
    "training_gap_max_failure_rate_clock": intspec_str,
    "training_gap_max_failure_rate_thread": intspec_str,
    "training_gap_min_gap": intspec_str,
    "training_resend_confidence_level": float_str,
    "training_resend_target_error_rate": float_str,
    "training_data": string_str,
}

random_funs = {
    "function_count": intspec_str,
    "trace": intspec_str,
    "security_check_values": string_str,
    "trace_assets": boolspec_str,
    "input_size": intspec_str,
    "local_static_state_size": intspec_str,
    "local_dynamic_state_size": intspec_str,
    "global_static_state_size": intspec_str,
    "global_dynamic_state_size": intspec_str,
    "output_size": intspec_str,
    "code_size": intspec_str,
    "loop_size": intspec_str,
    "bool_size": intspec_str,
    "type": ("char", "short", "int", "long", "float", "double"),
    "name": string_str,
    "failure_kind": ["message", "abort", "segv", "random", "assign"],
    "input_kind": ("argv", "stdin"),
    "input_type": ("int", "float", "string"),
    "dummy_failure": boolspec_str,
    "activation_code": int_str,
    "password": string_str,
    "time_check_count": int_str,
    "activation_code_check_count": int_str,
    "security_check_count": int_str,
    "password_check_count": int_str,
    "control_structures": string_str,
    "basic_block_size": intspec_str,
    "for_bound": ["constant", "input", "boundedInput", "boundedAny"],
    "operators": [
        "PlusA",
        "MinusA",
        "Mult",
        "Div",
        "Mod",
        "Shiftlt",
        "Shiftrt",
        "Lt",
        "Gt",
        "Le",
        "Ge",
        "Eq",
        "Ne",
        "BAnd",
        "BXor",
        "BOr",
        "*",
    ],
    "point_test": bool_str,
}

clean_up = {
    "kinds": [
        "names",
        "annotations",
        "constants",
        "randomize",
        "compress",
        "noExterns",
        "noMain",
        "removeUnusedFunctions",
        "*",
    ],
    "dump_call_graph": boolspec_str,
    "do_not_remove": string_str,
    "roots": string_str,
}

info = {
    "kind": (
        "cfg",
        "fun",
        "src",
        "linear",
        "WS",
        "DG",
        "CG",
        "alias",
        "globals",
        "universe",
    ),
    "universe_file_name": string_str,
    "globals_file_name": string_str,
}

measure = {"kind": ("time"), "times": intspec_str}

copy = {"name": string_str}

leak = {
    "secret_functions": string_str,
    "variable": string_str,
    "value": intspec_str,
    "kind": ("static", "dynamic", "dynamic_byte"),
    "debug": bool_str,
}

ident = {}

rnd_args = {"bogus_no": intspec_str}

self_modify = {
    "kinds": ("indirectBranch", "arithmetic", "comparisons"),
    "fraction": fracspec_str,
    "sub_expressions": boolspec_str,
    "bogus_instructions": (
        "PlusA",
        "MinusA",
        "Mult",
        "Div",
        "Mod",
        "Shiftlt",
        "Shiftrt",
        "Lt",
        "Gt",
        "Le",
        "Ge",
        "Eq",
        "Ne",
        "*",
    ),
    "bogus_instructions": intspec_str,
}

checksum = {
    "hash_function_kinds": ("add", "mul", "xor", "linear", "quadratic", "random"),
    "hash_value_types": ["int32", "int64"],
    "random_hash_function_size": intspec_str,
    "obfuscate_body": boolspec_str,
    "response_kinds": ("abort", "random", "global", "plugin"),
    "function_priority": string_str,
    "functions_to_be_checked_at_calls_site": string_str,
    "call_checkers_to_be_inserted_where": string_str,
    "require_number_of_segment_checkers": intspec_str,
    "protect_segments": ["text", "cstring", "const", "data"],
    "segment_checkers_to_be_inserted_where": (
        "randomly",
        "randomlyNoLoops",
        "topLevel",
        "first",
        "annotations",
    ),
    "insert_segment_checkers_in_these_functions": identspec_str,
    "do_not_insert_segment_checkers_in_these_functions": string_str,
    "trace_kinds": ["start", "stop", "step", "check"],
    "hash_functions_file": string_str,
    "addressing": ("relative", "absolute"),
}

inline = {
    "keep_functions": string_str,
    "dump_call_graph": boolspec_str,
    "optimize_kinds": ["constProp", "copyProp", "mergeLocals", "gotos"],
}

optimize = {
    "kinds": ["constProp", "copyProp", "mergeLocals"],
    "dump_interference_graph": False,
    "short_merged_names": False,
}

init_plugins = {
    "invariant_prefix": string_str,
    "responder_prefix": string_str,
    "initialize_prefix": string_str,
    "update_prefix": string_str,
}

software_metrics = {
    "kind": ["raw", "halstead", "mccabe"],
    "file_name": string_str,
    "json_file_name": string_str,
}

configurations = {}
configurations["top_level"] = top_level
configurations["virtualize"] = virtualize
configurations["jit"] = jit
configurations["jit_dynamic"] = jit_dynamic
configurations["flatten"] = flatten
configurations["split"] = split
configurations["merge"] = merge
configurations["add_opaque"] = add_opaque
configurations["encode_literals"] = encode_literals
configurations["encode_data"] = encode_data
configurations["encode_arithmetic"] = encode_arithmetic
configurations["init_encode_external"] = init_encode_external
configurations["encode_external"] = encode_external
configurations["anti_branch_analysis"] = anti_branch_analysis
configurations["anti_alias_analysis"] = anti_alias_analysis
configurations["anti_taint_analysis"] = anti_taint_analysis
configurations["init_opaque"] = init_opaque
configurations["update_opaque"] = update_opaque
configurations["init_entropy"] = init_entropy
configurations["update_entropy"] = update_entropy
configurations["init_implicit_flow"] = init_implicit_flow
configurations["random_funs"] = random_funs
configurations["clean_up"] = clean_up
configurations["info"] = info
configurations["measure"] = measure
configurations["copy"] = copy
configurations["leak"] = leak
configurations["ident"] = ident
configurations["rnd_args"] = rnd_args
configurations["self_modify"] = self_modify
configurations["checksum"] = checksum
configurations["inline"] = inline
configurations["optimize"] = optimize
configurations["init_plugins"] = init_plugins
configurations["software_metrics"] = software_metrics


"""List of available transforms."""
tigress_transforms = configurations.keys()
