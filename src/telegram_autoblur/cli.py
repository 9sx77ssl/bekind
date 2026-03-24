import argparse

from telegram_autoblur.app import run
from telegram_autoblur.matcher import blur_text


def main() -> None:
    parser = argparse.ArgumentParser(prog="bekind.py")
    parser.add_argument("--check-text", help="Check how text will look after blur")
    args = parser.parse_args()

    if args.check_text is not None:
        print(blur_text(args.check_text))
        return

    run()
