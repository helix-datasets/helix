from helix import component
from helix import utils


class AttackLinuxCreateHiddenFileComponent(component.Component):
    """Create Hidden File in Linux."""

    name = "linux-create-hidden-file"
    verbose_name = "Linux Create Hidden File"
    description = "Linux File Deletion via remove"
    version = "1.0.0"
    type = "att&ck"
    date = "2024-07-01 :15:30.000000"
    tags = (
        ("family", "att&ck"),
        ("category", "defense-evasion"),
        ("technique", "hidden-file"),
        ("id", "T1564"),
        ("name", "linux-create"),
    )

    blueprints = ["cmake-c"]


    #options = {"path": {}}


    def generate(self):
        source = utils.source(__name__, "linux-create.c")

        self.functions = [source]
        self.calls = {"main": ["${new_file}();"]}
        self.globals = ["new_file"]
