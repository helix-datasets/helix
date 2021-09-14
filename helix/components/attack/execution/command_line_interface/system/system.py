from .... import utils


class AttackLinuxSystemCommandLineInterfaceComponent(utils.SimpleTemplatedComponent):
    """Linux Command Line Interface via system."""

    name = "linux-system-command-line-interface"
    verbose_name = "Linux System Command Line Interface"
    description = "Linux Command Line Interface via system."
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "execution"),
        ("technique", "command-line-interface"),
        ("id", "T1059"),
        ("name", "linux-system"),
    )

    options = {"command": {}}

    source = "linux-system.cpp"
    function = "linux_system"
