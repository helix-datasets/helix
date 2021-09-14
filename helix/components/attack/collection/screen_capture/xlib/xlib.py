from .... import utils
from ...... import utils as helix_utils


class AttackLinuxXLibScreenCaptureComponent(utils.SimpleTemplatedComponent):
    """Capture a screenshot with XLib.

    Note:
        This component requires libx11-dev and cimg-dev to be installed.
    """

    name = "linux-xlib-screen-capture"
    verbose_name = "Linux XLib Screen Capture"
    description = "Capture a screenshot with XLib"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "collection"),
        ("technique", "screen-capture"),
        ("id", "T1113"),
        ("name", "linux-xlib"),
    )

    blueprints = ["cmake-cpp"]

    options = {"output": {}}

    dependencies = [
        helix_utils.LinuxAPTDependency("libx11-dev"),
        helix_utils.LinuxAPTDependency("cimg-dev"),
    ]

    libraries = ["X11", "pthread"]

    source = "linux-screenshot-xlib.cpp"
    function = "linux_screenshot_xlib"
