from .... import utils


class AttackWindowsRegQueryValueQueryRegistryComponent(utils.SimpleTemplatedComponent):
    """Read a registry key with RegQueryValue."""

    name = "windows-regqueryvalue-query-registry"
    verbose_name = "Windows RegQueryValue Query Registry"
    description = "Read a registry key with RegQueryValue"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "discovery"),
        ("technique", "query-registry"),
        ("id", "T1012"),
        ("name", "windows-regqueryvalue"),
    )

    options = {"hive": {"literal": True}, "path": {}, "key": {}}

    source = "windows-registry-regqueryvalue.cpp"
    function = "windows_registry_regqueryvalue"
