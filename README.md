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

You can write `.env` in either format:

```env
TG_API_ID=123456
TG_API_HASH=your_api_hash_here
TG_SESSION_NAME=bekind
```

or:

```env
export TG_API_ID=123456
export TG_API_HASH=your_api_hash_here
export TG_SESSION_NAME=bekind
```

## 5. Run the bot

```bash
python3 bekind.py
```

You can also run it from another folder:

```bash
python3 /full/path/to/bekind.py
```

The script will still find `.env` and will keep the session file inside the project folder.

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
- `src/telegram_autoblur/data/rules.toml` — single rules file with all words, roots, patterns and safe words
- `.vscode/settings.json` — VS Code settings so imports from `src` work without warnings
