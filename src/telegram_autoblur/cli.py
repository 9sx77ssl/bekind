import argparse

from telegram_autoblur.app import run
from telegram_autoblur.matcher import blur_text


def main() -> None:
    parser = argparse.ArgumentParser(prog="telegram-autoblur")
    parser.add_argument("--check-text", help="Preview how a text will be blurred without launching Telegram")
    args = parser.parse_args()

    if args.check_text is not None:
        print(blur_text(args.check_text))
        return

    run()
