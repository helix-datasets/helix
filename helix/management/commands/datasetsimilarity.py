import os
import math
import copy
import json
import random

from .. import utils as mutils

from . import dataset


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


class Command(mutils.CommandBase):
    """Generate a similarity dataset from a collection of Components.

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

        blueprint, components, load, transforms = dataset.parse(
            options["components"], options["load"], options["transforms"]
        )

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

        results = dataset.generate(
            blueprint, samples, load, transforms, output, options["workers"]
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
