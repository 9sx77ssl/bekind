# Telegram AutoBlur

Userbot on `pyrogram` that edits your outgoing Telegram messages and blurs Russian profanity.

## Quick Start

```bash
cd /home/rsz/Desktop/blur
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Fill `.env` with your values from `https://my.telegram.org`.

Then run:

```bash
telegram-autoblur
```

Or:

```bash
python3 -m telegram_autoblur
```

At first launch, Pyrogram will ask for:

- your phone number
- Telegram login code
- 2FA password if enabled

## Useful Commands

Check a phrase without launching Telegram:

```bash
telegram-autoblur --check-text "ты хуесос и пидорас"
```

Run tests:

```bash
python3 -m unittest tests.test_matcher tests.test_app -v
```

## Project Layout

- `src/telegram_autoblur/app.py` — Telegram client
- `src/telegram_autoblur/matcher.py` — blur engine
- `src/telegram_autoblur/loader.py` — source loading
- `src/telegram_autoblur/data/manual_words.txt` — manual additions
- `src/telegram_autoblur/data/safe_words.txt` — safe words
- `src/telegram_autoblur/data/patterns.txt` — regex rules
- `tests/test_matcher.py` — checks
