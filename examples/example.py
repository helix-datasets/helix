from helix import utils

output = "./example"

MinimalExampleComponent = utils.load("helix.components", "minimal-example")
minimal = MinimalExampleComponent()
minimal.generate()
minimal.finalize()

ConfigurationExampleComponent = utils.load("helix.components", "configuration-example")
config = ConfigurationExampleComponent()
config.configure(second_word="example")
config.generate()
config.finalize()

components = [minimal, config]

ReplaceExampleTransform = utils.load("helix.transforms", "replace-example")
replace = ReplaceExampleTransform()
replace.configure(old="hello", new="goodbye")

StripTransform = utils.load("helix.transforms", "strip")
strip = StripTransform()

transforms = [replace, strip]

CMakeCppBlueprint = utils.load("helix.blueprints", "cmake-cpp")
blueprint = CMakeCppBlueprint("example", components, transforms)
artifacts = blueprint.build(output)

for artifact in artifacts:
    print(artifact)
