from .... import utils


class AttackLinuxRemoveFileDeletionComponent(utils.SimpleTemplatedComponent):
    """Linux File Deletion via remove."""

    name = "linux-remove-file-deletion"
    verbose_name = "Linux Remove File Deletion"
    description = "Linux File Deletion via remove"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "defense-evasion"),
        ("technique", "file-deletion"),
        ("id", "T1107"),
        ("name", "linux-remove"),
    )

    options = {"path": {}}

    source = "linux-remove.cpp"
    function = "linux_remove"
