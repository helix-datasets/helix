import os
import uuid
import traceback
import multiprocessing

from ... import build
from ... import utils
from ... import exceptions

from .. import utils as mutils


def parse(components, load, transforms):
    try:
        classes = [
            utils.load("helix.components", utils.parse(c)["name"]) for c in components
        ]
    except exceptions.EntrypointNotFound as e:
        mutils.print(e, color=mutils.Color.red)
        exit(1)

    if load:
        loaded = mutils.load(*load)
        components += [c.name for c in loaded]
        classes += loaded

    blueprints = set.intersection(*[set(c.blueprints) for c in classes])

    if len(blueprints) > 1:
        mutils.print(
            "multiple possible blueprints found: {}".format(", ".join(blueprints)),
            color=mutils.Color.red,
        )
        exit(1)
    elif len(blueprints) < 1:
        mutils.print(
            "no common blueprint that supports all components could be found",
            color=mutils.Color.red,
        )
        exit(1)

    blueprint = blueprints.pop()

    try:
        classes = [utils.load("helix.transforms", t) for t in transforms]
    except exceptions.EntrypointNotFound as e:
        mutils.print(e, color=mutils.Color.red)
        exit(1)

    return blueprint, components, load, transforms


def process(blueprint, components, transforms, loads, working):
    identifier = uuid.uuid4()

    configuration = {
        "name": identifier.hex,
        "blueprint": {"name": blueprint},
    }

    configuration["components"] = [utils.parse(c) for c in components]

    if loads:
        loaded = mutils.load(*loads)

        for specification in configuration["components"]:
            name = specification["name"]

            for c in loaded:
                if c().name == name:
                    specification["class"] = c
                    specification.pop("name")

    configuration["transforms"] = [utils.parse(t) for t in transforms]

    project = os.path.join(working, identifier.hex)

    os.makedirs(project)

    stdout = os.path.join(project, "stdout.txt")
    stderr = os.path.join(project, "stderr.txt")

    with open(stdout, "wb") as stdout, open(stderr, "wb") as stderr:
        try:
            _, tags = build.build(
                configuration,
                os.path.join(working, identifier.hex),
                options={
                    "stdout": stdout,
                    "stderr": stderr,
                },
            )
        except Exception as e:
            print(
                "{} {}: {}".format(
                    mutils.format("✗", color=mutils.Color.red), identifier.hex, e
                )
            )

            with open(os.path.join(project, "exception.txt"), "w") as f:
                traceback.print_exc(file=f)

            return {}

    print(
        "{} {}".format(
            mutils.format("✓", color=mutils.Color.green),
            identifier.hex,
        )
    )

    return {identifier.hex: tags}


def generate(blueprint, samples, load, transforms, output, workers):
    print(
        "building {} samples with {} workers".format(
            mutils.format(len(samples), style=mutils.Style.bold),
            mutils.format(workers, style=mutils.Style.bold),
        )
    )

    arguments = [
        (
            blueprint,
            sample,
            transforms,
            load,
            output,
        )
        for sample in samples
    ]

    if workers == 1:
        results = [process(*a) for a in arguments]
    else:
        with multiprocessing.Pool(workers) as pool:
            results = pool.starmap(process, arguments)

    return results
