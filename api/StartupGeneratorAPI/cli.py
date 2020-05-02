import argparse
import logging
import pathlib
import sys

from StartupGeneratorAPI.model.words import WordsTextFile

logger = logging.getLogger(__name__)


def main():
    args = _parse_args()
    args.func(args)


def _parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser("run")
    run_parser.set_defaults(func=_run)
    run_parser.add_argument(
        "--set_1",
        "-s1",
        required=True,
        type=pathlib.Path,
        help="Path to first word set.",
    )
    run_parser.add_argument(
        "--set_2",
        "-s2",
        required=True,
        type=pathlib.Path,
        help="Path to the second word set.",
    )

    api_parser = subparsers.add_parser("api")
    api_parser.set_defaults(func=_api)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def _run(args):
    set_1_loader = WordsTextFile(args.set_1)
    set_2_loader = WordsTextFile(args.set_2)
    print("{} for {}".format(set_1_loader.random, set_2_loader.random))


def _api(args):
    from StartupGeneratorAPI.routes import main as api_main

    api_main()


if __name__ == "__main__":
    main()
