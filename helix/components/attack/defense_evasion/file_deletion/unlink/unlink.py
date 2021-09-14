from .... import utils


class AttackLinuxUnlinkFileDeletionComponent(utils.SimpleTemplatedComponent):
    """Linux File Deletion via unlink."""

    name = "linux-unlink-file-deletion"
    verbose_name = "Linux Unlink File Deletion"
    description = "Linux File Deletion via unlink"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "defense-evasion"),
        ("technique", "file-deletion"),
        ("id", "T1107"),
        ("name", "linux-unlink"),
    )

    options = {"path": {}}

    source = "linux-unlink.cpp"
    function = "linux_unlink"
