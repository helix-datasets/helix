import os
import json
import random

from .. import utils as mutils

from . import dataset


def classification(
    universe,
    classes,
    features,
    smin,
    smax,
    cratiomin,
    cratiomax,
    sratiomin,
    sratiomax,
    noiseratiomin,
    noiseratiomax,
    reclassratio,
    shuffle=True,
    seed=None,
):
    """Generate a classification task from a given universe of binary features.

    Generates a configurable set of classes with samples with a given set of
    parameters.

    Args:
        universe (set): A set of possible values to include in samples. This
            must have a minimum of ``features`` values and ideally far more.
        classes (int): The number of classes to generate.
        features (int): The number of features each sample should include.
        smin (int): The minimum number of samples per class.
        smax (int): The maximum number of samples per class.
        cratiomin (float): The minimum ratio of samples to preserve for
            centroid generation.
        cratiomin (float): The maximum ratio of samples to preserve for
            centroid generation.
        sratiomin (float): The minimum ratio of samples to preserve for sample
            generation from a class centroid.
        sratiomax (float): The maximum ratio of samples to preserve for sample
            generation from a class centroid.
        noiseratiomin (float): The minimum ratio of features to randomly
            replace in a sample.
        noiseratiomax (float): The maximum ratio of features to randomly
            replace in a sample.
        reclassratio (float): The ratio of samples to randomly reclass.
        shuffle (bool): If ``True`` samples and classes are shuffled before
            being returned.
        seed (int): A value to be used as the random seed. Optional. Set this
            if you would like a deterministic generation.
    """

    assert classes > 1
    # assert len(universe) > features * classes * 10
    assert smin <= smax
    assert cratiomin <= cratiomax
    assert sratiomin <= sratiomax

    if seed:
        random.seed(seed)

    def permute(sample, ratio):
        keep = int(features * ratio)
        permuted = random.sample(sample, k=keep)
        remaining = features - keep
        permuted += random.sample(universe - set(permuted), k=remaining)

        permuted = list(set(permuted))

        assert len(permuted) == features

        random.shuffle(permuted)

        return permuted

    # generate centroids
    centroids = []
    for _ in range(classes):
        if centroids:
            cratio = random.uniform(cratiomin, cratiomax)
            centroid = permute(centroids[-1], cratio)
        else:
            centroid = random.sample(universe, k=features)

        centroids.append(centroid)

    noiseclass = set(random.sample(universe, k=features * 2))

    # generate class samples
    classed = []
    for i in range(classes):
        classed.append([])
        samples = random.randint(smin, smax)
        for _ in range(samples):
            sratio = random.uniform(sratiomin, sratiomax)
            sample = permute(centroids[i], sratio)

            # add noise features
            noise = random.uniform(noiseratiomin, noiseratiomax)
            noise = int(noise * features)
            for _ in range(noise):
                index = random.randint(0, features - 1)
                sample[index] = random.choice(list(noiseclass - set(sample)))

            classed[-1].append(sample)

    # split samples and labels
    samples, labels = [], []
    for i, c in enumerate(classed):
        samples += c
        labels += [i] * len(c)

    # randomly reclass
    reclass = int(reclassratio * len(labels))
    for _ in range(reclass):
        index = random.randint(0, len(labels) - 1)
        labels[index] = random.randint(0, classes - 1)

    # random shuffle
    if shuffle:
        zipped = list(zip(samples, labels))
        random.shuffle(zipped)
        samples, labels = zip(*zipped)

    return samples, labels


class Command(mutils.CommandBase):
    """Generate a classification dataset from a collection of Components.

    .. code-block:: none

        TODO
    """

    name = "dataset-classification"
    help = "generate a classification dataset from a collection of components"

    def add_arguments(self, parser):
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
            "-a",
            "--class-count",
            type=int,
            default=2,
            help="number of classes to generate (default: 2)",
        )
        parser.add_argument(
            "-n",
            "--component-count",
            type=int,
            default=25,
            help="number of components per sample (default: 25)",
        )
        parser.add_argument(
            "-smin",
            "--sample-minimum",
            type=int,
            default=20,
            help="minimum number of samples per class (default: 20)",
        )
        parser.add_argument(
            "-smax",
            "--sample-maximum",
            type=int,
            default=100,
            help="maximum number of samples per class (default: 100)",
        )
        parser.add_argument(
            "-crmin",
            "--class-ratio-minimum",
            type=float,
            default=0.4,
            help="minimum class replacement ratio (default: 0.4)",
        )
        parser.add_argument(
            "-crmax",
            "--class-ratio-maximum",
            type=float,
            default=0.8,
            help="maximum class replacement ratio (default: 0.8)",
        )
        parser.add_argument(
            "-srmin",
            "--sample-ratio-minimum",
            type=float,
            default=0.8,
            help="minimum intra-class sample replacement ratio (default: 0.8)",
        )
        parser.add_argument(
            "-srmax",
            "--sample-ratio-maximum",
            type=float,
            default=0.95,
            help="maximum intra-class sample replacement ratio (default: 0.95)",
        )
        parser.add_argument(
            "-nrmin",
            "--noise-ratio-minimum",
            type=float,
            default=0.4,
            help="minimum sample noise ratio (default: 0.4)",
        )
        parser.add_argument(
            "-nrmax",
            "--noise-ratio-maximum",
            type=float,
            default=0.6,
            help="maximum sample noise ratio (default: 0.6)",
        )
        parser.add_argument(
            "-mr",
            "--misclassification-ratio",
            type=float,
            default=0.02,
            help="the percentage of samples to randomly misclassify (default: 0.02)",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=None,
            help="random seed (for deterministic builds)",
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

        samples, labels = classification(
            universe=set(components),
            classes=options["class_count"],
            features=options["component_count"],
            smin=options["sample_minimum"],
            smax=options["sample_maximum"],
            cratiomin=options["class_ratio_minimum"],
            cratiomax=options["class_ratio_maximum"],
            sratiomin=options["sample_ratio_minimum"],
            sratiomax=options["sample_ratio_maximum"],
            noiseratiomin=options["noise_ratio_minimum"],
            noiseratiomax=options["noise_ratio_maximum"],
            reclassratio=options["misclassification_ratio"],
            seed=options.get("seed"),
        )

        results = dataset.generate(
            blueprint, samples, load, transforms, output, options["workers"]
        )

        truth = {}
        for result, label in zip(results, labels):
            if not result:
                continue

            name, tags = list(result.items())[0]

            truth[name] = {"class": label, "tags": tags}

        with open(os.path.join(output, "labels.json"), "w") as f:
            json.dump(truth, f)

        print(
            "built {} samples from {} classes in {}".format(
                mutils.format(len(truth), style=mutils.Style.bold),
                mutils.format(options["class_count"], style=mutils.Style.bold),
                mutils.format(output, style=mutils.Style.bold),
            )
        )
