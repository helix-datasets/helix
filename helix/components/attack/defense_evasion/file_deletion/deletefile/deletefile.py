from .... import utils


class AttackWindowsDeleteFileFileDeletionComponent(utils.SimpleTemplatedComponent):
    """Windows File Deletion via DeleteFile."""

    name = "windows-deletefile-file-deletion"
    verbose_name = "Windows Delete File Deletion"
    description = "Windows File Deletion via DeleteFile"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "defense-evasion"),
        ("technique", "file-deletion"),
        ("id", "T1107"),
        ("name", "windows-deletefile"),
    )

    options = {"path": {}}

    source = "windows-deletefile.cpp"
    function = "windows_deletefile"
