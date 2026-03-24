# bekind

`bekind.py` is a Telegram userbot on `pyrogram`.
It watches your outgoing messages and edits Russian profanity into a blurred form.

Example:

- `блять` -> `бл*ть`
- `пидорас` -> `пи*ас`
- `хуесос` -> `ху*ос`

## 1. Clone the repository

```bash
git clone git@github.com:noki44ngel/bekind.git
cd bekind
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create the config file

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
TG_API_ID=123456
TG_API_HASH=your_api_hash_here
TG_SESSION_NAME=bekind
```

`TG_API_ID` and `TG_API_HASH` are created here:

- `https://my.telegram.org`

## 5. Run the bot

```bash
python3 bekind.py
```

On first start Telegram will ask for:

- your phone number
- the login code
- your 2FA password if you use one

## Check text without launching Telegram

```bash
python3 bekind.py --check-text "ты хуесос, а это мандарин"
```

## Run tests

```bash
python3 -m unittest tests.test_matcher tests.test_app -v
```

## Main files

- `bekind.py` — start file
- `src/telegram_autoblur/app.py` — Telegram client
- `src/telegram_autoblur/matcher.py` — text blur logic
- `src/telegram_autoblur/data/manual_words.txt` — your manual word list
- `src/telegram_autoblur/data/safe_words.txt` — words that must not be blurred
- `src/telegram_autoblur/data/patterns.txt` — regex patterns
