from .... import utils
from ...... import utils as helix_utils


class AttackLinuxLibcURLRemoteFileCopyComponent(utils.SimpleTemplatedComponent):
    """Download a file with libcURL.

    Note:
        This component requires libcurl-dev to be installed.
    """

    name = "linux-libcurl-remote-file-copy"
    verbose_name = "Linux LibcURL Remote File Copy"
    description = "Download a file with libcURL"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "command-and-control"),
        ("technique", "remote-file-copy"),
        ("id", "T1105"),
        ("name", "linux-libcurl"),
    )

    blueprints = ["cmake-cpp"]

    options = {"url": {}, "output": {}}

    dependencies = [helix_utils.LinuxAPTDependency("libcurl4-gnutls-dev")]

    libraries = ["curl"]

    source = "linux-download-libcurl.cpp"
    function = "linux_download_libcurl"
    extras = ["write_data"]
