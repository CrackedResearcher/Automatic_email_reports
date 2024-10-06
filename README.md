# Auto Email Summarizer 

This was the **first version** of CalmEmail. I started working on it out of the blue in June, thinking, "What if I could build something that automatically sends me email summaries at specific intervals?" So, I built this tool.

## What It Does

This is an email summarizer assistant that you run from your terminal. Once you run the project, it will:

1. Fetch your latest emails.
2. Summarize those emails using **Google Gemini** (AI).
3. Automatically send you the summary via email at intervals you choose.

You just have to run the project, and it’ll take care of setting up cron jobs based on your input—no manual setup needed!

### Key Features

- **Automated Summaries**: Fetches the latest emails and summarizes them.
- **Cron Job Setup**: Automatically sets up cron jobs based on what you tell it.
- **Database Storage**: Keeps track of the last time emails were fetched using SQLite3, so it only fetches new ones next time.
- **Email Automation**: Fetches and sends the summaries via email.

---

## Tech Stack

| **Tech**              | **Purpose**                                         |
|-----------------------|-----------------------------------------------------|
| **Python**            | The main programming language                       |
| **Google Gemini AI**  | Used for summarizing emails                         |
| **Colorama**          | Makes the terminal look cool with colored text      |
| **SQLite3**           | Stores data about the emails you've already fetched |
| **IMAP**              | Fetches your emails from your inbox                 |
| **SMTP**              | Sends the summarized emails                        |
| **Cron Jobs**         | Automates the tool to run at intervals you set      |

---

## How to Get It Running

### 1. Clone the Project

```bash
git clone https://github.com/YOUR_USERNAME/Terminal_CalmEmail.git
cd calmemail
```

### 2. Set Up a Virtual Environment (Optional, but nice to have)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

All the Python packages you need are listed in the `requirements.txt` file. Just run:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

You'll need an API key for Google Gemini. Set it up like this:

1. Create a `.env` file in the project root (or copy the example):

```bash
cp .env.example .env
```

2. Then edit your `.env` file to look like this:

```bash
API_KEY=your-google-gemini-api-key
```

### 5. Run the Project

Just run it in your terminal:

```bash
python calmemail.py
```

The project will ask you for your email config and when you want it to run. It’ll handle setting up the cron job for you and start summarizing and sending emails.

---

## Requirements

Here's what you'll need to install (this is already in the `requirements.txt` file):

```bash
google-generativeai
python-dotenv
requests
colorama
sqlite3
```

---

## Summary of How It Works

1. Run the tool once, and it’ll ask you for your email details and schedule.
2. Based on your input, the tool will automatically fetch new emails, summarize them using Google Gemini, and send you the summary.
3. You don’t need to worry about setting up cron jobs—CalmEmail handles all that for you.

---

## Contributing

If you want to contribute to the project, feel free to fork the repository and submit a pull request!

---

## License

This project is licensed under the MIT License.

---
