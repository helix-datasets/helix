from .... import utils


class AttackLinuxUtimeTimestompComponent(utils.SimpleTemplatedComponent):
    """Linux Timestomp via utime."""

    name = "linux-utime-timestomp"
    verbose_name = "Linux Utime Timestomp"
    description = "Linux Timestomp via utime."
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "defense-evasion"),
        ("technique", "timestomp"),
        ("id", "T1099"),
        ("name", "linux-utime"),
    )

    options = {"path": {}, "timestamp": {}}
    """Configuration options.

    Example:
        Timestamp should be in the following format: %Y-%m-%d %H:%M:%S e.g.,
        2001-11-12 18:31:01
    """

    source = "linux-utime.cpp"
    function = "linux_utime"
