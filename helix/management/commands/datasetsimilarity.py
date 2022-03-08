import os
import math
import copy
import uuid
import json
import random
import traceback
import multiprocessing

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


class Command(mutils.CommandBase):
    """Generate a dataset from a collection of Components.

    .. code-block:: none

        usage: helix dataset-similarity [-h] [-c [COMPONENTS [COMPONENTS ...]]] [-l [file [file ...]]] [-t [TRANSFORMS [TRANSFORMS ...]]] [-s SAMPLE_COUNT]
                                        [-m MAXIMUM_SAMPLES] [-n COMPONENT_COUNT] [-w WORKERS] [-v]
                                        {simple,random,walk} output

        positional arguments:
          {simple,random,walk}  dataset generation strategy
          output                output directory where dataset should be written

        optional arguments:
          -h, --help            show this help message and exit
          -c [COMPONENTS [COMPONENTS ...]], --components [COMPONENTS [COMPONENTS ...]]
                                component(s) to include (by name)
          -l [file [file ...]], --load [file [file ...]]
                                load additional component(s) from one or more files
          -t [TRANSFORMS [TRANSFORMS ...]], --transforms [TRANSFORMS [TRANSFORMS ...]]
                                transform(s) to apply to all samples (by name)
          -s SAMPLE_COUNT, --sample-count SAMPLE_COUNT
                                number of samples to attempt to generate
          -m MAXIMUM_SAMPLES, --maximum-samples MAXIMUM_SAMPLES
                                maximum number of samples to generate
          -n COMPONENT_COUNT, --component-count COMPONENT_COUNT
                                number of components per sample
          -w WORKERS, --workers WORKERS
                                number of parallel workers to use (default: <count(CPUs)/2>)
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

        print(
            "building {} samples with {} workers".format(
                mutils.format(len(samples), style=mutils.Style.bold),
                mutils.format(options["workers"], style=mutils.Style.bold),
            )
        )

        arguments = [
            (
                blueprint,
                sample,
                transforms,
                options.get("load"),
                output,
            )
            for sample in samples
        ]

        if options["workers"] == 1:
            results = [process(*a) for a in arguments]
        else:
            with multiprocessing.Pool(options["workers"]) as pool:
                results = pool.starmap(process, arguments)

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
