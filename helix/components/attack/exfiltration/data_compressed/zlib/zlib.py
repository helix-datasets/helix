from .... import utils
from ...... import utils as helix_utils


class AttackLinuxZLibCompressDataCompressedComponent(utils.SimpleTemplatedComponent):
    """Linux file compression with zlib.

    Note:
        This component requires zlib1g-dev to be installed.
    """

    name = "linux-zlib-compress-data-compressed"
    verbose_name = "Linux ZLib Compress Data Compressed"
    description = "Linux file compression with zlib"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "exfiltration"),
        ("technique", "data-compressed"),
        ("id", "T1002"),
        ("name", "linux-zlib-compress"),
    )

    options = {"input": {}, "output": {}}

    dependencies = [helix_utils.LinuxAPTDependency("zlib1g-dev")]

    libraries = ["z"]

    source = "linux-compress-zlib.cpp"
    function = "linux_compress_zlib"


class AttackLinuxZLibDecompressDataCompressedComponent(utils.SimpleTemplatedComponent):
    """Linux file decompression with zlib.

    Note:
        This component requires zlib1g-dev to be installed.
    """

    name = "linux-zlib-decompress-data-compressed"
    verbose_name = "Linux ZLib Decompress Data Compressed"
    description = "Linux file decompression with zlib"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "exfiltration"),
        ("technique", "data-compressed"),
        ("id", "T1002"),
        ("name", "linux-zlib-decompress"),
    )

    options = {"input": {}, "output": {}}

    dependencies = [helix_utils.LinuxAPTDependency("zlib1g-dev")]

    libraries = ["z"]

    source = "linux-decompress-zlib.cpp"
    function = "linux_decompress_zlib"
