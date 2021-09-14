from .... import utils


class AttackWindowsBitBltScreenCaptureComponent(utils.SimpleTemplatedComponent):
    """Capture a screenshot with BitBlt."""

    name = "windows-bitblt-screen-capture"
    verbose_name = "Windows BitBlt Screen Capture"
    description = "Capture a screenshot with BitBlt"
    version = "1.0.0"
    type = "att&ck"
    date = "2019-10-01 17:15:00.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "collection"),
        ("technique", "screen-capture"),
        ("id", "T1113"),
        ("name", "windows-bitblt"),
    )

    options = {"output": {}}

    source = "windows-screenshot-bitblt.cpp"
    function = "windows_screenshot_bitblt"
