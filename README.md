#  Gaslight Lyricsor Bot

**Gaslight** is a Telegram bot that finds and returns song lyrics based on the song name you give it.

---

## 🇬🇧 English

### ✨ Features

- 🔎 Search for a song by name (and artist, if available)
- 🧠 Automatic typo correction — shows the best match even with spelling mistakes
- 📋 Smart search via the **iTunes API**, returning up to 10 similar results so the user can pick the most accurate one
- ⌨️ Manual, precise search with the command:
  ```
  /search music by artist
  ```
- 📜 Lyrics fetched from multiple sources (with a configurable priority order):
  - [Genius](https://genius.com/developers) (via `lyricsgenius`)
  - [lrclib](https://lrclib.net/)
  - [lyrics.ovh](https://lyricsovh.docs.apiary.io/)
  - [iTunes Search API](https://performance-partners.apple.com/search-api)
- 🌐 Bilingual interface: **Persian** and **English** (user-switchable)
- ✂️ Automatic message splitting to respect Telegram's 4096-character limit

> ℹ️ This project intentionally does **not** include caching, audio-based song recognition, or usage statistics — the focus is purely on accurate search and lyrics retrieval.

### 🛠️ Tech Stack

| Part | Technology |
|---|---|
| Language | Python 3.11+ |
| Telegram bot library | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (async version) |
| Lyrics & search sources | `lyricsgenius`, iTunes Search API, lrclib, lyrics.ovh |

### 📁 Project Structure

```
gaslight/
├── bot.py                     # Main entry point, runs the bot
├── config.py                   # Loads settings and environment variables
├── .env                        # Tokens and API keys (never committed)
├── .env.example                 # Example file without real values
├── handlers/                     # Command and message handlers
│   ├── start.py
│   ├── search.py                 # Handles automatic song search
│   ├── manual_search.py           # Handles /search music by artist
│   └── language.py                # Language switching
├── services/
│   ├── lyrics_service.py         # Lyrics fetching logic from multiple sources + fallback
│   ├── itunes_service.py          # Search and fetch up to 10 similar results from iTunes
│   └── spell_correction.py        # Typo detection and best-match logic
├── locales/                        # Translation files (fa.json / en.json)
├── requirements.txt
├── .gitignore
└── README.md
```

### 🚀 Local Setup

**Prerequisites**
- Python 3.11 or later
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Genius API key from [genius.com](https://genius.com/api-clients)

**Steps**

1. Clone the repository
   ```bash
   git clone https://github.com/YOUR-USERNAME/gaslight.git
   cd gaslight
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   cp .env.example .env
   ```
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   GENIUS_API_TOKEN=your_genius_api_key_here
   ```
   > ⚠️ Never commit the `.env` file — it's already in `.gitignore`.
   > ℹ️ iTunes, lrclib, and lyrics.ovh don't require API keys, so the tokens above are all you need.

5. Run the bot
   ```bash
   python bot.py
   ```
   The bot currently runs in **polling** mode, which is simpler for local development and doesn't require a domain or HTTPS.

### 💬 Usage

**Automatic search**
1. Start the bot with `/start`
2. Send the song name (and artist, if possible)
3. The bot uses iTunes to find up to 10 similar results and shows the best match — even correcting typos
4. Lyrics are fetched from one of the sources (Genius, lrclib, lyrics.ovh, or iTunes) and sent to you, split across multiple messages if needed

**Manual search**
If you know the exact song and artist:
```
/search music by artist
```
Example:
```
/search Blinding Lights by The Weeknd
```

**Language switching**
Use the language command to switch between Persian and English.

### ⚖️ Copyright Note

Song lyrics are typically copyrighted. This bot only retrieves lyrics through APIs licensed to display this content (Genius, lrclib, lyrics.ovh, iTunes) and does not bulk-store or redistribute lyrics outside the bot's context.

### 🤝 Contributing

This project is a learning journey, so if you spot a bug or have a suggestion, feel free to open an Issue or Pull Request.

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div dir="rtl">

## 🇮🇷 فارسی

**Gaslight** یه ربات تلگرامیه که اسم یه آهنگ رو بهش می‌دی و لیریکس (متن) اون آهنگ رو برات پیدا می‌کنه و برمی‌گردونه.

### ✨ امکانات

- 🔎 جستجوی آهنگ با اسم (و در صورت امکان اسم خواننده)
- 🧠 تشخیص خودکار غلط املایی در جستجو و نمایش بهترین تطبیق ممکن
- 📋 جستجوی هوشمند از طریق **iTunes API** که تا ۱۰ نتیجه‌ی مشابه پیدا می‌کنه تا کاربر بتونه دقیق‌ترین گزینه رو انتخاب کنه
- ⌨️ جستجوی دستی و دقیق با دستور:
  ```
  /search music by artist
  ```
- 📜 دریافت لیریکس از چند منبع مختلف (ترتیب اولویت قابل تنظیم):
  - [Genius](https://genius.com/developers) (از طریق `lyricsgenius`)
  - [lrclib](https://lrclib.net/)
  - [lyrics.ovh](https://lyricsovh.docs.apiary.io/)
  - [iTunes Search API](https://performance-partners.apple.com/search-api)
- 🌐 پشتیبانی از دو زبان: **فارسی** و **انگلیسی** (قابل تغییر توسط کاربر)
- ✂️ تقسیم خودکار پیام‌های طولانی (رعایت محدودیت ۴۰۹۶ کاراکتری تلگرام)

> ℹ️ این پروژه قرار نیست فیچرهایی مثل **کش کردن نتایج**، **شناسایی موزیک از فایل صوتی**، یا **آمار استفاده از ربات** داشته باشه — تمرکز فقط روی جستجو و دریافت دقیق لیریکسه.

### 🛠️ تکنولوژی‌های استفاده‌شده

| بخش | تکنولوژی |
|---|---|
| زبان برنامه‌نویسی | Python 3.11+ |
| کتابخونه‌ی ربات تلگرام | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (نسخه‌ی async) |
| منابع لیریکس و جستجو | `lyricsgenius`، iTunes Search API، lrclib، lyrics.ovh |

### 📁 ساختار پروژه

```
gaslight/
├── bot.py                     # نقطه ورود اصلی، اجرای ربات
├── config.py                   # خواندن تنظیمات و متغیرهای محیطی
├── .env                        # توکن‌ها و کلیدهای API (هرگز commit نمی‌شه)
├── .env.example                 # نمونه‌ی بدون مقدار واقعی
├── handlers/                     # هندلرهای دستورات و پیام‌ها
│   ├── start.py
│   ├── search.py                 # هندل کردن جستجوی خودکار آهنگ
│   ├── manual_search.py           # هندل دستور /search music by artist
│   └── language.py                # تغییر زبان
├── services/
│   ├── lyrics_service.py         # منطق گرفتن لیریکس از چند منبع + fallback
│   ├── itunes_service.py          # جستجو و پیدا کردن ۱۰ نتیجه‌ی مشابه از iTunes
│   └── spell_correction.py        # تشخیص غلط املایی و بهترین تطبیق
├── locales/                        # فایل‌های ترجمه (fa.json / en.json)
├── requirements.txt
├── .gitignore
└── README.md
```

### 🚀 راه‌اندازی و اجرا (Local Setup)

**پیش‌نیازها**
- Python نسخه‌ی 3.11 یا بالاتر
- یه اکانت تلگرام و ساخت ربات از طریق [@BotFather](https://t.me/BotFather)
- یه API key از [Genius](https://genius.com/api-clients)

**مراحل**

۱. کلون کردن پروژه
```bash
git clone https://github.com/YOUR-USERNAME/gaslight.git
cd gaslight
```

۲. ساخت محیط مجازی (Virtual Environment)

> 💡 `venv` یه محیط ایزوله می‌سازه که کتابخونه‌های این پروژه رو از بقیه‌ی سیستمت جدا نگه می‌داره.

```bash
python -m venv venv
source venv/bin/activate   # ویندوز: venv\Scripts\activate
```

۳. نصب کتابخونه‌ها
```bash
pip install -r requirements.txt
```

۴. تنظیم متغیرهای محیطی

فایل `.env.example` رو کپی کن و اسمش رو بذار `.env`، بعد مقادیر واقعی رو داخلش بذار:

```bash
cp .env.example .env
```

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GENIUS_API_TOKEN=your_genius_api_key_here
```

> ⚠️ فایل `.env` هرگز نباید commit بشه — داخل `.gitignore` قرار داره.
> ℹ️ iTunes، lrclib و lyrics.ovh نیازی به API key ندارن، پس فقط توکن‌های بالا کافیه.

۵. اجرای ربات
```bash
python bot.py
```

ربات فعلاً به روش **polling** اجرا می‌شه (یعنی خودش مدام از تلگرام سوال می‌کنه «پیام جدیدی هست؟») که برای اجرای لوکال ساده‌تره و نیازی به دامنه یا HTTPS نداره.

### 💬 نحوه‌ی استفاده

**جستجوی عادی (خودکار)**
۱. ربات رو با `/start` استارت کن
۲. اسم آهنگ (و ترجیحاً اسم خواننده) رو بفرست
۳. ربات با استفاده از iTunes تا ۱۰ نتیجه‌ی مشابه پیدا می‌کنه و بهترین تطبیق (حتی اگه غلط املایی داشته باشی) رو نشون می‌ده
۴. لیریکس از یکی از منابع (Genius، lrclib، lyrics.ovh یا iTunes) برات ارسال می‌شه — اگه طولانی باشه، در چند پیام تقسیم می‌شه

**جستجوی دستی (دقیق)**

اگه دقیقاً می‌دونی اسم آهنگ و خواننده چیه، می‌تونی مستقیم بنویسی:
```
/search music by artist
```
مثال:
```
/search Blinding Lights by The Weeknd
```

**تغییر زبان**

با دستور تغییر زبان می‌تونی بین فارسی/انگلیسی جابه‌جا شی.

### ⚖️ نکته‌ی کپی‌رایت

متن آهنگ‌ها معمولاً کپی‌رایت دارن. این ربات فقط از طریق APIهایی که مجوز نمایش این محتوا رو دارن (Genius، lrclib، lyrics.ovh، iTunes) لیریکس رو دریافت می‌کنه و هیچ ذخیره‌سازی انبوه یا توزیع مجدد لیریکس بیرون از context ربات انجام نمی‌ده.

### 🤝 مشارکت

این پروژه در حال یادگیریه، پس اگه پیشنهاد یا باگی دیدی خوشحال می‌شم از طریق Issue یا Pull Request مطرحش کنی.

### 📄 لایسنس

این پروژه تحت لایسنس [MIT](LICENSE) منتشر شده.

</div>
