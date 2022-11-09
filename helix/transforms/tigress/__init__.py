import logging
import sys

"""Custom logger for tiggress transform."""
logger = logging.getLogger("transform.tigress")
logger.setLevel(logging.INFO)

console = logging.StreamHandler(stream=sys.stdout)
console.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)s %(name)s]: %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)
