import os
import math
import copy
import uuid
import json
import random

from ... import build
from ... import utils
from ... import exceptions

from .. import utils as mutils


class SamplingError(Exception):
    """Raised when there is a problem generating a sample list."""


def simple(collection, samples, components):
    """A single component per sample for every component.

    Note:
        This simply ignores the requested number of samples and components and
        returns a single sample with a single component for every component in
        the collection.
    """

    return [[c] for c in collection]


def rand(collection, samples, components):
    """A completely random dataset - may contain exact duplicates."""

    options = []

    for _ in range(samples):
        options.append(random.sample(collection, components))

    return options


def walk(collection, samples, components):
    """A sample walk with random permutations for increased similarity.

    Generates a dataset by randomly replacing a random number of components
    from one build to the next to inject aditional similarity over a simple
    random strategy.
    """

    CHANGE = 0.02

    options = []

    for _ in range(samples):
        if options:
            sample = copy.deepcopy(options[-1])

            change = random.randint(0, math.ceil(components * CHANGE))
            for _ in range(change):
                changed = random.randint(0, components - 1)
                sample[changed] = random.choice(collection)

            options.append(sample)
        else:
            options.append(random.sample(collection, components))

    return options


def process(blueprint, components, transforms, loads, working, verbose=False):
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

    name = "[{}]".format(", ".join(components))

    try:
        _, tags = build.build(
            configuration,
            os.path.join(working, identifier.hex),
            options={"propagate": verbose},
        )
    except (exceptions.BuildFailure, exceptions.ConfigurationError):
        print(
            "{} {} {}".format(
                name,
                mutils.format("✗", color=mutils.Color.red),
                identifier.hex,
            )
        )

        return {}

    print(
        "{} {} {}".format(
            name,
            mutils.format("✓", color=mutils.Color.green),
            identifier.hex,
        )
    )

    return {identifier.hex: tags}


class Command(mutils.CommandBase):
    """Generate a dataset from a collection of Components.

    .. code-block:: none

        TODO
    """

    name = "dataset-similarity"
    help = "generate a similarity dataset from a collection of components"

    def add_arguments(self, parser):
        parser.add_argument(
            "strategy",
            type=str,
            choices=["simple", "random", "walk"],
            help="dataset generation strategy",
        )

        parser.add_argument(
            "output", type=str, help="output directory where dataset should be written"
        )

        parser.add_argument(
            "-c",
            "--components",
            help="component(s) to include (by name)",
            nargs="*",
            default=[],
        )
        parser.add_argument(
            "-l",
            "--load",
            help="load additional component(s) from one or more files",
            metavar="file",
            nargs="*",
            default=[],
        )
        parser.add_argument(
            "-t",
            "--transforms",
            help="transform(s) to apply to all samples (by name)",
            nargs="*",
            default=[],
        )

        parser.add_argument(
            "-s",
            "--sample-count",
            type=int,
            default=60,
            help="number of samples to attempt to generate",
        )
        parser.add_argument(
            "-m",
            "--maximum-samples",
            type=int,
            default=None,
            help="maximum number of samples to generate",
        )
        parser.add_argument(
            "-n",
            "--component-count",
            type=int,
            default=20,
            help="number of components per sample",
        )
        parser.add_argument(
            "-w",
            "--workers",
            metavar="WORKERS",
            type=int,
            default=round(os.cpu_count() / 2),
            help="number of parallel workers to use (default: <count(CPUs)/2>)",
        )
        parser.add_argument(
            "-v", "--verbose", action="store_true", help="build in verbose mode"
        )

    def handle(self, *args, **options):
        output = os.path.abspath(os.path.expanduser(options["output"]))

        if os.path.isdir(output):
            pass
        else:
            try:
                os.makedirs(output)
            except Exception as e:
                mutils.print(e, color=mutils.Color.red)
                exit(1)

        components = options.get("components")

        try:
            classes = [
                utils.load("helix.components", utils.parse(c)["name"])
                for c in components
            ]
        except exceptions.EntrypointNotFound as e:
            mutils.print(e, color=mutils.Color.red)
            exit(1)

        if options.get("load"):
            loaded = mutils.load(*options["load"])
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

        transforms = options.get("transforms")

        try:
            classes = [utils.load("helix.transforms", t) for t in transforms]
        except exceptions.EntrypointNotFound as e:
            mutils.print(e, color=mutils.Color.red)
            exit(1)

        if options["strategy"] == "simple":
            strategy = simple
        elif options["strategy"] == "random":
            strategy = rand
        elif options["strategy"] == "walk":
            strategy = walk
        else:
            mutils.print(
                "unknown generation strategy: {}".format(options["strategy"]),
                color=mutils.Color.red,
            )
            exit(1)

        try:
            samples = strategy(
                components,
                samples=options.get("sample_count"),
                components=options.get("component_count"),
            )
        except SamplingError as e:
            mutils.print(e, color=mutils.Color.red)
            exit(1)

        results = []
        for sample in samples:
            results.append(
                process(
                    blueprint,
                    sample,
                    transforms,
                    options.get("load"),
                    output,
                    verbose=options.get("verbose"),
                )
            )

        results = [r for r in results if r]
        if "maximum_samples" in options:
            results = results[: options["maximum_samples"]]

        labels = {}
        for result in results:
            labels.update(result)

        with open(os.path.join(output, "labels.json"), "w") as f:
            json.dump(labels, f)

        print(
            "built {} samples in {}".format(
                mutils.format(len(labels), style=mutils.Style.bold),
                mutils.format(output, style=mutils.Style.bold),
            )
        )
